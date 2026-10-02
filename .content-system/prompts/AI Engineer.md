# Prompt record — AI Engineer (hero)

- **Asset:** `assets/profile/AI Engineer.png`
- **Role:** hero (wide, 1536x1024)
- **Provider:** `xai-oauth/grok-imagine-image` (the configured image-model role)
- **Recorded:** 2026-10-01
- **Exact title:** `AI Engineer`
- **Exact subtitle:** `Reusable components, automated pipelines`

## Why this asset exists

The page opens on the claim it is about: an engineer who automates repetitive
work. Issue #24 accepted a hero that the owner then rejected a second time.
The drawing carried faults a vision pass could name — pegboard tools that read
as painted on, a robot whose feet did not meet the floor, sketchy double lines
on the table legs — and the dark variant was worse than the light one: a jagged
light halo traced the engineer, the glassware and the bench tools, and the
title carried a ragged light outline. Issue #27 is the redraw, with the new
image model and a rebuilt dark transform.

This still is frame one of the rebuilt animation. It is not drawn as one
picture. It is composited by `scripts/build_locked_motion.py` from one locked
environment plate plus keyed character sprites, so the animation can move the
characters without the environment drifting. The plate carries the title, the
subtitle and the whole workshop; the engineer, the robots and the burst are
separate sprites pasted on top.

## Layers and how they were prompted

Every layer was generated this session with the configured image-model role,
`xai-oauth/grok-imagine-image`, and each was reviewed before use. The model
returns 2496x1664 for a 1536x1024 3:2 request, so each plate is downscaled to
the plate resolution the recipe declares.

**Environment plate** (`plate-wide-c.png` → `plate-wide-01.png`, 1536x1024):
a flat hand-drawn wide workshop scene with no characters in it — a long yellow
workbench of glassware, round-bottom flasks, a book, gears and a small device,
a pegboard of simple unlabelled tools on the back wall, a faint blueprint grid,
and a conveyor belt at the right; a single unbroken ground line across the
width; the title `AI Engineer` set large in royal blue in the upper left and
the subtitle `Reusable components, automated pipelines` beneath it in warm
yellow, with no other text. Flat hand-drawn vector, thick ink outlines, palette
of royal blue #4169E1, warm yellow #FFD93D, orange and ink #1A1A1A on cream
#FFF9F0, no gradients, no photorealism, no 3D, no people, no robots.

This is the third plate generated. The first two were rejected on review: the
second (`plate-wide-b.png`) had no ground line at all, so every sprite floated
above the floor once composited.

**Character sprites**, each drawn alone on a flat cream field so the builder can
key the paper out and paste it onto the plate:

- **Engineer, idle** (`guy-02.png`): an anime-style young engineer, spiky dark
  hair, goggles pushed up on the forehead, white lab coat over orange overalls,
  holding a round flask of glowing yellow liquid at chest height.
- **Engineer, raised** (`guy-raise-01.png`): the same character raising the
  flask overhead, the other hand on the hip.
- **Robot** (`robot-01.png`): a small round white-bodied robot with a blue
  screen face, running hard with arms flailing.
- **Burst** (`boom-01.png`): a comic orange-and-yellow explosion with a dark
  outline and a few sparks.

All four share the clause that made keying possible: one single subject centred
on a completely flat solid cream `#FFF9F0` background with generous empty
margin, thick uniform ink outlines, no text, no shadow.

## Review decision

Accepted 2026-10-01 under #27. Redrawn from scratch with
`xai-oauth/grok-imagine-image` after the owner rejected the #24 hero a second
time. A vision pass over every generated sprite found no malformed glyph, no
broken line and no floating part, and a pass over the rebuilt frames confirms
the feet meet the ground line, the engineer holds one size and one x-position
across both poses, and the title is never occluded. The two engineer poses are
fitted to a common body height and pinned at the feet and ground-centre, so only
the arm moves between them.

## Verification

- Dimensions 1536x1024, mode RGB, no alpha channel.
- SHA-256 of the committed file:
  `f6580ae8d47065528c049eac514aba4ecdf7e926c7e7f94076875f8f11a365d0`
- The recipe that composites it is `scripts/motion-recipes/hero-wide.json`;
  `scripts/build_locked_motion.py check` proves the committed GIF's frames are
  identical outside the recipe's declared moving boxes.
- Keying was checked before compositing: `scripts/build_locked_motion.paper_key`
  keys every sprite cleanly, and no sprite contains an enclosed transparent
  hole, so the white lab coat's interior survives.
