# Prompt record: What You Can Check (motion)

- Asset: `assets/profile/anim/What You Can Check.gif` (480x720, 4 frames, role `motion`)
- Dark asset: `What You Can Check-dark.gif` — derived, not generated
- Provider: built-in image_gen (openrouter, `qwen/qwen-image-3`)
- Recorded: 2026-10-01

## Why this file exists

The section lists what a reader can verify. The picture shows a source card leaving a
stack and landing on the open book, which is the act of checking a claim rather than a
picture of a claim.

## Format

GIF, three generated frames replayed in ping-pong order. Durations 1100, 800, 900, 800 ms.
See `AI Engineer motion.md` for why GIF and why ping-pong.

## Frames

Frame one is the committed still `assets/profile/What You Can Check.png`.

1. **Card on the stack.** The stack of blank source cards sits above the open book.
2. **Card in flight.** Change prompt: *"One blank card leaves the bottom of the stack and
   is caught mid-air, tilted, between the stack and the open book. The camera is
   completely locked: the stack, the book, the headphones, the small round companion and
   the background stay in exactly the same pixel position, and every card stays blank with
   no writing on it."*
3. **Card landed.** Change prompt: *"The card has landed flat on the open book, and the
   remaining stack sits one card shorter. The camera is completely locked: every other
   object stays in exactly the same pixel position."*

Prompt skeleton for every frame: flat hand-drawn vector illustration, thick uniform black
ink outlines, warm cream background, royal blue and warm yellow only, deliberately naive
sketchy linework, completely flat lighting with no gradients or shadows, and no text,
letters, numbers, captions, labels, signatures, watermarks, logos or wordmarks anywhere
beyond the title and subtitle already in the still. Every source card stays completely
blank.

## Result

A vision pass over the three frames confirmed one card leaves the stack and lands on the
book, that everything else is identical, and that no frame gained text, a logo or a
wordmark.

## Dark variant

`What You Can Check-dark.gif` is a palette transform of the light GIF by
`scripts/derive_dark_assets.py`, not a generation.
