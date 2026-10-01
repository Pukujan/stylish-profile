# Prompt record: Reusable Blocks (five-frame animation)

Generated with the built-in image generation tool (`built-in image_gen`,
provider `openrouter`, model `qwen/qwen-image-3`). The published file is
`assets/profile/anim/Reusable Blocks.gif`, 720x720, five frames, role `motion`.

## Why this file exists

The page claims that the work is about building a component once and reusing it
everywhere. A still frame cannot show "once, then everywhere". This animation
can: one block, then two, then three, then a full grid, with the original block
turning warm yellow to mark which one the rest were copied from.

## Format

GIF, because that is what GitHub animates in a README. A probe of GitHub's own
markdown renderer on 2026-10-01 showed a `.gif` image receiving the
`data-animated-image` attribute while `.apng`, `.png`, `.webp` and `.jpg` did
not, so APNG would have displayed as a single static frame.

## Frames

Frame one was generated from a written prompt; frames two through five were
produced by passing the previous frame back in as an input image with one
change each, which is what keeps the drawing identical between frames.

1. One blue block alone on a cream page, above a black baseline rule.
2. Duplicate the block once to the right: two blocks.
3. Add one more: three blocks in a row.
4. Add a second row of three: a two-by-three grid of six.
5. Recolour only the top-left block to warm yellow: the source the others came
   from.

Prompt skeleton for every frame: flat hand-drawn vector illustration, thick
uniform black ink outlines, warm cream (#FFF9F0) background, royal blue
(#4169E1) and warm yellow (#FFD93D) only, deliberately naive sketchy linework,
completely flat lighting with no gradients or shadows, and no text, letters,
numbers, captions, labels, signatures, watermarks, logos or wordmarks anywhere.

## Result

Assembled with Pillow at 720x720, 64 colours on one shared palette, frame
durations 650 ms with a 1800 ms hold on the final frame, looping forever.

Vision checks read one block in frame one, two in frame two, three in frame
three, six in frame four, and six with a single yellow block in frame five,
with no text or logo in any frame.
