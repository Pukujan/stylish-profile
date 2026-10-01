# TASK-SP-0006 — Records Follow Through

<!-- continuity:task {"acceptance": ["every manifest usage string is diffed against the shipped HTML, and no string asserts a placement the pages do not give it", "scripts/track_activity.py writes the four generated charts' hash values into the manifest, and a tracker run leaves each recorded hash equal to the file on disk", "scripts/check_profile_links.py also fails when a manifest entry's recorded hash does not match the file it names, and names the entry when it does", "scripts/generate_voice_notes.py --check compares every transcript the tour page prints under a clip that promises the clip's own words against the recorded script, and exits 1 naming the clip when they differ", "the tour page's transcript for What Is Still Being Built is verbatim with its clip, and the clip's stale count is recorded as an owner item rather than edited away", "visual-style.json roles.motion describes the motion assets that exist", "PROJECT.md, .continuity/documents.json and docs/CONTINUITY_INDEX.md describe the shipped page", "profile/README.md alt text matches the manifest and the tour page", "the sixth receipt on issue #1 no longer attributes a decision the owner never made", "the adapter check, the hotload check, both hsw modes, the link check, the voice check, the dark check and continuity validate all pass", "every paragraph the tour page marks as a transcript is the clip's own words, and the four project descriptions carry their own class instead of borrowing it", "scripts/refresh_profile.ps1, the one path that publishes to main without a pull request, validates the rewritten records before it pushes", "no record in the content adapter states a project count the page does not have", "the four chart hashes are checked against the files by scripts/check_profile_links.py, and the task records that their freshness rests on scripts/track_activity.py being their only writer, because the pinned content-system validator's hash comparison covers the narrative roles and not generated SVGs"], "depends_on": [], "goal": "Make the records that still contradict the shipped page agree with it, and make the two that can drift do so loudly instead of silently", "id": "SP-0006", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/16", "next_action": "re-run the tracker once the owner deletes the two probe repositories, then commit so the sanitizer-probe row leaves profile/tracking.json", "owner": "omp@windows-workstation", "priority": "P1", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "completed", "why": "Three stills claim a placement the pages do not give them, the tour page prints a transcript that disagrees with the audio under it, PROJECT.md and the document inventory describe the deleted shipped/not-shipped table, the tracker rewrites the charts without updating their recorded hashes, and nothing compares a page transcript against its clip"} -->

- Status: completed
- Owner: omp@windows-workstation
- Priority: P1
- Depends on: none

## Goal

Make the records that still contradict the shipped page agree with it, and make the two that can drift do so loudly instead of silently

## Why

Three stills claim a placement the pages do not give them, the tour page prints a transcript that disagrees with the audio under it, PROJECT.md and the document inventory describe the deleted shipped/not-shipped table, the tracker rewrites the charts without updating their recorded hashes, and nothing compares a page transcript against its clip

## Allowed files

- README.md
- PROJECT.md
- profile/README.md
- docs/index.html
- docs/research/github-profile-pages.md
- docs/CONTINUITY_INDEX.md
- .content-system/**
- .continuity/**
- scripts/generate_voice_notes.py
- scripts/track_activity.py
- scripts/check_profile_links.py
- scripts/refresh_profile.ps1
- .github/workflows/track.yml
- tasks/**
- checkpoints/**

## Human outcome

A reader who follows a record to the page finds the thing the record promised,
and the two records that can drift on their own - the chart hashes and the page
transcripts - fail a check instead of quietly going stale.

## Scope and boundaries

- In scope: manifest usage strings, the tour page's transcripts and the check
  that guards them, the tracker's manifest write-back, `visual-style.json`
  motion, `PROJECT.md`, the document inventory and the research write-up.
- In scope, second pass: the tour page's markup so `class="transcript"` means
  only a transcript, the content-system validator on the unattended publish
  path, and the records outside the first pass that still state a three-project
  count.
- Out of scope: regenerating any illustration or chart, and re-recording any
  voice clip. The two stale clips need a paid Fish Audio run, so they are
  recorded as open owner items rather than fixed.
- Dependencies/uncertainty: none. The clip staleness is a decision, not a
  blocker.

## Acceptance criteria

- [x] every manifest usage string is diffed against the shipped HTML, and no string asserts a placement the pages do not give it
- [x] scripts/track_activity.py writes the four generated charts' hash values into the manifest, and a tracker run leaves each recorded hash equal to the file on disk
- [x] scripts/check_profile_links.py also fails when a manifest entry's recorded hash does not match the file it names, and names the entry when it does
- [x] scripts/generate_voice_notes.py --check compares every transcript the tour page prints under a clip that promises the clip's own words against the recorded script, and exits 1 naming the clip when they differ
- [x] the tour page's transcript for What Is Still Being Built is verbatim with its clip, and the clip's stale count is recorded as an owner item rather than edited away
- [x] visual-style.json roles.motion describes the motion assets that exist
- [x] PROJECT.md, .continuity/documents.json and docs/CONTINUITY_INDEX.md describe the shipped page
- [x] profile/README.md alt text matches the manifest and the tour page
- [x] the sixth receipt on issue #1 no longer attributes a decision the owner never made
- [x] the adapter check, the hotload check, both hsw modes, the link check, the voice check, the dark check and continuity validate all pass
- [x] every paragraph the tour page marks as a transcript is the clip's own words, and the four project descriptions carry their own class instead of borrowing it
- [x] scripts/refresh_profile.ps1, the one path that publishes to main without a pull request, validates the rewritten records before it pushes
- [x] no record in the content adapter states a project count the page does not have
- [x] the four chart hashes are checked against the files by `scripts/check_profile_links.py`, and the task records that their freshness rests on `scripts/track_activity.py` being their only writer, because the pinned content-system validator's hash comparison covers the narrative roles and not generated SVGs

## Evidence and sources

Recorded at `7482fcf` on branch `task/SP-0006-records-follow-through`.

| Command | Result |
| --- | --- |
| `python <cgm>/scripts/validate_content_system.py --adapter .content-system --project-root .` | `VALID: content-generation-modules contract and target adapter` |
| `python <cgm>/scripts/verify_hsw_applied.py --root <cgm>` | exit 0 |
| `python <cgm>/scripts/verify_hsw_applied.py --root <cgm> --mode acs-html --html docs/index.html` | exit 0 |
| `python <cgm>/.../hotload_check.py --cgm-root <cgm> --adopter-root .` | exit 0 |
| `python scripts/check_profile_links.py` | `VALID: 33 local reference(s) resolved, 36 recorded hash(es) matched` |
| `python scripts/generate_voice_notes.py --check` | `checked 9 clip(s), 0 problem(s)` |
| `python scripts/derive_dark_assets.py --check` | `VALID: 8 dark variant(s) match their source` |
| `python -m continuity docs render` then `validate` then `preflight` | `RENDERED`, `VALID`, `TARGET_VALID` |

Three checks were proved by breaking them on purpose. Planting a stale hash on
`assets/profile/The Badge Wall.png` made `check_profile_links.py` exit 1 and name
the entry. Editing the `What Is Still Being Built` transcript on the tour page
made `generate_voice_notes.py --check` exit 1 and name the clip; restoring it
returned `0 problem(s)`. The tracker's write-back was proved in a scratch
checkout: all four chart hashes equalled the SVGs just written, only those four
manifest entries changed, a planted stale hash was repaired on the next run, and
a second run left every file byte-identical.

`scripts/track_activity.py --days 14 --dry-run` printed the same eight target
files and the same digests as the real run, which is what makes the dry run a
usable preview of the daily refresh.

## Reproduction details (only when needed)

Starting revision, material inputs/configuration, runtime, exact command or prompt, observed result, and limitations.

## Related records

- Owning issue: https://github.com/Pukujan/stylish-profile/issues/16. Parent
  ancestry: follows #13 and PR #14, which closed the manifest-hash work but left
  three usage strings, the transcript divergence and the tracker write-back.
  Dependencies: none.
- Primary writer: omp@windows-workstation, branch
  `task/SP-0006-records-follow-through`, as-of `784c8bf`.
- Related PR/CI evidence: PR #17, squash-merged as `14a2090` with the `gates`
  check SUCCESS and zero approvals. Issue #16 closed on merge. PR #18 landed the
  task file and its checkpoint as `5e222f1`; PR #19 landed the second pass as
  `27b0661`. The publish target `Pukujan/Pukujan` took the mirrored profile page
  as `8e0ed80`, and `raw.githubusercontent.com/Pukujan/Pukujan/main/README.md`
  is byte-identical to `profile/README.md` (SHA-256
  `21fbfd48ce7d905ad970f7f0f1259c0e368139a18d278b56a25b8d0155aac47b`). The
  receipts are the seventh and eighth on issue #1. The checkpoint is
  `2a11aa5`, pushed under request ID `4c8a1d7e93b2406f8e5a2d1b7c3f9062`.

## Checkpoint log

### 2026-10-01 18:20:00 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":["scripts/track_activity.py, scripts/check_profile_links.py, scripts/generate_voice_notes.py, .content-system/asset-manifest.json, .content-system/visual-style.json, .continuity/documents.json, .github/workflows/track.yml, PROJECT.md, README.md, profile/README.md, docs/index.html, docs/research/github-profile-pages.md, docs/CONTINUITY_INDEX.md, tasks, checkpoints"],"completed":["the records that still contradicted the shipped page now agree with it, and the two that could drift on their own fail a check instead of going stale"],"decisions":["the four project notes on the tour page print a description under a What it does label rather than the clip's words, so the transcript check compares only the notes that promise the clip's own words; the two clips that still say three projects stay verbatim with their audio and are recorded as open owner items, because correcting them needs a paid Fish Audio run"],"evidence":["PR #17 squash-merged as 14a2090 with the gates check SUCCESS and zero approvals, closing issue #16; check_profile_links.py reports 33 references and 36 recorded hashes and exits 1 on a planted stale hash; generate_voice_notes.py --check reports 9 clips and 0 problems and exits 1 naming the clip when a verbatim transcript is edited; the tracker's write-back was proved in a scratch checkout where all four chart hashes equalled the SVGs just written, a planted stale hash was repaired, and a second run left every file byte-identical; the mirror Pukujan/Pukujan took the profile page as 8e0ed80 and the live raw file is byte-identical to profile/README.md"],"next_action":"wait for the owner to delete the two probe repositories, then re-run the tracker and commit so the sanitizer-probe row leaves profile/tracking.json","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0006","timestamp":"2026-10-01T18:20:00Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"3894a0bbcf684c8d117b534474d0f209210e9837c83cb242eeb7cffc73173f14","request_id":"4c8a1d7e93b2406f8e5a2d1b7c3f9062","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0006"} -->

Completed:
- the records that still contradicted the shipped page now agree with it, and the two that could drift on their own fail a check instead of going stale

Evidence:
- PR #17 squash-merged as 14a2090 with the gates check SUCCESS and zero approvals, closing issue #16; check_profile_links.py reports 33 references and 36 recorded hashes and exits 1 on a planted stale hash; generate_voice_notes.py --check reports 9 clips and 0 problems and exits 1 naming the clip when a verbatim transcript is edited; the tracker's write-back was proved in a scratch checkout where all four chart hashes equalled the SVGs just written, a planted stale hash was repaired, and a second run left every file byte-identical; the mirror Pukujan/Pukujan took the profile page as 8e0ed80 and the live raw file is byte-identical to profile/README.md

Decisions:
- the four project notes on the tour page print a description under a What it does label rather than the clip's words, so the transcript check compares only the notes that promise the clip's own words; the two clips that still say three projects stay verbatim with their audio and are recorded as open owner items, because correcting them needs a paid Fish Audio run

Changed:
- scripts/track_activity.py, scripts/check_profile_links.py, scripts/generate_voice_notes.py, .content-system/asset-manifest.json, .content-system/visual-style.json, .continuity/documents.json, .github/workflows/track.yml, PROJECT.md, README.md, profile/README.md, docs/index.html, docs/research/github-profile-pages.md, docs/CONTINUITY_INDEX.md, tasks, checkpoints

Blocked/uncertain:
- none

Next:
- wait for the owner to delete the two probe repositories, then re-run the tracker and commit so the sanitizer-probe row leaves profile/tracking.json

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
