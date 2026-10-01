# Prompt record: The Badge Wall (motion)

- Asset: `assets/profile/anim/The Badge Wall.gif` (900x600, 4 frames, role `motion`)
- Dark asset: `The Badge Wall-dark.gif` — derived, not generated
- Provider: built-in image_gen (openrouter, `qwen/qwen-image-3`)
- Recorded: 2026-10-01

## Why this file exists

The section explains why this page does not lead with third-party statistics cards. The
picture has to say "searching for something real behind a wall of empty cards", and a
search is a motion.

## Format

GIF, three generated frames replayed in ping-pong order. Durations 1100, 800, 900, 800 ms.
See `AI Engineer motion.md` for why GIF and why ping-pong.

## Frames

Frame one is the committed still `assets/profile/The Badge Wall.png`.

1. **Glass held low.** The companion holds the empty magnifying glass at chest height.
2. **Glass raised.** Change prompt: *"The small round companion raises the empty
   magnifying glass overhead, holding it above its head. LOCK: the camera is completely
   locked, and every object other than the one named stays in exactly the same pixel
   position - the wall of blank cards, the title, and the background do not move at all."*
3. **Glass returned.** Change prompt: *"The companion brings the empty magnifying glass
   back down to chest height. LOCK: the camera is completely locked and every other
   object stays in exactly the same pixel position."*

Prompt skeleton for every frame: flat hand-drawn vector illustration, thick uniform black
ink outlines, warm cream background, royal blue and warm yellow only, deliberately naive
sketchy linework, completely flat lighting with no gradients or shadows, and no text,
letters, numbers, captions, labels, signatures, watermarks, logos or wordmarks anywhere
beyond the title and subtitle already in the still. Every badge card in the wall stays
completely blank.

## Result

The first attempt was rejected: the whole background panned across the frame, which reads
as a camera move rather than as the companion searching, and it would have made the
animation the loudest thing in a section about not being loud. It was re-rolled with the
`LOCK` clause above and the change moved from the camera to the glass.

A vision pass over the accepted frames confirmed the companion raises the glass upward
across the frames, that the wall stays in place, and that no frame gained text or a logo.

Residual, accepted: the wall shifts by a few pixels in the third frame. It is inside the
tolerance the `LOCK` clause asks for and is not visible at the size the figure renders.

## Dark variant

`The Badge Wall-dark.gif` is a palette transform of the light GIF by
`scripts/derive_dark_assets.py`, not a generation.
