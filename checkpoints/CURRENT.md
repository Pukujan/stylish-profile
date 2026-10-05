# Current Repository Checkpoint

<!-- continuity:current {"active_task":"SP-0012","active_task_file":"tasks/TASK-SP-0012-repo-readme-presentation.md","protocol_version":"0.1.0-draft","schema":"project-continuity.current.v1"} -->

This is an as-of projection; live GitHub issues own progression. Link the owning leaf, parent ancestry and dependencies for active work.

## Program state

Phase: bootstrap.

## Completed

- continuity protocol initialized.
- SP-0001: the profile page shipped, with the illustrations, charts, and the written record.
- SP-0002: the projects table, a spoken note per project, four-frame animations, and a derived dark variant of every image.
- SP-0003: every voice note opens and plays, the dark variants cannot go stale without failing the gate, and the account has an avatar drawn as the same character as the page.
- SP-0004: the dark illustrations keep the character's own colours, and both pages introduce Pujan instead of auditing him.
- SP-0005: every content-system record matches the page it describes, and the length printed beside each voice note is checked against the clip.
- SP-0006: the records that still contradicted the shipped page agree with it, and the two that could drift fail a check instead of going stale quietly.
- SP-0007: the hero and the figure beside the project list are rebuilt from one locked environment plate plus keyed character sprites, so only the characters move; `scripts/build_locked_motion.py check` fails a committed GIF whose environment drifts outside its declared moving boxes, and runs as a gate.
- SP-0008: the hero is redrawn from scratch with the configured image model and the dark transform no longer repaints a figure's own outline as light ink, so the silhouette halo is gone; the page and the tour page now run hero, introduction, market, what Pujan does about it, the daily commits, the featured projects, then the rest. Merged to `main` as `14338d2` from pull request #29, with every step of the required `gates` job green on the merge candidate.
- SP-0009: the derived dark GIFs no longer flash. The page mask is decided once for the whole loop instead of once per frame, so a pixel byte-identical in two consecutive light frames gets the same dark output. Flash is 0 on all eight committed dark GIFs (was 24,148), both hero animations' page area is unchanged (+0.00%), and the dark hero's 48,617 px of surviving page cream are preserved exactly. Merged to `main` as `8add943` from pull request #35, with the required `gates` job green on the merge candidate and on `main`.
- SP-0010: the profile page leads with the market instead of the audit register. It runs hero, a short introduction naming Agent Custom Setup, the market, what Pujan does about it, the daily commits, the featured projects, then the rest, and `docs/index.html` tells the same story at the same points. The market opener no longer asserts a market shift the linked repositories do not demonstrate, and the four `What I do about it` bullets no longer share one `not X` shape. Merged to `main` as `10d2012` from pull request #37, with the required `gates` job green on the merge candidate and on `main`; mirrored to `Pukujan/Pukujan` as `348db42` so `github.com/Pukujan` renders it.

## Active

- SP-0012: the repository README is re-presented so it carries the profile
  page's own visual language and a skimmable structure — three of the
  repository's committed illustrations, two tables where the content is
  tabular, and the four gate ordering rules folded into a `<details>`. Same
  sections, claims, links and sentences; the presentation changed. Issue #41,
  branch `task/SP-0012-repo-readme-presentation`. Not merged.

The two records that could drift are gated: `scripts/track_activity.py`
writes the chart hashes it draws into the manifest, `scripts/check_profile_links.py`
fails when a recorded hash no longer matches its file, and
`scripts/generate_voice_notes.py --check` fails when a transcript the page
promises is the clip's own words is not. The two rebuilt figures are gated the
same way: `scripts/build_locked_motion.py check` fails a committed GIF whose
environment drifts outside the moving boxes its recipe declares.

## Queued

- #39: the dark variants are derived from the light asset by a deterministic recolour. Comparing that against a purpose-drawn dark ground, or reversing the pipeline to a video-generation route with an image-to-video reference frame, would reverse `.content-system/project-brief.json` `mechanism[1]`. The issue asks for a side-by-side comparison and a decision before any code; adoption would retire the `gates.yml` step "Dark variants match their source". Not started.
- Re-run the tracker once the two probe repositories are gone, so the `sanitizer-probe` row leaves `profile/tracking.json`.
- Re-record `The Short Tour.mp3` and `What Is Still Being Built.mp3`, which still say three projects where the page lists four. Needs a paid Fish Audio run and the owner's approval.
- Upload the avatar to the GitHub account, which is a web-UI action the REST API does not expose.
- Delete the two throwaway probe repositories, which needs the `delete_repo` scope on the `gh` token.

## Blockers

None known.

## Next atomic action

Open the pull request for SP-0012 against `main`, verify the required `gates`
check on the exact merge candidate, merge with `gh pr merge --squash`, and post
the leaf receipt to issue #41. Then file the dark-plate and video-generation
follow-up issue with a supersession link to `.content-system/project-brief.json`
`mechanism[1]`, naming the `scripts/derive_dark_assets.py` path and the
`gates.yml` step "Dark variants match their source" as the things adoption
would retire. When the owner deletes the two probe repositories, re-run
`scripts/track_activity.py --days 14`, then `continuity docs render`, then
commit so the `sanitizer-probe` row leaves `profile/tracking.json`.
