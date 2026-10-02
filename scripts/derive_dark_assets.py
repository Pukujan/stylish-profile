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

The paper is found once for the whole loop rather than once per frame. The
border-connected pass answers a question about the frame it is run on, and that
answer moves between frames even where the drawing does not. Two things move
it, and the first is much the larger: a sprite crossing a region changes which
pixels are ink, so a region that reached the frame edge in one frame can be
sealed off in the next. The page colour also drifts between frames in the
source light GIF itself, which is what stops a byte-exact repair from following
the first effect. A pixel is paper if the border-connected pass calls it paper
in this frame, or in another frame where its colour is within
PAPER_MATCH_TOLERANCE of this frame's.

One thing does have to change. Text and rules are drawn straight onto the
paper, so leaving them alone would put black text on a dark field. Ink that
sits on the paper is redrawn in light ink, while ink that belongs to the
drawing keeps its own colour.

"On the paper" cannot be decided by distance alone. The first version of this
transform asked whether an ink pixel sat within eight pixels of the paper, and
that lightened the character's own outline wherever the character stood near
the field - a light fringe tracing every silhouette, which is the pale band
that ran along every contour of the shipped dark illustrations.

Two tests agree on what is instead drawn on the paper, and either one is
enough. The first is enclosure: an ink component whose interior encloses
almost nothing is drawn on the paper, while the drawing itself encloses
thousands of pixels. Measured across all eight pictures, the components this
test accepts enclose at most 117 px and the smallest it rejects encloses
125 px, while the drawing itself encloses up to 55,771 px. Enclosure alone
is not enough, because a diagram drawn on the paper - the line, dot and square
of a timeline - can enclose a large area and still be a mark. The second test
is surround: the drawing's contour is traced by its own fill, so only a
quarter of it has paper within a couple of pixels, while a diagram drawn on
the paper is next to paper along its whole length. Measured across all eight
pictures, the components that test accepts reach 0.700 and the highest a
rejected one reaches is 0.698, while the drawing's own contour never passes
0.680. That is where PAGE_MARK_RING sits.

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
# Eight pixels clears the title strokes in a 900 px wide render. On its own
# this is not enough - it traces a light fringe along every contour of the
# drawing - which is why a component has to pass one of the two tests in
# _page_mark_mask before any of its ink is lightened.
PAPER_INK_REACH = 8

# The enclosed area, as a fraction of the frame, below which an ink component
# is text drawn on the paper rather than the drawing itself. Measured across
# the eight pictures, the components this test accepts enclose at most 117 px
# and the smallest it rejects encloses 125 px, so the cut sits in the thinnest
# part of the two clusters rather than in a wide gap - which is why the ring
# test below exists and either one is enough. The drawing itself encloses up to
# 55,771 px.
PAGE_MARK_FRACTION = 2.37e-4

# The fraction of an ink component's immediate surroundings that has to be
# paper before the component counts as a diagram drawn on the page. Measured
# across all eight illustrations, every component at or above 0.70 is a mark
# and the highest one below it reaches 0.698, while the drawing's own contour
# never passes 0.680. The cut is narrow, and it is why enclosure is kept as the
# other half of the test rather than replaced by this.
PAGE_MARK_RING = 0.70

# How far out those surroundings are measured. Two pixels clears the
# anti-aliased edge of a stroke without reaching the fill inside a contour.
PAGE_MARK_RING_RADIUS = 2

