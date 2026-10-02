# TASK-SP-0008 — Hero Redraw and Page Lead

<!-- continuity:task {"acceptance": ["a new hero still at 1536x1024 and a new phone hero still at 1024x1536 are generated with the new image model, both spelling the title and subtitle exactly and carrying no other text", "a vision pass over the new light and dark hero frames finds no malformed glyph, no broken connecting line, no floating element, no light halo tracing a silhouette, and no ragged title outline", "both hero locked-motion GIFs pass scripts/build_locked_motion.py check outside their declared moving boxes", "the dark-variant transform no longer repaints a figure's own outline as light ink, and scripts/derive_dark_assets.py --check passes on every committed variant after the change", "the first screen of profile/README.md runs hero image, a short introduction naming the featured project, the market, what Pujan does about it, the daily commits, the projects, then everything else", "docs/index.html carries the same order and the same opening claims", "no sentence in the reordered opening explains pinning, checks, gating or fail-closed behaviour, and those facts still appear further down the page", "every existing gate stays green: check_profile_links, generate_voice_notes --check, the pinned CGM adapter validator, the hsw writing scans, and continuity validate"], "depends_on": [], "goal": "Redraw the hero with the new image model so it holds up in dark mode, and lead the page with the hero, a short featured-project introduction, the market, the fix and the daily commits before the projects", "id": "SP-0008", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/27", "next_action": "generate the new wide hero plate with the new image model and review it against the vision checklist", "owner": "omp@windows-workstation", "priority": "P1", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "active", "why": "The owner rejected the shipped hero a second time: it carries drawing faults and its dark variant traces a light halo around every silhouette, because the paper-mask transform repaints a figure's own outline as light ink. The page also buries its story, opening on an audit-flavoured explanation of version pinning instead of the market, the fix and the fresh activity"} -->

- Status: active
- Owner: omp@windows-workstation
- Priority: P1
- Depends on: none

## Goal

Redraw the hero with the new image model so it holds up in dark mode, and lead the page with the hero, a short featured-project introduction, the market, the fix and the daily commits before the projects.

## Why

The owner rejected the shipped hero a second time. The drawing carries faults a vision pass can name — pegboard tools that look painted on, a robot whose feet do not meet the floor, sketchy double lines on the table legs — and its dark variant is worse: a jagged light halo traces the engineer, the glassware and the bench tools, and the title carries a ragged light outline. The halo comes from `scripts/derive_dark_assets.py`, which repaints every ink pixel within 8 pixels of the paper as light ink, so a figure's own outline turns cream against the dark field.

The page has a second problem. It opens on an audit-flavoured explanation of version pinning, and the freshest thing on it — the daily commit chart — sits near the bottom under `What's fresh`. The owner wants the voice to run hero image, a short introduction naming the featured project, the market, what Pujan is doing about it, the daily commits, the projects, then everything else.

## Allowed files

- PROJECT.md
- profile/README.md
- docs/index.html
- docs/CONTINUITY_INDEX.md
- .content-system/**
- .continuity/**
- .github/workflows/gates.yml
- assets/profile/**
- scripts/derive_dark_assets.py
- scripts/build_locked_motion.py
- scripts/build_motion_gif.py
- scripts/motion-recipes/**
- scripts/track_activity.py
- tasks/**
- checkpoints/**

## Human outcome

A visitor meets a hero drawing that holds up in both themes, and a first screen that says what Pujan does, who it is for and why it matters now, before it explains any mechanism.

## Scope and boundaries

- In scope: the hero still, the phone hero still, both locked-motion GIFs, both derived dark variants; the dark-variant transform where it produces the halo and the gate that checks it; the section order and opening copy of `profile/README.md` and `docs/index.html`; the records that describe all of it.
- Out of scope: the other eight illustrations and their animations; re-recording the voice notes (two still say `three tools` against a page listing four, which needs a paid Fish Audio run and the owner's approval); the page's links, palette and audio-player behaviour; the tracker's data; any market claim that is not an observation or grounded in the owner's own repositories.

## Acceptance criteria

- [ ] a new hero still at 1536x1024 and a new phone hero still at 1024x1536 are generated with the new image model, both spelling the title and subtitle exactly and carrying no other text
- [ ] a vision pass over the new light and dark hero frames finds no malformed glyph, no broken connecting line, no floating element, no light halo tracing a silhouette, and no ragged title outline
- [ ] both hero locked-motion GIFs pass `scripts/build_locked_motion.py check` outside their declared moving boxes
- [ ] the dark-variant transform no longer repaints a figure's own outline as light ink, and `scripts/derive_dark_assets.py --check` passes on every committed variant after the change
- [ ] the first screen of `profile/README.md` runs hero image, a short introduction naming the featured project, the market, what Pujan does about it, the daily commits, the projects, then everything else
- [ ] `docs/index.html` carries the same order and the same opening claims
- [ ] no sentence in the reordered opening explains pinning, checks, gating or fail-closed behaviour, and those facts still appear further down the page
- [ ] every existing gate stays green: `check_profile_links`, `generate_voice_notes --check`, the pinned CGM adapter validator, the hsw writing scans, and `continuity validate`

## Evidence and sources

Recorded on branch `task/SP-0008-hero-redraw-and-page-lead`.

| Command | Result |
| --- | --- |
| `python scripts/build_locked_motion.py check --recipe scripts/motion-recipes/hero-wide.json` | `OK AI Engineer.gif: 6 frames, environment identical outside 5 declared moving boxes` |
| `python scripts/build_locked_motion.py check --recipe scripts/motion-recipes/hero-phone.json` | `OK AI Engineer phone.gif: 6 frames, environment identical outside 5 declared moving boxes` |
| `python scripts/build_locked_motion.py check --recipe scripts/motion-recipes/projects-on-one-thread.json` | `OK Projects on One Thread.gif: 6 frames, environment identical outside 1 declared moving boxes` |
| `python scripts/derive_dark_assets.py && python scripts/derive_dark_assets.py --check` | `VALID: 8 dark variant(s) match their source` |
| `python scripts/check_profile_links.py` | `VALID: 33 local reference(s) resolved, 36 recorded hash(es) matched` |
| `python scripts/generate_voice_notes.py --check` | `checked 9 clip(s), 0 problem(s)` |
| pinned CGM `validate_content_system.py --adapter .content-system` | `VALID: content-generation-modules contract and target adapter` |
| pinned CGM `verify_hsw_applied.py --root <cgm>` | `VALID: HSW always-on contract OK` |
| pinned CGM `verify_hsw_applied.py --mode acs-html --html docs/index.html` | `VALID: HSW always-on contract OK and HTML tell scan clean` |
| `continuity docs render` then `continuity validate --root .` | `VALID` |

Halo measurement, before and after, on the committed hero frame: the old rule
`result[ink & binary_dilation(paper, iterations=8)] = PAPER_INK` lightened
2.40% of the frame; the new rule paints only the page's own marks, and a 6x
zoom on Projects on One Thread, The Badge Wall and Pujan and the Loose Ends
shows the old rule's "white outlines" were that artifact.

Source-unchanged frame flips (pixels identical in the light source but
differing in the dark output), measured on all eight committed light GIFs
against both transforms:

| Asset | HEAD transform | current transform |
| --- | --- | --- |
| AI Engineer phone | 89 | 80 |
| AI Engineer | 47 | 5 |
| One Push Many Pipelines | 22,380 | 21,094 |
| Projects on One Thread | 55 | 0 |
| Pujan and the Loose Ends | 1,782 | 271 |
| Reusable Blocks | 6,956 | 0 |
| The Badge Wall | 4,151 | 1,775 |
| What You Can Check | 1,063 | 923 |
| **Total** | **36,523** | **24,148** |

The residual is a pre-existing defect, not a regression: HEAD's `_paper_mask`
was already border-connected per frame, so the shipped One Push dark GIF
flickers too. It is filed separately. Two fixes were measured and rejected —
freezing the page to the intersection of every frame's candidate reaches 0
flips but costs 21-100% of the page area on six of eight assets; morphological
opening does not move the mask differences at all, because they are sprites
moving rather than leaks.

## Related records

- Owning issue: https://github.com/Pukujan/stylish-profile/issues/27. Leaf; parent ancestry: none. Supersedes the hero accepted under #24 / PR #25 without reopening it.
- Primary writer: omp@windows-workstation, branch `task/SP-0008-hero-redraw-and-page-lead`.
- Related PR/CI evidence: pending.

## Checkpoint log

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
