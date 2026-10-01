"""Composite an animation from one locked environment plate and keyed sprites.

The image model cannot hold a camera still: frames re-rolled from a previous
frame drift across the whole canvas. This builder never re-draws the plate. It
keys each sprite out of its flat paper background, scales it to a declared
size, and pastes it onto a pixel copy of the plate at declared anchor points.
The environment is therefore the same bytes in every frame, and the moving
regions are exactly the sprite footprints the builder wrote into the recipe.

Usage:
    python scripts/build_locked_motion.py build --recipe scripts/motion-recipes/hero.json
    python scripts/build_locked_motion.py check --recipe scripts/motion-recipes/hero.json

A recipe names the plate, the sprites, the frames as lists of placements, and
the output geometry. `build` writes the still (frame zero at plate resolution),
the GIF, and rewrites the recipe with the `moving_boxes` it computed, so the
committed recipe always describes the committed GIF. `check` re-verifies a
committed GIF against those boxes without needing the layers; it is the gate
that fails when the environment is not identical across frames.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_motion_gif

REPO_ROOT = Path(__file__).resolve().parent.parent

# A sprite's paper is the flat field it was drawn on. It is keyed by removing
# the paper colour only where it connects to the image border, so enclosed
# cream inside a drawing (a robot's body, a card's face) stays opaque.
PAPER_TOLERANCE = 46

# The moving-box union may not cover more than this fraction of the frame, and
# the locked remainder must still carry real drawing rather than bare paper.
# Without the second guard a recipe could unlock the whole scene and pass by
# declaring boxes over everything that matters.
MAX_MOVING_COVERAGE = 0.75
MIN_LOCKED_INK_FRACTION = 0.02


def paper_key(rgb: np.ndarray, tolerance: int = PAPER_TOLERANCE) -> np.ndarray:
    border = np.concatenate([rgb[0, :], rgb[-1, :], rgb[:, 0], rgb[:, -1]]).astype(np.int32)
    reference = np.median(border, axis=0)
    distance = np.abs(rgb.astype(np.int32) - reference).max(axis=-1)
    candidate = distance <= tolerance
    labels, _ = ndimage.label(candidate, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
    touching = set(labels[0, :]) | set(labels[-1, :]) | set(labels[:, 0]) | set(labels[:, -1])
    touching.discard(0)
    return np.isin(labels, list(touching))


def key_sprite(path: Path) -> Image.Image:
    """Return the sprite as RGBA with its border-connected paper made transparent."""
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)
    paper = paper_key(rgb)
    alpha = np.where(paper, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb, alpha]), "RGBA")


def landmarks(sprite: Image.Image) -> dict:
    """Measure the keyed sprite: ink bbox, feet row, shoulder row, ground centre.

    The shoulder row is the first row from the top whose ink width clears 45%
    of the widest row, which for these drawings is the coat line rather than a
    raised arm. The ground centre is the ink centroid of the bottom rows: the
    body's contact point with the floor. Anchoring x there rather than at the
    bbox centre keeps the torso still when a pose changes the silhouette.
    """
    alpha = np.asarray(sprite)[:, :, 3]
    ys, xs = np.where(alpha > 0)
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    widths = np.array([int((alpha[y] > 0).sum()) for y in range(y0, y1 + 1)])
    shoulder = y0 + int(np.argmax(widths > 0.45 * int(widths.max())))
    band = alpha[max(y0, y1 - 9) : y1 + 1]
    return {
        "bbox": (x0, y0, x1, y1),
        "feet": y1,
        "shoulder": shoulder,
        "body": y1 - shoulder,
        "ground_x": int(np.where(band > 0)[1].mean()),
    }


def fit_scale(info: dict, fit: str, size) -> float:
    """The scale that maps the measured sprite onto its declared plate size.

    `bbox`, `body` and `width` size one dimension and let the other follow the
    drawing. `contain` takes a [w, h] box and picks whichever dimension binds,
    so a wide icon cannot spill past the card it sits in.
    """
    x0, y0, x1, y1 = info["bbox"]
    if fit == "body":
        return size / info["body"]
    if fit == "bbox":
        return size / (y1 - y0)
    if fit == "width":
        return size / (x1 - x0)
    if fit == "contain":
        return min(size[0] / (x1 - x0), size[1] / (y1 - y0))
    raise SystemExit(f"unknown fit {fit!r}")


def anchor_point(info: dict, on: str) -> tuple[float, float]:
    """The sprite-space point a placement's (x, y) refers to."""
    x0, y0, x1, y1 = info["bbox"]
    if on == "feet":
        return info["ground_x"], y1
    if on in ("centre", "bbox"):
        return (x0 + x1) / 2, (y0 + y1) / 2
    raise SystemExit(f"unknown anchor {on!r}")


