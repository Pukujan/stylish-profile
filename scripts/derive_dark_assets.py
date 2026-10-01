"""Derive a dark-mode variant of a flat-palette illustration.

The illustrations on this page are flat vector-style renders: a small set of
saturated accents drawn with thick outlines on a cream field. On a dark page
that cream field reads as a lit rectangle, so the page needs a dark copy of
every picture.

Regenerating each picture through the image model for dark mode would cost a
model call per frame and would not be reproducible - two runs of the same
prompt do not return the same picture. The transform here is deterministic
instead: same input, same output, every time.

The rule has to answer one question per pixel: is this the field, the ink, or
an accent? Saturation alone is not enough to tell, because the "ink" in these
renders is not black - it is a dark navy, and a pale yellow accent has lower
saturation than that navy. So the decision uses both lightness and saturation:

- Light and unsaturated is the cream field. It inverts to the dark field.
- Dark, at any saturation, is ink. It inverts to light ink, keeping its hue, so
  the navy outlines become light blue lines instead of disappearing.
- Light and saturated is an accent. It is left alone, so yellow stays yellow
  rather than turning olive.

Inverting lightness alone would darken the yellow; keeping saturated colours
alone would leave the navy outlines invisible on black. Both are needed, and
both are blended smoothly rather than switched on a threshold, because the
renders are anti-aliased: an outline-to-field edge is a ramp of intermediate
tones, and a hard switch would put a visible band along every line.

The transform runs on numpy arrays. A per-pixel Python loop over a 1536x1024
render is slow enough to look like a hang, and a five-frame GIF multiplies that
by five.
"""

from __future__ import annotations

import argparse
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageSequence

# A pixel counts as the cream field when it is at least this light and at most
# this saturated. The cream measures lightness 0.96 at saturation 0.07, and the
# palest accent measures lightness 0.79 at saturation 0.33, so the two windows
# do not overlap.
FIELD_LIGHTNESS = (0.60, 0.85)
FIELD_SATURATION = (0.15, 0.35)

# A pixel counts as ink below this lightness, whatever its saturation. The navy
# outlines measure 0.26 and the accents measure 0.40 and up.
INK_LIGHTNESS = (0.35, 0.55)

# How much saturation the field keeps once it has inverted. The cream carries a
# faint warm cast; leaving it at full strength would make the dark field olive
# instead of neutral.
FIELD_SATURATION_KEPT = 0.15

# Endpoints of the grey ramp.
DARK_FIELD = 0.06
DARK_INK = 0.93


def _smoothstep(x: np.ndarray, low: float, high: float) -> np.ndarray:
    t = np.clip((x - low) / (high - low), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _rgb_to_hls(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maximum = rgb.max(axis=-1)
    minimum = rgb.min(axis=-1)
    delta = maximum - minimum

    lightness = (maximum + minimum) / 2.0
    with np.errstate(divide="ignore", invalid="ignore"):
        saturation = np.where(
            lightness > 0.5,
            delta / np.maximum(2.0 - maximum - minimum, 1e-9),
            delta / np.maximum(maximum + minimum, 1e-9),
        )
        saturation = np.where(delta < 1e-9, 0.0, saturation)

        safe = np.maximum(delta, 1e-9)
        hue = np.zeros_like(maximum)
        hue = np.where(maximum == red, ((green - blue) / safe) % 6.0, hue)
        hue = np.where(maximum == green, (blue - red) / safe + 2.0, hue)
        hue = np.where(maximum == blue, (red - green) / safe + 4.0, hue)
        hue = np.where(delta < 1e-9, 0.0, (hue / 6.0) % 1.0)

    return hue, lightness, saturation


def _hls_to_rgb(hue: np.ndarray, lightness: np.ndarray, saturation: np.ndarray) -> np.ndarray:
    def channel(t: np.ndarray) -> np.ndarray:
        t = t % 1.0
        return np.where(
            t < 1.0 / 6.0,
            p + (q - p) * 6.0 * t,
            np.where(
                t < 1.0 / 2.0,
                q,
                np.where(t < 2.0 / 3.0, p + (q - p) * (2.0 / 3.0 - t) * 6.0, p),
            ),
        )

    q = np.where(lightness < 0.5, lightness * (1.0 + saturation), lightness + saturation - lightness * saturation)
    p = 2.0 * lightness - q
    return np.stack([channel(hue + 1.0 / 3.0), channel(hue), channel(hue - 1.0 / 3.0)], axis=-1)


def darken_array(rgb: np.ndarray) -> np.ndarray:
    """Map an HxWx3 uint8 image onto the dark palette."""
    values = rgb.astype(np.float64) / 255.0
    hue, lightness, saturation = _rgb_to_hls(values)

    # HSV saturation, used only to tell the cream field from a pale accent.
    maximum = values.max(axis=-1)
    minimum = values.min(axis=-1)
    with np.errstate(divide="ignore", invalid="ignore"):
        vividness = np.where(maximum > 0, (maximum - minimum) / np.maximum(maximum, 1e-9), 0.0)

    field = _smoothstep(lightness, *FIELD_LIGHTNESS) * (
        1.0 - _smoothstep(vividness, *FIELD_SATURATION)
    )
    ink = 1.0 - _smoothstep(lightness, *INK_LIGHTNESS)
    invert = np.maximum(field, ink)

    # Invert lightness around the midpoint, so the cream lands on the dark field
    # and the navy ink lands on the light ink.
    new_lightness = lightness + invert * (1.0 - 2.0 * lightness)
    # The field loses its warm cast; ink keeps its hue at full strength.
    new_saturation = saturation * (1.0 - field * (1.0 - FIELD_SATURATION_KEPT))

    result = _hls_to_rgb(hue, new_lightness, new_saturation)
    return np.clip(np.rint(result * 255.0), 0, 255).astype(np.uint8)


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
        if not args.check:
            parser.error("at least one source is required")
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
