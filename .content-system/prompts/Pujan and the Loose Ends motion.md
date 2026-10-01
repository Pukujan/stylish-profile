# Prompt record: Pujan and the Loose Ends (motion)

- Asset: `assets/profile/anim/Pujan and the Loose Ends.gif` (900x600, 4 frames, role `motion`)
- Dark asset: `Pujan and the Loose Ends-dark.gif` — derived, not generated
- Provider: built-in image_gen (openrouter, `qwen/qwen-image-3`)
- Recorded: 2026-10-01

## Why this file exists

The picture stands in for the story the voice notes tell: a desk, three trays, and a pile
of sheets that has not been filed yet. A sheet arriving in a tray is the whole point of
the tooling, so the still had to move.

## Format

GIF, three generated frames replayed in ping-pong order. Durations 1100, 800, 900, 800 ms.
See `AI Engineer motion.md` for why GIF and why ping-pong.

## Frames

Frame one is the committed still `assets/profile/Pujan and the Loose Ends.png`.

1. **Middle tray occupied.** All three trays hold sheets.
2. **Tray emptied.** Change prompt: *"Empty the middle tray completely, leaving it bare.
   The camera is completely locked: the person, the desk, the left and right trays, the
   swirl of loose papers, the small round companion and the background stay in exactly the
   same pixel position."*
3. **Sheet landed.** Change prompt: *"A single blank sheet of paper has landed flat in the
   middle tray, which now holds exactly one sheet. The camera is completely locked: every
   other object stays in exactly the same pixel position."*

Prompt skeleton for every frame: flat hand-drawn vector illustration, thick uniform black
ink outlines, warm cream background, royal blue and warm yellow only, deliberately naive
sketchy linework, completely flat lighting with no gradients or shadows, and no text,
letters, numbers, captions, labels, signatures, watermarks, logos or wordmarks anywhere
beyond the title and subtitle already in the still. Every sheet of paper stays completely
blank.

## Result

The first attempt was rejected: nothing measurable moved in the trays, so the three frames
were effectively the same picture three times. Emptying the tray in frame two and landing
the sheet in frame three gives the sequence a readable state change, and it also matches
what the tooling actually does — clear the slot, then file one item into it.

A vision pass over the accepted frames confirmed the middle tray is empty in frame two and
holds a single sheet in frame three, and that no frame gained text or a logo.

Residual, accepted: the person's posture and the companion's speech bubble change slightly
between frames. The bubble stays empty, so no copy is invented, and the posture change is
small enough to read as hand-drawn jitter.

## Dark variant

`Pujan and the Loose Ends-dark.gif` is a palette transform of the light GIF by
`scripts/derive_dark_assets.py`, not a generation.