class Layer:
    """A keyed sprite and the geometry that places it.

    The builder renders every frame twice: once at plate resolution for the
    still, once at output resolution for the GIF. Both renders derive from the
    same measurements, so the still and the animation cannot disagree.

    Rendering in output space rather than scaling a finished composite is what
    keeps the environment byte-identical between frames. A plate pixel that
    touches a sprite edge would otherwise be resampled together with the
    sprite, and its value would depend on where the sprite stands.
    """

    def __init__(self, spec: dict, layers_dir: Path):
        self.name = spec["name"]
        # A static layer is pasted identically in every frame (an icon inside
        # its card). It is deliberately left out of the moving boxes: the
        # locked region then covers the icon too, and the check fails if a
        # rebuild ever lets it drift.
        self.static = bool(spec.get("static"))
        self.anchor_on = spec.get("anchor", "feet")
        image = key_sprite(layers_dir / spec["path"])
        info = landmarks(image)
        if spec.get("flip"):
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            width = image.width
            x0, y0, x1, y1 = info["bbox"]
            info = dict(
                info,
                bbox=(width - 1 - x1, y0, width - 1 - x0, y1),
                ground_x=width - 1 - info["ground_x"],
            )
        self.image = image
        scale = fit_scale(info, spec["fit"], spec["size"])
        ax, ay = anchor_point(info, self.anchor_on)
        # Everything below is in plate pixels: the fitted scale, the anchor
        # inside the scaled sprite, and the ink bbox it sweeps.
        self.scale = scale
        self.ax, self.ay = ax * scale, ay * scale
        x0, y0, x1, y1 = info["bbox"]
        self.rect = (x0 * scale, y0 * scale, x1 * scale, y1 * scale)
        self.bbox_height = (y1 - y0) * scale

    def render(self, out_scale: float, factor: float) -> tuple[Image.Image, float, float]:
        """The sprite at output resolution, with its anchor in output pixels."""
        total = self.scale * out_scale * factor
        image = self.image.resize(
            (max(1, int(round(self.image.width * total))),
             max(1, int(round(self.image.height * total)))),
            Image.LANCZOS,
        )
        return image, self.ax * out_scale * factor, self.ay * out_scale * factor


def resolve(placement: dict, layer: Layer) -> float:
    """The size multiplier for one placement, relative to its fitted scale.

    A placement may give a size: a target ink-bbox height in plate pixels for
    a layer that pulses (the comic burst). 0 hides the layer for that frame.
    """
    if "size" not in placement:
        return 1.0
    return placement["size"] / layer.bbox_height


def build_frame(
    placements: list[dict],
    layers: dict[str, Layer],
    plate: Image.Image,
    out_scale: float,
) -> Image.Image:
    """One frame: a plate copy, then each placement in recipe order.

    `plate` is at the resolution being rendered and placements are given in
    plate coordinates, so each anchor is multiplied by `out_scale`. Compositing
    at the target resolution rather than scaling a finished composite is what
    keeps the environment byte-identical: a plate pixel touching a sprite edge
    would otherwise be resampled together with the sprite, and its value would
    depend on where the sprite stands. Order is depth order: a layer listed
    later is nearer the reader, so the engineer occludes a robot running
    behind him.
    """
    canvas = plate.convert("RGBA").copy()
    for placement in placements:
        layer = layers[placement["layer"]]
        factor = resolve(placement, layer)
        if factor <= 0:
            continue
        image, ax, ay = layer.render(out_scale, factor)
        canvas.alpha_composite(
            image,
            (
                int(round(placement["x"] * out_scale - ax)),
                int(round(placement["y"] * out_scale - ay)),
            ),
        )
    return canvas.convert("RGB")