# How far apart two frames' colours at the same pixel may be and still count
# as the page agreeing with itself.
#
# The page colour is not constant across a loop. It drifts a level or two
# between frames in the source light GIF itself, before this transform runs,
# and the border-connected pass can then answer differently in each frame. On
# One Push Many Pipelines the interiors of the three boxes are the page colour
# exactly, and they drift two levels at frame 2, which is enough to make the
# pass call them page in one frame and not in the next. This tolerance is the
# smallest value that darkens all three interiors in every frame; at zero the
# first box stays cream in frames 0 and 1, which is the cream trail the fix is
# meant to remove.
#
# Drift is the smaller of the two reasons the answer moves. The larger one is
# that a sprite crossing a region changes which pixels are ink, so a region
# that reached the frame edge in one frame is sealed off in the next while the
# source bytes at the pixel do not change at all. The tolerance cannot repair
# that on its own, but it does not have to: at a byte-identical pixel the two
# frames' colours are equal, so the test passes trivially and the union carries
# the answer across. The tolerance matters for the pixels where the source
# itself moved.
#
# Two is also far from everything that is not page, which is why it is safe
# rather than merely sufficient. The nearest light thing that is not page is
# the grey the small robot in AI Engineer is drawn in, fifteen levels away, and
# Pujan's drawer white is twelve. The construction never reaches a pixel the
# border-connected pass has not already called page in some frame, so a drawn
# object can only be darkened where some frame's pass was already wrong about
# it - which is the shipped behaviour this transform inherits and stabilises,
# not a new hole.
#
# This is not a test for "is this pixel paper", and it is not asked to be one.
# The skin, the bench face and the pegboard are the page colour exactly, so no
# tolerance separates them from it. The tolerance decides whether the page has
# moved, not what the page is.
PAPER_MATCH_TOLERANCE = 2

_NEIGHBOURS = np.ones((3, 3), dtype=bool)


def _candidate_mask(rgb: np.ndarray) -> np.ndarray:
    """Every light, barely coloured pixel, wherever it sits.

    This is the raw colour test behind :func:`_paper_mask`. It catches the
    character's skin and the paper alike, because the two are the same cream,
    so on its own it is not a background test. It is still the right mask for
    asking what a region is made of, as opposed to where it connects to.
    """
    values = rgb.astype(np.float64) / 255.0
    maximum = values.max(axis=-1)
    minimum = values.min(axis=-1)
    lightness = (maximum + minimum) / 2.0
    with np.errstate(divide="ignore", invalid="ignore"):
        saturation = np.where(
            maximum > 0, (maximum - minimum) / np.maximum(maximum, 1e-9), 0.0
        )
    return (lightness > PAPER_LIGHTNESS) & (saturation < PAPER_SATURATION)

def _paper_mask(rgb: np.ndarray) -> np.ndarray:
    """The light, barely coloured region that reaches the edge of the frame.

    The connected-component pass is the point of this function. A plain "light
    and unsaturated" test also catches the character's skin, because the skin
    and the paper are the same cream, and darkening the skin is the bug this
    whole rewrite exists to fix. Only the region touching the border is paper.
    """
    candidate = _candidate_mask(rgb)
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


def _page_mark_mask(
    rgb: np.ndarray, paper: np.ndarray, ink: np.ndarray
) -> np.ndarray:
    """Ink drawn on the paper rather than part of the drawing.

    Distance alone cannot make this call - an eight pixel reach lightened the
    character's own outline wherever the character stood near the field, which
    is the pale fringe that ran along every contour of the shipped dark
    illustrations. Two tests make it instead, and either one is enough.

    Enclosure: the largest page-coloured area inside a title component is a
    few dozen pixels, while the drawing itself encloses thousands. The
    candidate mask is the right thing to measure against, because the areas
    enclosed by the drawing are exactly the ones the border-connected paper
    mask misses.

    Surround: a diagram drawn on the paper can enclose a large area and still
    be a mark, but its outline has paper alongside it for its whole length,
    while the drawing's contour is traced by its own fill.
    """
    height, width = rgb.shape[:2]
    labels, count = ndimage.label(ink, structure=_NEIGHBOURS)
    sizes = np.bincount(labels.ravel(), minlength=count + 1)
    sizes[0] = 0

    surrounded = np.zeros(count + 1, dtype=bool)
    for index in range(1, count + 1):
        if not sizes[index]:
            continue
        component = labels == index
        ring = (
            ndimage.binary_dilation(component, iterations=PAGE_MARK_RING_RADIUS)
            & ~component
        )
        ring_size = int(ring.sum())
        if ring_size and int((ring & paper).sum()) / ring_size >= PAGE_MARK_RING:
            surrounded[index] = True
    on_paper = np.isin(labels, np.where(surrounded)[0])

    filled = ndimage.binary_fill_holes(ink)
    owners, owner_count = ndimage.label(filled, structure=_NEIGHBOURS)
    enclosed = filled & ~ink & _candidate_mask(rgb)
    biggest = np.zeros(owner_count + 1, dtype=np.int64)
    if enclosed.any():
        inner, inner_count = ndimage.label(enclosed, structure=_NEIGHBOURS)
        inner_sizes = np.bincount(inner.ravel(), minlength=inner_count + 1)
        owner = np.asarray(
            ndimage.maximum(owners, inner, index=np.arange(1, inner_count + 1)),
            dtype=int,
        )
        np.maximum.at(biggest, owner, inner_sizes[1:])

    limit = max(1, int(round(PAGE_MARK_FRACTION * height * width)))
    on_paper |= np.isin(owners, np.where(biggest < limit)[0])
    return ink & ndimage.binary_dilation(paper, iterations=PAPER_INK_REACH) & on_paper

