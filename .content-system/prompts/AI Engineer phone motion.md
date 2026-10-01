# Prompt record: AI Engineer phone (motion)

- Asset: `assets/profile/anim/AI Engineer phone.gif` (480x720, 4 frames, role `motion`)
- Dark asset: `AI Engineer phone-dark.gif` — derived, not generated
- Provider: built-in image_gen (openrouter, `qwen/qwen-image-3`)
- Recorded: 2026-10-01

## Why this file exists

The hero is a wide landscape frame. On a phone it would either shrink to an unreadable
strip or force the page to scroll sideways. A portrait render of the same scene is served
through a `picture` element below 640 pixels, so the hero keeps its weight on a small
screen.

## Format

GIF, three generated frames replayed in ping-pong order. Durations 1100, 800, 900, 800 ms.
See `AI Engineer motion.md` for why GIF and why ping-pong.

## Frames

Frame one is the committed still `assets/profile/AI Engineer phone.png`, which was itself
generated from `assets/profile/AI Engineer.png` as an input image so the characters,
palette and composition match the wide hero.

1. **Seated.** The block rests at the top of the structure, framed tall.
2. **Raised.** Change prompt: *"The engineer raises the block they are holding to head
   height, lifting it clear of the structure. The camera is completely locked: every other
   object stays in exactly the same pixel position, and the portrait framing is
   unchanged."*
3. **Lowered.** Change prompt: *"The engineer lowers the block from head height down to
   the bench, bringing it to rest against the front of the structure. The camera is
   completely locked: every other object stays in exactly the same pixel position."*

Prompt skeleton for every frame: flat hand-drawn vector illustration, thick uniform black
ink outlines, warm cream background, royal blue and warm yellow only, deliberately naive
sketchy linework, completely flat lighting with no gradients or shadows, and no text,
letters, numbers, captions, labels, signatures, watermarks, logos or wordmarks anywhere.

## Result

A vision pass confirmed the output is a genuine tall portrait frame, that the block is at
head height in the raised frame, that the whole illustration sits inside the frame with
nothing cropped at the edges, and that no frame carries a logo or a wordmark.

## Dark variant

`AI Engineer phone-dark.gif` is a palette transform of the light GIF by
`scripts/derive_dark_assets.py`, not a generation.