def moving_boxes(recipe: dict, layers: dict[str, Layer], plate_size, out_size) -> list[dict]:
    """Per-layer swept ink bbox in output pixels, from the placements drawn.

    The box is the keyed ink bbox at its placed position, unioned across every
    frame the layer appears in. It is the ink box rather than the sprite canvas
    so the locked region reaches as close to the character as it can.
    """
    sx = out_size[0] / plate_size[0]
    sy = out_size[1] / plate_size[1]
    swept: dict[str, list[float]] = {}
    for placements in recipe["frames"]:
        for placement in placements:
            layer = layers[placement["layer"]]
            if layer.static:
                continue
            factor = resolve(placement, layer)
            if factor <= 0:
                continue
            rx0, ry0, rx1, ry1 = layer.rect
            left = placement["x"] - layer.ax * factor + rx0 * factor
            top = placement["y"] - layer.ay * factor + ry0 * factor
            box = swept.setdefault(layer.name, [1e9, 1e9, -1e9, -1e9])
            box[0] = min(box[0], left)
            box[1] = min(box[1], top)
            box[2] = max(box[2], left + (rx1 - rx0) * factor)
            box[3] = max(box[3], top + (ry1 - ry0) * factor)
    # LANCZOS resampling of a sprite spreads its faint edge alpha a few output
    # pixels beyond the ink bbox, so the declared box is grown by the filter
    # support. Without this the check would fail on plate pixels the sprite
    # genuinely touched.
    margin = 4
    result = []
    for name, (x0, y0, x1, y1) in swept.items():
        left = max(0, int(np.floor(x0 * sx)) - margin)
        top = max(0, int(np.floor(y0 * sy)) - margin)
        right = min(out_size[0], int(np.ceil(x1 * sx)) + margin)
        bottom = min(out_size[1], int(np.ceil(y1 * sy)) + margin)
        result.append({"layer": name, "x": left, "y": top, "w": right - left, "h": bottom - top})
    return result


def load_recipe(path: Path) -> dict:
    recipe = json.loads(path.read_text(encoding="utf-8"))
    recipe["_path"] = path
    return recipe


