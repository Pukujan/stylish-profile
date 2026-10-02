# Prompt record: AI Engineer (motion)

- Asset: `assets/profile/anim/AI Engineer.gif` (900x600, 6 frames, role `motion`)
- Phone asset: `assets/profile/anim/AI Engineer phone.gif` (480x720, 6 frames)
- Dark assets: `AI Engineer-dark.gif`, `AI Engineer phone-dark.gif` — derived, not generated
- Provider: `xai-oauth/grok-imagine-image` (the configured image-model role) for the layers; compositing by `scripts/build_locked_motion.py`
- Recorded: 2026-10-01

## Why this file exists

Issue #24 rejected the hero before it because the whole picture warped from
frame to frame: the frames had each been re-rolled from the last by the image
model, which ignored the "camera completely locked" instruction. The fix is
structural rather than a better prompt. The environment is one generated plate
that is copied, never re-drawn, and only the characters are moved.

Issue #27 is the second redraw. The owner rejected the #24 hero on the drawing
itself, and its dark variant carried a light halo around every silhouette. Both
the plate and the sprites were regenerated with the new image model, and the
dark transform was rebuilt; see `AI Engineer.md` for the layer prompts and the
two rejected plates.

## Format

GIF, because a probe of GitHub's markdown renderer on 2026-10-01 showed a
`.gif` image receiving the `data-animated-image` attribute while `.apng`
displayed as a single frozen frame. Six composited frames, durations 240 ms
each with a 360 ms hold on the last, so the loop breathes rather than rattles.

The loop is seamless by construction: the travelling robots start off-frame at
the left and end off-frame at the right, and the comic burst is hidden in both
the first and the last frame, so frame six returning to frame one shows no
snap.

## The recipe

`scripts/motion-recipes/hero-wide.json` names the plate, the sprites, the output
size and the six frames as lists of placements. Each placement gives a sprite,
the plate point its anchor lands on, and optionally a per-frame size for the
burst. The builder measures each keyed sprite once — its ink bbox, its feet row,
its shoulder row and its ground-centre — and uses those to scale and place it,
so the two engineer poses share one body height and one ground point.

Per frame the engineer alternates the idle and raised poses, the two robots
advance along the floor at different depths, and the burst pops once: hidden,
small, full, medium, small, hidden.

The sprite `size` is 380. The #24 recipes used 460, which was sized to the old
sprites' body boxes; the regenerated poses measure taller, so 460 would have
made the engineer overflow the bench. At `fit: "body"` the idle pose scales by
380/799 and the raised pose by 380/906, giving body boxes of 205x487 and
215x484 — close enough that the two poses read as one character.

## Why the environment cannot drift

Every frame is built from the same resampled plate; the sprites are resampled
to output resolution before compositing, so a plate pixel that touches a sprite
edge never mixes with the sprite's pixels. The recipe records the union of the
placed sprite footprints as `moving_boxes`, and
`scripts/build_locked_motion.py check` compares the committed GIF's frames
outside those boxes and fails on any difference. The same check runs in CI as
the `Animation environments stay locked` gate.

## Result

All six frames are byte-identical outside the declared moving boxes, which
cover 19.4% of the frame. A vision pass over the frame sheet confirms the feet
on the ground line in every frame, the engineer at one size and one x-position
across both poses, the flask raised every other frame, the burst popping once
per loop, and the robots entering and exiting off-frame.

## Dark variant

`AI Engineer-dark.gif` is not generated. It is a palette transform of the light
GIF by `scripts/derive_dark_assets.py`, so it is byte-stable and re-runs with
the tracker rather than costing a model call per frame.

The transform no longer repaints a figure's own outline. The previous rule
recoloured every ink pixel within 8 pixels of the paper, which drew a light
halo along the engineer, the glassware and the bench tools; the current rule
recolours only the page's own marks — ink the drawing encloses, or ink almost
entirely ringed by paper — so a silhouette outline is left alone.
