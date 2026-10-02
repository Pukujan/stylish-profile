# Prompt record — AI Engineer phone (hero, portrait)

- **Asset:** `assets/profile/AI Engineer phone.png`
- **Role:** hero phone (portrait, 1024x1536)
- **Provider:** `xai-oauth/grok-imagine-image` (the configured image-model role)
- **Recorded:** 2026-10-01
- **Exact title:** `AI Engineer`
- **Exact subtitle:** `Reusable components, automated pipelines`

## Why this asset exists

The same hero rebuilt for the narrow screen the page serves below 640 pixels.
It is frame one of `assets/profile/anim/AI Engineer phone.gif`, composited by
`scripts/build_locked_motion.py` from its own portrait environment plate plus
the same keyed character sprites the wide hero uses. The title and subtitle are
kept exactly as the wide hero declares them; #24's boundaries say the hero's
declared copy does not change. Issue #27 is the redraw, with the new image
model and a rebuilt dark transform.

## Layers

The portrait plate (`plate-tall-c.png` → `plate-tall-01.png`, 1024x1536)
recomposes the wide scene for a tall frame: the title very large across the
upper third, the subtitle beneath it, and the bench with its glassware and
conveyor filling the lower half, with the middle left as open cream so the
engineer can stand there, and a single unbroken ground line at y=1318 of 1536.
The engineer, robot and burst sprites are the same files the wide hero uses,
re-fitted to a larger body height for the portrait. The layer prompts are
recorded in `AI Engineer.md`.

This is the third portrait plate generated. The first two were rejected on
review: the second (`plate-tall-b.png`) put its ground line at y=1004 of 1536,
leaving a dead cream bottom third with nothing in it.

## Review decision

Accepted 2026-10-01 under #27. Redrawn from scratch with
`xai-oauth/grok-imagine-image`, and recomposed for the narrow framing so the
ground line sits above a dead bottom third. A vision pass confirms the portrait
framing, the same engineer and robots, the feet on the ground line, and no text
beyond the declared title and subtitle.

## Verification

- Dimensions 1024x1536, mode RGB, no alpha channel.
- SHA-256 of the committed file:
  `393fd7e264deada792b2d3f6f4ebd4f49c4765b5bdb33bf2e10c315e41853174`
- Recipe `scripts/motion-recipes/hero-phone.json`.