def cmd_build(recipe_path: Path, layers_dir: Path, write_back: bool) -> int:
    recipe = load_recipe(recipe_path)
    plate = Image.open(layers_dir / recipe["plate"]).convert("RGB")
    out_size = tuple(recipe["output"])
    out_scale = out_size[0] / plate.width
    layers = {spec["name"]: Layer(spec, layers_dir) for spec in recipe["sprites"]}

    # The plate is resampled once and shared by every frame, so the locked
    # region is the same bytes by construction; only the sprites differ.
    plate_out = plate.resize(out_size, Image.LANCZOS)
    frames = [
        build_frame(placements, layers, plate_out, out_scale)
        for placements in recipe["frames"]
    ]

    still = REPO_ROOT / recipe["still"]
    still.parent.mkdir(parents=True, exist_ok=True)
    build_frame(recipe["frames"][0], layers, plate, 1.0).save(still, optimize=True)

    gif = REPO_ROOT / recipe["gif"]
    build_motion_gif.write_gif(build_motion_gif.quantize(frames), gif, recipe["durations"])

    boxes = moving_boxes(recipe, layers, plate.size, out_size)
    recipe["moving_boxes"] = boxes
    # The union, not the sum of areas: overlapping boxes must not be counted
    # twice, or a recipe could hide a huge swept region behind many small ones.
    mask = np.zeros((out_size[1], out_size[0]), dtype=bool)
    for box in boxes:
        mask[box["y"] : box["y"] + box["h"], box["x"] : box["x"] + box["w"]] = True
    coverage = mask.mean()
    if coverage > MAX_MOVING_COVERAGE:
        raise SystemExit(
            f"moving boxes cover {coverage:.0%} of the frame; the cap is "
            f"{MAX_MOVING_COVERAGE:.0%}, above which the lock check is meaningless"
        )
    ink = np.asarray(frames[0]).max(axis=2) < 120
    locked_ink = int((ink & ~mask).sum())
    if locked_ink < MIN_LOCKED_INK_FRACTION * out_size[0] * out_size[1]:
        raise SystemExit(
            f"only {locked_ink} ink pixels sit outside the moving boxes; at least "
            f"{MIN_LOCKED_INK_FRACTION:.0%} of the frame must be locked drawing"
        )
    if write_back:
        saved = {k: v for k, v in recipe.items() if k != "_path"}
        recipe_path.write_text(json.dumps(saved, indent=2) + "\n", encoding="utf-8")

    print(f"{recipe['name']}: {len(frames)} frames -> {gif.name} ({out_size[0]}x{out_size[1]})")
    print(f"  still -> {still.name}")
    print(f"  moving coverage {coverage:.1%}")
    for box in boxes:
        print(f"  {box['layer']:14s} x {box['x']:4d}-{box['x'] + box['w']:4d}  y {box['y']:4d}-{box['y'] + box['h']:4d}")
    return 0


def cmd_check(recipe_path: Path) -> int:
    """Every pixel outside the declared moving boxes must be identical in all frames."""
    recipe = load_recipe(recipe_path)
    gif = REPO_ROOT / recipe["gif"]
    if not gif.exists():
        raise SystemExit(f"missing {gif}")
    if "moving_boxes" not in recipe:
        raise SystemExit(f"{recipe_path} declares no moving_boxes; run build first")

    frames: list[np.ndarray] = []
    with Image.open(gif) as source:
        for index in range(getattr(source, "n_frames", 1)):
            source.seek(index)
            frames.append(np.asarray(source.convert("RGB"), dtype=np.uint8))
    if len(frames) != len(recipe["frames"]):
        raise SystemExit(f"{gif.name} holds {len(frames)} frames, recipe declares {len(recipe['frames'])}")

    height, width = frames[0].shape[:2]
    if (width, height) != tuple(recipe["output"]):
        raise SystemExit(f"{gif.name} is {width}x{height}, recipe declares {recipe['output']}")

    locked = np.ones((height, width), dtype=bool)
    for box in recipe["moving_boxes"]:
        locked[
            max(0, box["y"] - 1) : min(height, box["y"] + box["h"] + 1),
            max(0, box["x"] - 1) : min(width, box["x"] + box["w"] + 1),
        ] = False

    failures = 0
    for index, frame in enumerate(frames[1:], start=1):
        drift = (frame != frames[0]).any(axis=2) & locked
        if int(drift.sum()):
            ys, xs = np.where(drift)
            print(
                f"FAIL {gif.name} frame {index + 1}: {int(drift.sum())} locked pixels changed "
                f"(x {int(xs.min())}-{int(xs.max())}, y {int(ys.min())}-{int(ys.max())})"
            )
            failures += 1
    if failures:
        return 1
    print(
        f"OK {gif.name}: {len(frames)} frames, environment identical outside "
        f"{len(recipe['moving_boxes'])} declared moving boxes"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="composite frames, write the still, the GIF and the boxes")
    build.add_argument("--recipe", type=Path, required=True)
    build.add_argument("--layers", type=Path, default=Path("work/sp0007/layers"))
    build.add_argument("--no-write-back", action="store_true")
    check = sub.add_parser("check", help="verify a committed GIF against its recipe")
    check.add_argument("--recipe", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "build":
        return cmd_build(args.recipe, args.layers, write_back=not args.no_write_back)
    return cmd_check(args.recipe)


if __name__ == "__main__":
    sys.exit(main())
