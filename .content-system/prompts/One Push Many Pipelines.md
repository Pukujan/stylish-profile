# Prompt record: One Push Many Pipelines (five-frame animation)

Generated with the built-in image generation tool (`built-in image_gen`,
provider `openrouter`, model `qwen/qwen-image-3`). The published file is
`assets/profile/anim/One Push Many Pipelines.gif`, 720x720, five frames, role
`motion`.

## Why this file exists

The second half of the claim is that one action should drive several outputs
without anyone repeating the steps by hand. This animation shows a single dot
travelling down a stem, the stem forking, and every box at the end of a fork
filling in: one push, several finished results.

## Format

GIF, for the same reason as `Reusable Blocks.gif`: a probe of GitHub's own
markdown renderer on 2026-10-01 showed `.gif` getting `data-animated-image`
while `.apng` did not.

## Frames

Frame one was generated from a written prompt; frames two through five were
produced by passing the previous frame back in as an input image with one
change each.

1. One black dot at the top of a short vertical stem, one empty outlined box at
   the bottom.
2. The dot slides a third of the way down the stem.
3. The stem forks into two branches, each ending in an empty box, the dot at
   the fork.
4. A third branch appears, the dot still at the fork.
5. The dot reaches the bottom and all three boxes fill solid royal blue.

Prompt skeleton for every frame: flat hand-drawn vector illustration, thick
uniform black ink outlines, warm cream (#FFF9F0) background, black and royal
blue (#4169E1) only, naive sketchy linework, completely flat lighting, and no
text, letters, numbers, captions, labels, signatures, watermarks, logos or
wordmarks anywhere.

## Result

Assembled with Pillow at 720x720, 64 colours on one shared palette, frame
durations 650 ms with a 1800 ms hold on the final frame, looping forever.

Vision checks read one dot and one empty box in frame one, three filled blue
boxes in frame five, and no text or logo in any frame.
