# Current Repository Checkpoint

<!-- continuity:current {"active_task":null,"active_task_file":null,"protocol_version":"0.1.0-draft","schema":"project-continuity.current.v1"} -->

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

## Active

None. The two records that could drift are gated: `scripts/track_activity.py`
writes the chart hashes it draws into the manifest, `scripts/check_profile_links.py`
fails when a recorded hash no longer matches its file, and
`scripts/generate_voice_notes.py --check` fails when a transcript the page
promises is the clip's own words is not. The two rebuilt figures are gated the
same way: `scripts/build_locked_motion.py check` fails a committed GIF whose
environment drifts outside the moving boxes its recipe declares.

## Queued

- #28: the derived dark GIFs still flash where a moving sprite crosses
  page-coloured territory. Pre-existing, reduced by SP-0008 from 36,523 flashing
  pixels to 24,148, not removed. Needs a page mask that is leak-proof without
  shrinking the page area.
- Re-run the tracker once the two probe repositories are gone, so the `sanitizer-probe` row leaves `profile/tracking.json`.
- Re-record `The Short Tour.mp3` and `What Is Still Being Built.mp3`, which still say three projects where the page lists four. Needs a paid Fish Audio run and the owner's approval.
- Upload the avatar to the GitHub account, which is a web-UI action the REST API does not expose.
- Delete the two throwaway probe repositories, which needs the `delete_repo` scope on the `gh` token.

## Blockers

None known.

## Next atomic action

Nothing is active. The earliest queued item that needs no outside help is #28:
find a page mask for `scripts/derive_dark_assets.py` that stops the dark GIFs
flashing without shrinking the page area, then measure flashing pixels and page
area together before touching any committed asset. When the owner deletes the
two probe repositories, re-run `scripts/track_activity.py --days 14`, then
`continuity docs render`, then commit so the `sanitizer-probe` row leaves
`profile/tracking.json`.
