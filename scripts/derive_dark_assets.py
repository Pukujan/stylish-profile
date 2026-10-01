"""Derive a dark-mode variant of a flat-palette illustration.

The illustrations on this page are flat vector-style renders: a small set of
saturated accents drawn with thick outlines on a cream field. On a dark page
that cream field reads as a lit rectangle, so the page needs a dark copy of
every picture.

Regenerating each picture through the image model for dark mode would cost a
model call per frame and would not be reproducible - two runs of the same
prompt do not return the same picture. The transform here is deterministic
instead: same input, same output, every time.

An earlier version of this script inverted every pixel's lightness: cream went
to black, black went to white, accents stayed put. That is the obvious
transform, and it produced bad pictures. The character's skin is the same cream
as the field, so it inverted to black and the face became a hole. The hair is
near black, so it inverted to white. The figure came out as a photographic
negative, and the pictures were worse in dark mode than in light.

What the page needs is the paper to go dark while the drawing on it stays
itself. So the transform finds the paper - the light, barely coloured region
that reaches the edge of the frame - and replaces only that. Everything the
drawing put on top keeps its colour, which is what keeps skin skin and hair
hair.

One thing does have to change. Text and rules are drawn straight onto the
paper, so leaving them alone would put black text on a dark field. Ink that
sits within a few pixels of the paper is redrawn in light ink, while ink
enclosed by the drawing keeps its own colour. That distance is what separates
the title from the character's outline, and it is the only tuned number here.

The transform runs on numpy arrays. A per-pixel Python loop over a 900x600
render is slow enough to look like a hang, and a five-frame GIF multiplies that
by five. Finding the paper needs a connected-component pass, which is why scipy
is a dependency.
"""

from __future__ import annotations

import argparse
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageSequence
from scipy import ndimage

# Paper is light and barely coloured. The cream field measures lightness 0.96 at
# saturation 0.03, and the palest accent - the peach - measures 0.85 at 0.37, so
# these thresholds separate the two.
PAPER_LIGHTNESS = 0.72
PAPER_SATURATION = 0.30

# Ink is anything this dark, whatever its colour. The navy outlines measure 0.26
# and the black screens measure 0.00, while the darkest accent sits at 0.40.
INK_LIGHTNESS = 0.55

# The dark field. Warm rather than neutral, so the picture still looks like it
# was drawn on paper, and light enough to separate from the page behind it:
# GitHub's dark background is #0d1117 and this page's is #0f0f0f, so a field of
# pure black would leave the illustration with no edge at all.
PANEL = (26, 22, 18)

# Ink that sits on the paper comes back as light ink. Slightly lighter than the
# cream the field was, so small text holds up.
PAPER_INK = (250, 246, 236)

# How far from the paper an ink pixel may sit and still count as drawn on it.
# Eight pixels clears the title strokes in a 900 px wide render without reaching
# the character, whose outline sits further in.
PAPER_INK_REACH = 8


def _paper_mask(rgb: np.ndarray) -> np.ndarray:
    """The light, barely coloured region that reaches the edge of the frame.

    The connected-component pass is the point of this function. A plain "light
    and unsaturated" test also catches the character's skin, because the skin
    and the paper are the same cream, and darkening the skin is the bug this
    whole rewrite exists to fix. Only the region touching the border is paper.
    """
    values = rgb.astype(np.float64) / 255.0
    maximum = values.max(axis=-1)
    minimum = values.min(axis=-1)
    lightness = (maximum + minimum) / 2.0
    with np.errstate(divide="ignore", invalid="ignore"):
        saturation = np.where(
            maximum > 0, (maximum - minimum) / np.maximum(maximum, 1e-9), 0.0
        )

    candidate = (lightness > PAPER_LIGHTNESS) & (saturation < PAPER_SATURATION)
    labels, _ = ndimage.label(
        candidate, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    )
    touching = (
        set(labels[0, :])
        | set(labels[-1, :])
        | set(labels[:, 0])
        | set(labels[:, -1])
    )
    touching.discard(0)
    if not touching:
        return np.zeros(candidate.shape, dtype=bool)
    return np.isin(labels, list(touching))


