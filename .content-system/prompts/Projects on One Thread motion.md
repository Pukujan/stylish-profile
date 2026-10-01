# Prompt record: Projects on One Thread (motion)

- Asset: `assets/profile/anim/Projects on One Thread.gif` (720x720, 6 frames, role `motion`)
- Dark asset: `Projects on One Thread-dark.gif` — derived, not generated
- Provider: built-in image_gen for the layers; compositing by `scripts/build_locked_motion.py`
- Recorded: 2026-10-01

## Why this file exists

The figure beside the project list shows the habit the four tools share moving
along one thread. Under #24 it was rebuilt from layers for the same reason as
the hero: the previous GIF had been re-rolled frame from frame, so the cards,
the thread and the lettering all warped, and the owner's screenshots showed a
broken and doubled line.

## The recipe

`scripts/motion-recipes/figure.json`. The four icons are **static** layers:
pasted identically into each frame, and deliberately left out of the declared
moving boxes, so the lock check covers them too and a rebuild that let an icon
drift would fail. The only moving layer is the dot, which travels the width of
the plate in six steps, visiting the four card centres.

The dot does not ride a straight line. Its y per frame is the thread's measured
centre line at that x (`work/sp0007/probe-figure.py` on the accepted plate), so
it follows the thread's actual wobble. Durations are 200 ms per frame; the dot
exits right as the next loop enters left, so the wrap is seamless.

## Result

All six frames are byte-identical outside the dot's swept band, which covers
5.7% of the frame — the strongest lock of any figure on the page. Verified by
`scripts/build_locked_motion.py check` and by the same gate in CI. A vision pass
over the frame sheet confirms the dot advancing along the thread with the cards,
icons and lettering unmoved.

## Dark variant

`Projects on One Thread-dark.gif` is a palette transform of the light GIF by
`scripts/derive_dark_assets.py`, byte-stable and re-checked in CI.
