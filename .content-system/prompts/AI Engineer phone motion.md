# Prompt record: AI Engineer phone (motion)

- Asset: `assets/profile/anim/AI Engineer phone.gif` (480x720, 6 frames, role `motion`)
- Dark asset: `AI Engineer phone-dark.gif` — derived, not generated
- Provider: `xai-oauth/grok-imagine-image` (the configured image-model role) for the layers; compositing by `scripts/build_locked_motion.py`
- Recorded: 2026-10-01

## Why this file exists

The portrait hero the page serves below 640 pixels, rebuilt under #24 with the
same locked-plate method as the wide hero, and redrawn under #27 with the new
image model. The framing is different — the engineer stands larger in the open
middle band of the tall plate, the robots run along the bottom, and the burst
pops beside the flask at the left — but the cast and the declared title and
subtitle are the wide hero's.

## The recipe

`scripts/motion-recipes/hero-phone.json`. Six composited frames, durations 240
ms with a 360 ms hold on the last; the robots travel off-frame at both ends and
the burst is hidden in the first and last frame, so the loop is seamless. The
moving boxes cover 14.9% of the frame. The sprite `size` is 380, matched to the
wide recipe so the two framings show the same character at the same scale.

## Result

All six frames are byte-identical outside the declared moving boxes, verified
by `scripts/build_locked_motion.py check` and by the same gate in CI. A vision
pass over the frame sheet confirms the portrait framing, the feet on the ground
line, the raised flask every other frame, and no text beyond the plate's own
title and subtitle.

## Dark variant

`AI Engineer phone-dark.gif` is a palette transform of the light GIF by
`scripts/derive_dark_assets.py`, byte-stable and re-checked in CI. It carries
the rebuilt transform, so the engineer's own outline is no longer repainted as
light ink and the silhouette halo is gone.
