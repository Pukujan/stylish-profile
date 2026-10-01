# Prompt record: Three Projects One Thread (motion)

- Asset: `assets/profile/anim/Three Projects One Thread.gif` (720x720, 4 frames, role `motion`)
- Dark asset: `Three Projects One Thread-dark.gif` — derived, not generated
- Provider: built-in image_gen (openrouter, `qwen/qwen-image-3`)
- Recorded: 2026-10-01

## Why this file exists

The section says one habit runs through all four tools. A still diagram states that; a
moving dot demonstrates it, because the thread is only interesting where something
travels along it.

## Format

GIF, three generated frames replayed in ping-pong order. Durations 1100, 800, 900, 800 ms.
See `AI Engineer motion.md` for why GIF and why ping-pong.

## Frames

Frame one is the committed still `assets/profile/Three Projects One Thread.png`.

1. **No dot.** Three cards joined by one blue thread, exactly as in the still.
2. **Dot at the left card.** Change prompt: *"A single small solid ink dot appears on the
   blue thread just to the right of the left-hand card, as if travelling along it. The
   camera is completely locked: the three cards, their icons, the thread, the title and
   the background stay in exactly the same pixel position."*
3. **Dot at the middle card.** Change prompt: *"The small dot has travelled further along
   the thread and now sits between the left and middle cards. The camera is completely
   locked: every other element stays in exactly the same pixel position."*

Prompt skeleton for every frame: flat hand-drawn vector illustration, thick uniform black
ink outlines, warm cream background, royal blue and warm yellow only, deliberately naive
sketchy linework, completely flat lighting with no gradients or shadows, and no text,
letters, numbers, captions, labels, signatures, watermarks, logos or wordmarks anywhere
beyond the title and subtitle already in the still.

## Result

A vision pass over the three frames confirmed the dot appears on the thread and advances
from the left card toward the middle, that everything else is identical, and that no
frame gained text, a logo or a wordmark.

Residual, accepted: a robot's antenna tilts slightly in the third frame. It is a few
pixels and reads as hand-drawn jitter rather than as a second moving subject, so it was
not re-rolled.

## Dark variant

`Three Projects One Thread-dark.gif` is a palette transform of the light GIF by
`scripts/derive_dark_assets.py`, not a generation.
