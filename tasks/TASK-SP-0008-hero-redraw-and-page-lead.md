# TASK-SP-0008 — Hero Redraw and Page Lead

<!-- continuity:task {"acceptance": ["a new hero still at 1536x1024 and a new phone hero still at 1024x1536 are generated with the new image model, both spelling the title and subtitle exactly and carrying no other text", "a vision pass over the new light and dark hero frames finds no malformed glyph, no broken connecting line, no floating element, no light halo tracing a silhouette, and no ragged title outline", "both hero locked-motion GIFs pass scripts/build_locked_motion.py check outside their declared moving boxes", "the dark-variant transform no longer repaints a figure's own outline as light ink, and scripts/derive_dark_assets.py --check passes on every committed variant after the change", "the first screen of profile/README.md runs hero image, a short introduction naming the featured project, the market, what Pujan does about it, the daily commits, the projects, then everything else", "docs/index.html carries the same order and the same opening claims", "no sentence in the reordered opening explains pinning, checks, gating or fail-closed behaviour, and those facts still appear further down the page", "every existing gate stays green: check_profile_links, generate_voice_notes --check, the pinned CGM adapter validator, the hsw writing scans, and continuity validate"], "depends_on": [], "goal": "Redraw the hero with the new image model so it holds up in dark mode, and lead the page with the hero, a short featured-project introduction, the market, the fix and the daily commits before the projects", "id": "SP-0008", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/27", "next_action": "none; SP-0008 is merged as 14338d2 and its close-out is recorded. The residual dark-GIF flash is filed as #28.", "owner": "omp@windows-workstation", "priority": "P1", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "completed", "why": "The owner rejected the shipped hero a second time: it carries drawing faults and its dark variant traces a light halo around every silhouette, because the paper-mask transform repaints a figure's own outline as light ink. The page also buries its story, opening on an audit-flavoured explanation of version pinning instead of the market, the fix and the fresh activity"} -->

- Status: completed
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
flickers too. It is filed as #28 with the same numbers. Two fixes were measured
and rejected —
freezing the page to the intersection of every frame's candidate reaches 0
flips but costs 21-100% of the page area on six of eight assets; morphological
opening does not move the mask differences at all, because they are sprites
moving rather than leaks.

## Related records

- Owning issue: https://github.com/Pukujan/stylish-profile/issues/27. Leaf; parent ancestry: none. Supersedes the hero accepted under #24 / PR #25 without reopening it.
- Primary writer: omp@windows-workstation, branch `task/SP-0008-hero-redraw-and-page-lead`.
- Related PR/CI evidence: pull request #29, `https://github.com/Pukujan/stylish-profile/pull/29`. Every step of the required `gates` job passed on `49e7af7`, the exact merge candidate. Squash merge `14338d22ffcf229650303868ab7500ac0a069f87` on `main`, verified by fetching `origin/main` and confirming the merge commit is an ancestor.
- Delivery note: the first candidate, `c96852d`, failed `gates` on a stale `docs/CONTINUITY_INDEX.md` — the index had been rendered before the task projection and `checkpoints/CURRENT.md` were written, so the runner saw a hash for `PROJECT.md` that no longer matched. Re-rendered and pushed as `49e7af7`; auto-merge then landed the green run. No product file changed in that fix.
- Follow-up filed from this task: #28, the residual flash in the derived dark GIFs, which predates this task and is reduced but not removed by it.
- Leaf receipt for the close-out increment, request `9df782a29413487d90c89449415a8108`: https://github.com/Pukujan/stylish-profile/issues/27#issuecomment-5943631954 — names both the checkpoint commit `993f8e9` and the repair `d01d5b5`.
- Gate-running notes for the next session, including the `--blocked ""` trap, the render-before-push ordering and the pinned-versions requirement for the byte-comparison check: `README.md`, section "Running the gates locally".

## Checkpoint log

### 2026-10-02 00:49:12 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":["scripts/derive_dark_assets.py, scripts/motion-recipes/hero-wide.json, scripts/motion-recipes/hero-phone.json, assets/profile/AI Engineer.png, assets/profile/AI Engineer phone.png, assets/profile/anim/AI Engineer.gif, assets/profile/anim/AI Engineer phone.gif, the eight derived dark GIFs, profile/README.md, docs/index.html, .content-system/asset-manifest.json, the four hero prompt records, PROJECT.md, tasks/TASK-SP-0008-hero-redraw-and-page-lead.md, checkpoints/CURRENT.md"],"completed":["Redrew the wide and phone hero from scratch with the configured image model, rebuilt the dark transform so it no longer repaints a figure's own outline as light ink, and reordered the profile page and the tour page to hero, introduction, market, the fix, the daily commits, the featured projects, then the rest."],"decisions":["Kept the per-frame border-connected paper mask and shipped the transform measured strictly better than the shipped one, rather than the frozen page construction that reaches zero flash but costs 21-100% of the page area on six of eight assets."],"evidence":["build_locked_motion check passes on hero-wide, hero-phone and projects-on-one-thread; derive_dark_assets --check reports 8 dark variants matching their source; check_profile_links reports 33 references resolved and 36 hashes matched; generate_voice_notes --check reports 9 clips and 0 problems; the pinned CGM adapter validator and both hsw scans pass; continuity validate is VALID. Flash measurement on all eight dark GIFs: 36,523 source-unchanged pixels under the old transform, 24,148 under the new one."],"next_action":"Push the branch, open the pull request against main, arm auto-merge, verify the merge and the required checks, then append the exact check results and merge SHA to issue #27 and the task projection.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0008","timestamp":"2026-10-02T00:49:12Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"498ea73793ebcd9f5af2bcdfcb99f8467ff4178909083d9448cbc8ca4e8872c8","request_id":"76ccddfe2a364fa2b829d4ea4d40e4f6","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0008"} -->

Completed:
- Redrew the wide and phone hero from scratch with the configured image model, rebuilt the dark transform so it no longer repaints a figure's own outline as light ink, and reordered the profile page and the tour page to hero, introduction, market, the fix, the daily commits, the featured projects, then the rest.

Evidence:
- build_locked_motion check passes on hero-wide, hero-phone and projects-on-one-thread; derive_dark_assets --check reports 8 dark variants matching their source; check_profile_links reports 33 references resolved and 36 hashes matched; generate_voice_notes --check reports 9 clips and 0 problems; the pinned CGM adapter validator and both hsw scans pass; continuity validate is VALID. Flash measurement on all eight dark GIFs: 36,523 source-unchanged pixels under the old transform, 24,148 under the new one.

Decisions:
- Kept the per-frame border-connected paper mask and shipped the transform measured strictly better than the shipped one, rather than the frozen page construction that reaches zero flash but costs 21-100% of the page area on six of eight assets.

Changed:
- scripts/derive_dark_assets.py, scripts/motion-recipes/hero-wide.json, scripts/motion-recipes/hero-phone.json, assets/profile/AI Engineer.png, assets/profile/AI Engineer phone.png, assets/profile/anim/AI Engineer.gif, assets/profile/anim/AI Engineer phone.gif, the eight derived dark GIFs, profile/README.md, docs/index.html, .content-system/asset-manifest.json, the four hero prompt records, PROJECT.md, tasks/TASK-SP-0008-hero-redraw-and-page-lead.md, checkpoints/CURRENT.md

Blocked/uncertain:
- none

Next:
- Push the branch, open the pull request against main, arm auto-merge, verify the merge and the required checks, then append the exact check results and merge SHA to issue #27 and the task projection.

### 2026-10-02 00:53:15 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":["tasks/TASK-SP-0008-hero-redraw-and-page-lead.md, checkpoints/CURRENT.md, docs/CONTINUITY_INDEX.md"],"completed":["Closed SP-0008 out: pull request #29 merged to main as 14338d2 with every step of the required gates job green on the merge candidate, and the task and checkpoint projections now record the merge."],"decisions":["Recorded the merge as a separate synchronized increment rather than amending the merged history, and left the pre-existing dark-GIF flash with #28 rather than fixing it inside this task."],"evidence":["gates job on 49e7af7: continuity records validate, content adapter conformance, always-on writing contract, tour page writing scan, profile links resolve, voice notes match their record, dark variants match their source and animation environments stay locked, all success. continuity validate is VALID after the close-out render. origin/main fetched and the merge commit confirmed an ancestor. Local runs under the CI pins agree on 33 references, 36 hashes, 9 clips, 8 dark variants and the three locked-motion recipes."],"next_action":"Pick up #28: find a page mask for scripts/derive_dark_assets.py that stops the dark GIFs flashing without shrinking the page area, and measure flashing pixels and page area together before touching any committed asset.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0008","timestamp":"2026-10-02T00:53:15Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256": "ef8cab3a509b3cee495a985adfab903638aab2e86dfa0323090833394fbfcddc", "request_id": "9df782a29413487d90c89449415a8108", "schema": "project-continuity.checkpoint-operation.v1", "task_id": "SP-0008"} -->

Completed:
- Closed SP-0008 out: pull request #29 merged to main as 14338d2 with every step of the required gates job green on the merge candidate, and the task and checkpoint projections now record the merge.

Evidence:
- gates job on 49e7af7: continuity records validate, content adapter conformance, always-on writing contract, tour page writing scan, profile links resolve, voice notes match their record, dark variants match their source and animation environments stay locked, all success. continuity validate is VALID after the close-out render. origin/main fetched and the merge commit confirmed an ancestor. Local runs under the CI pins agree on 33 references, 36 hashes, 9 clips, 8 dark variants and the three locked-motion recipes.

Decisions:
- Recorded the merge as a separate synchronized increment rather than amending the merged history, and left the pre-existing dark-GIF flash with #28 rather than fixing it inside this task.

Changed:
- tasks/TASK-SP-0008-hero-redraw-and-page-lead.md, checkpoints/CURRENT.md, docs/CONTINUITY_INDEX.md

Blocked/uncertain:
- none

Next:
- Pick up #28: find a page mask for scripts/derive_dark_assets.py that stops the dark GIFs flashing without shrinking the page area, and measure flashing pixels and page area together before touching any committed asset.

### 2026-10-02 01:06:21 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":["README.md, .content-system/asset-manifest.json, docs/CONTINUITY_INDEX.md, tasks/TASK-SP-0008-hero-redraw-and-page-lead.md"],"completed":["Corrected the phone hero's framing record to the measurement and wrote the local gate-running rules into the README, then published the missing close-out receipt on issue #27."],"decisions":["Corrected the manifest wording rather than re-placing the phone sprites, because the measured 14 percent margin is inside the 13.9 to 17.8 percent band the whole page already uses, so there was no dead third to fix. Put the gate-ordering rules in the README's gate section rather than only in the task handoff, because the next session reads the README before it reads a finished task."],"evidence":["Last drawn row on the committed phone still is 1321 of 1536, a 14 percent bottom margin, against 841 of 1024 on the wide hero, measured directly from the PNGs. Local gates under the CI pins: check_profile_links 34 references and 36 hashes, generate_voice_notes 9 clips 0 problems, derive_dark_assets 8 variants matching, build_locked_motion check OK on all three recipes, pinned adapter validator VALID, both hsw scans VALID, continuity validate VALID. Receipt for request 9df782a29413487d90c89449415a8108 posted to issue #27 as comment 5943631954, naming 993f8e9 and the d01d5b5 repair. Post-merge gates run 36948611156 on main at e1049db: success. Both merged SP-0008 branches deleted, local and remote."],"next_action":"Pick up #28: find a page mask for scripts/derive_dark_assets.py that stops the dark GIFs flashing without shrinking the page area, and measure flashing pixels and page area together before touching any committed asset.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0008","timestamp":"2026-10-02T01:06:21Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"2bc7081dff333ee6ab00d48962b2b85ae5738884fc85ab328b6127118ea0c602","request_id":"f8084b17565b40feb0d4887ad9fdce9c","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0008"} -->

Completed:
- Corrected the phone hero's framing record to the measurement and wrote the local gate-running rules into the README, then published the missing close-out receipt on issue #27.

Evidence:
- Last drawn row on the committed phone still is 1321 of 1536, a 14 percent bottom margin, against 841 of 1024 on the wide hero, measured directly from the PNGs. Local gates under the CI pins: check_profile_links 34 references and 36 hashes, generate_voice_notes 9 clips 0 problems, derive_dark_assets 8 variants matching, build_locked_motion check OK on all three recipes, pinned adapter validator VALID, both hsw scans VALID, continuity validate VALID. Receipt for request 9df782a29413487d90c89449415a8108 posted to issue #27 as comment 5943631954, naming 993f8e9 and the d01d5b5 repair. Post-merge gates run 36948611156 on main at e1049db: success. Both merged SP-0008 branches deleted, local and remote.

Decisions:
- Corrected the manifest wording rather than re-placing the phone sprites, because the measured 14 percent margin is inside the 13.9 to 17.8 percent band the whole page already uses, so there was no dead third to fix. Put the gate-ordering rules in the README's gate section rather than only in the task handoff, because the next session reads the README before it reads a finished task.

Changed:
- README.md, .content-system/asset-manifest.json, docs/CONTINUITY_INDEX.md, tasks/TASK-SP-0008-hero-redraw-and-page-lead.md

Blocked/uncertain:
- none

Next:
- Pick up #28: find a page mask for scripts/derive_dark_assets.py that stops the dark GIFs flashing without shrinking the page area, and measure flashing pixels and page area together before touching any committed asset.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
