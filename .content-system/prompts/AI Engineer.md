# Prompt record — AI Engineer (hero)

- **Asset:** `assets/profile/AI Engineer.png`
- **Role:** hero (wide, 1536x1024)
- **Provider:** built-in image_gen
- **Recorded:** 2026-10-01
- **Exact title:** `AI Engineer`
- **Exact subtitle:** `Reusable components, automated pipelines`

## Why this asset exists

The page opens on the claim it is about: an engineer who automates repetitive
work. Issue #24 rejected the previous hero on two counts — the whole picture
warped from frame to frame, and the drawing itself was not worth keeping. The
owner asked for a new direction: a cool anime-style engineer with thick
outlines, mid-experiment, with a comic explosion and robots running.

This still is frame one of the rebuilt animation. It is not drawn as one
picture. It is composited by `scripts/build_locked_motion.py` from one locked
environment plate plus keyed character sprites, so the animation can move the
characters without the environment drifting. The plate carries the title, the
subtitle and the whole workshop; the engineer, the robots and the burst are
separate sprites pasted on top.
## Layers and how they were prompted

The five layers were generated in an earlier session whose exact prompt text was
not recorded, so the wording below is *reconstructed* from the accepted output
and the #24 direction, not a verbatim transcript. The figure record
`Projects on One Thread.md` shows the prompt style that was actually used for
the layers generated this session.

**Environment plate** (`plate-wide-01.png`, 1536x1024): a flat hand-drawn wide
workshop scene with no characters in it — a long yellow workbench of glassware,
round-bottom flasks, a book, gears and a small device, a pegboard of simple
unlabelled tools on the back wall, a faint blueprint grid, and a conveyor belt
at the right; the title `AI Engineer` set large in royal blue in the upper left
and the subtitle `Reusable components, automated pipelines` beneath it in warm
yellow, with no other text. Flat hand-drawn vector, thick ink outlines, palette
of royal blue #4169E1, warm yellow #FFD93D, orange and ink #1A1A1A on cream
#FFF9F0, no gradients, no photorealism, no 3D, no people, no robots.

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

Accepted 2026-10-01 after the #24 rebuild. A vision pass confirms the anime
engineer, the raised flask, the comic burst and the running robots, with the
title and subtitle spelled exactly and no other text. The two engineer poses
are fitted to a common body height and pinned at the feet and ground-centre, so
only the arm moves between them.

## Verification

- Dimensions 1536x1024, mode RGB, no alpha channel.
- SHA-256 of the committed file:
  `71279d49050e02df496c061b1a715ed92be4f30305b1c8471f89f02d9e8640b0`
- The recipe that composites it is `scripts/motion-recipes/hero-wide.json`;
  `scripts/build_locked_motion.py check` proves the committed GIF's frames are
  identical outside the recipe's declared moving boxes.
