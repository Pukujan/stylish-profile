# Prompt record — AI Engineer phone (hero, portrait)

- **Asset:** `assets/profile/AI Engineer phone.png`
- **Role:** hero phone (portrait, 1024x1536)
- **Provider:** built-in image_gen
- **Recorded:** 2026-10-01
- **Exact title:** `AI Engineer`
- **Exact subtitle:** `Reusable components, automated pipelines`

## Why this asset exists

The same hero rebuilt for the narrow screen the page serves below 640 pixels.
It is frame one of `assets/profile/anim/AI Engineer phone.gif`, composited by
`scripts/build_locked_motion.py` from its own portrait environment plate plus
the same keyed character sprites the wide hero uses. The title and subtitle are
kept exactly as the wide hero declares them; #24's boundaries say the hero's
declared copy does not change.

## Layers

The portrait plate (`plate-tall-01.png`, 1024x1536) recomposes the wide scene
for a tall frame: the title very large across the upper third, the subtitle
beneath it, and the bench with its glassware and conveyor filling the lower
half, with the middle left as open cream so the engineer can stand there. The
engineer, robot and burst sprites are the same files the wide hero uses,
re-fitted to a larger body height for the portrait. The layer prompts and their
reconstruction caveat are recorded in `AI Engineer.md`.

## Review decision

Accepted 2026-10-01 after the #24 rebuild. A vision pass confirms the portrait
framing, the same engineer and robots, the title large enough to read at a 390
pixel column, and no text beyond the declared title and subtitle.

## Verification

- Dimensions 1024x1536, mode RGB, no alpha channel.
- SHA-256 of the committed file:
  `90a30b5f93ca2beb3f9decd5acbd358b6859a0d7c91ec4de0467b46351ff39ec`
- Recipe `scripts/motion-recipes/hero-phone.json`.