def _ink_mask(rgb: np.ndarray) -> np.ndarray:
    values = rgb.astype(np.float64) / 255.0
    lightness = (values.max(axis=-1) + values.min(axis=-1)) / 2.0
    return lightness < INK_LIGHTNESS


def darken_array(rgb: np.ndarray) -> np.ndarray:
    """Map an HxWx3 uint8 illustration onto the dark page."""
    paper = _paper_mask(rgb)
    result = rgb.copy()
    result[paper] = np.array(PANEL, dtype=rgb.dtype)

    on_paper = _ink_mask(rgb) & ndimage.binary_dilation(
        paper, iterations=PAPER_INK_REACH
    )
    result[on_paper] = np.array(PAPER_INK, dtype=rgb.dtype)
    return result


def darken_frame(frame: Image.Image) -> Image.Image:
    return Image.fromarray(darken_array(np.asarray(frame.convert("RGB"))))


def convert(source: Path, destination: Path | BytesIO) -> None:
    if isinstance(destination, Path):
        destination.parent.mkdir(parents=True, exist_ok=True)
    # Pillow infers the format from the destination name, which a buffer does
    # not have, so name it explicitly.
    image_format = {"gif": "GIF", "png": "PNG"}.get(source.suffix.lstrip(".").lower())
    if image_format is None:
        raise SystemExit(f"unsupported source type: {source.name}")
    with Image.open(source) as image:
        if getattr(image, "is_animated", False):
            frames, durations = [], []
            for frame in ImageSequence.Iterator(image):
                frames.append(darken_frame(frame))
                durations.append(frame.info.get("duration", 100))
            # One shared colour table for the whole loop, for the same reason the
            # light GIFs use one: independent per-frame quantisation makes flat
            # colours shimmer between frames.
            reference = frames[0].quantize(colors=64, method=Image.MEDIANCUT)
            prepared = [frame.quantize(palette=reference, dither=Image.NONE) for frame in frames]
            prepared[0].save(
                destination,
                format=image_format,
                save_all=True,
                append_images=prepared[1:],
                duration=durations,
                loop=0,
                optimize=False,
                disposal=2,
            )
        else:
            darken_frame(image).save(destination, format=image_format)
    if isinstance(destination, Path):
        print(f"{source.name} -> {destination.name}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sources", nargs="*", type=Path)
    parser.add_argument("--suffix", default="-dark")
    parser.add_argument(
        "--check",
        action="store_true",
        help="re-derive each source and fail if the committed variant differs",
    )
    parser.add_argument(
        "--into",
        type=Path,
        help="write into this directory instead of beside each source",
    )
    args = parser.parse_args(argv)

    if not args.sources:
        anim = Path(__file__).resolve().parents[1] / "assets" / "profile" / "anim"
        args.sources = sorted(
            path for path in anim.glob("*.gif") if not path.stem.endswith(args.suffix)
        )
        if not args.sources:
            raise SystemExit(f"no light illustrations found under {anim}")

    if args.check:
        return check(args.sources, args.suffix)

    for source in args.sources:
        if not source.is_file():
            raise SystemExit(f"missing source: {source}")
        if args.into:
            destination = args.into / f"{source.stem}{args.suffix}{source.suffix}"
        else:
            destination = source.with_name(f"{source.stem}{args.suffix}{source.suffix}")
        convert(source, destination)
    return 0


def check(sources: list[Path], suffix: str) -> int:
    """Fail when a committed dark variant no longer matches its light source.

    The derivation is deterministic, so re-deriving and comparing bytes is a
    real test rather than a smoke test. Without it a regenerated illustration
    leaves its dark copy behind silently, and the only way to notice would be
    to look at the page in dark mode and spot one wrong picture among nine.
    """
    problems: list[str] = []
    for source in sources:
        if not source.is_file():
            problems.append(f"missing source: {source}")
            continue
        destination = source.with_name(f"{source.stem}{suffix}{source.suffix}")
        if not destination.is_file():
            problems.append(f"{destination.name} is missing")
            continue
        buffer = BytesIO()
        convert(source, buffer)
        if buffer.getvalue() != destination.read_bytes():
            problems.append(f"{destination.name} does not match {source.name}")

    if problems:
        print(f"INVALID: {len(problems)} dark variant(s) out of date")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"VALID: {len(sources)} dark variant(s) match their source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