def _scene(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The masks an illustration is classified by, before anything is drawn."""
    return _paper_mask(rgb), _ink_mask(rgb)

def darken_array(
    rgb: np.ndarray,
    paper: np.ndarray | None = None,
    marks: np.ndarray | None = None,
) -> np.ndarray:
    """Map an HxWx3 uint8 illustration onto the dark page.

    Both masks are optional so a caller can supply the ones a loop agreed on
    rather than the ones this frame derives on its own; :func:`loop_scene` is
    the caller that does.
    """
    detected_paper, ink = _scene(rgb)
    if paper is None:
        paper = detected_paper
    if marks is None:
        marks = _page_mark_mask(rgb, detected_paper, ink)
    result = rgb.copy()
    result[paper] = np.array(PANEL, dtype=rgb.dtype)
    result[marks] = np.array(PAPER_INK, dtype=rgb.dtype)
    return result


def darken_frame(
    frame: Image.Image,
    paper: np.ndarray | None = None,
    marks: np.ndarray | None = None,
) -> Image.Image:
    return Image.fromarray(
        darken_array(np.asarray(frame.convert("RGB")), paper=paper, marks=marks)
    )

def loop_scene(
    arrays: list[np.ndarray],
) -> tuple[list[np.ndarray], np.ndarray]:
    """The masks a whole loop is drawn with, rather than one set per frame.

    The page mask is a border-connected pass, and the pass answers a question
    about the frame it runs on. That answer moves between frames even where the
    drawing does not, for two reasons. A sprite crossing a region changes which
    pixels are ink, so a region that reached the frame edge in one frame is
    sealed off in the next; that is the larger effect. The page colour also
    drifts a level or two between frames in the source light GIF itself. Either
    way the pixel can be unchanged in the source while the output blinks
    between the dark page and the cream mark colour, and no check in this
    repository can catch it, because every check re-derives each frame the same
    way.

    So a pixel counts as page here if the border-connected pass calls it page
    in this frame, or if it holds nearly the same colour as a frame in which
    that pass does. PAPER_MATCH_TOLERANCE gates that second clause. It never
    reaches a pixel the pass has not already called page somewhere, which is
    why the skin, the bench face and the pegboard - all of them the page colour
    exactly, and none of them ever border-connected - are still excluded by
    connectivity and not by colour.

    The marks mask is taken from the first frame, because it is a size test: a
    sprite crossing a region can cut it in two and push both halves under the
    enclosure threshold.
    """
    papers = [_paper_mask(array) for array in arrays]
    marks = _page_mark_mask(arrays[0], papers[0], _ink_mask(arrays[0]))
    integers = [array.astype(np.int16) for array in arrays]
    pages = []
    for index, array in enumerate(arrays):
        page = papers[index].copy()
        for other in range(len(arrays)):
            if other == index:
                continue
            near = np.abs(integers[index] - integers[other]).max(axis=-1)
            page |= papers[other] & (near <= PAPER_MATCH_TOLERANCE)
        pages.append(page & _candidate_mask(array))
    return pages, marks


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
            arrays, durations = [], []
            for frame in ImageSequence.Iterator(image):
                arrays.append(np.asarray(frame.convert("RGB")))
                durations.append(frame.info.get("duration", 100))
            papers, marks = loop_scene(arrays)
            frames = [
                Image.fromarray(darken_array(array, paper=paper, marks=marks))
                for array, paper in zip(arrays, papers)
            ]
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
