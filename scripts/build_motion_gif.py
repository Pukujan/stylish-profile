"""Assemble a small loop of generated frames into a GIF.

The illustrations on this page are flat vector-style renders, so a short loop
reads as motion without needing many frames. Frames are chained at generation
time (each frame is rendered from the previous one with a single recorded
change), so by the time they arrive here they already share their geometry and
palette; this script only has to keep them sharing a colour table.

Two details matter for the result:

- A single palette is built from one frame and forced onto all of them. Letting
  Pillow quantize each frame independently makes flat colours shimmer between
  frames, which is the most visible artefact in a short loop.
- The frame order is a ping-pong by default. A three-frame loop that jumps
  straight from the last frame back to the first reads as a snap; playing the
  middle frame again on the way back makes the same frames read as a swing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

PALETTE_COLORS = 64


def parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = (int(part) for part in value.lower().split("x"))
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected WIDTHxHEIGHT, got {value!r}") from None
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError(f"expected positive dimensions, got {value!r}")
    return width, height


def parse_durations(value: str) -> list[int]:
    try:
        durations = [int(part) for part in value.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected comma-separated milliseconds, got {value!r}") from None
    if not durations or any(d <= 0 for d in durations):
        raise argparse.ArgumentTypeError(f"expected positive durations, got {value!r}")
    return durations


def ping_pong(frames: list[Image.Image]) -> list[Image.Image]:
    """Play the frames forwards then backwards, without repeating the ends."""
    if len(frames) < 3:
        return frames
    return frames + frames[-2:0:-1]


def load_frames(paths: list[Path], size: tuple[int, int]) -> list[Image.Image]:
    frames = []
    for path in paths:
        if not path.is_file():
            raise SystemExit(f"missing frame: {path}")
        with Image.open(path) as image:
            frames.append(image.convert("RGB").resize(size, Image.LANCZOS))
    return frames


def quantize(frames: list[Image.Image]) -> list[Image.Image]:
    reference = frames[-1].quantize(colors=PALETTE_COLORS, method=Image.MEDIANCUT)
    return [frame.quantize(palette=reference, dither=Image.NONE) for frame in frames]


def build(
    frame_paths: list[Path],
    output: Path,
    size: tuple[int, int],
    durations: list[int],
    loop: bool,
) -> None:
    frames = load_frames(frame_paths, size)
    if loop:
        frames = ping_pong(frames)
    if len(durations) not in (1, len(frames)):
        raise SystemExit(
            f"got {len(durations)} durations for {len(frames)} frames; "
            "supply one value or one per frame"
        )
    if len(durations) == 1:
        durations = durations * len(frames)

    output.parent.mkdir(parents=True, exist_ok=True)
    prepared = quantize(frames)
    prepared[0].save(
        output,
        save_all=True,
        append_images=prepared[1:],
        duration=durations,
        loop=0,
        optimize=False,
        disposal=2,
    )
    print(f"wrote {output} ({len(frames)} frames, {size[0]}x{size[1]})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--frames", nargs="+", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--size", required=True, type=parse_size)
    parser.add_argument("--durations", default="700", type=parse_durations)
    parser.add_argument(
        "--no-loop",
        action="store_true",
        help="keep the given frame order instead of playing it back and forth",
    )
    args = parser.parse_args(argv)

    build(args.frames, args.output, args.size, args.durations, loop=not args.no_loop)
    return 0


if __name__ == "__main__":
    sys.exit(main())
