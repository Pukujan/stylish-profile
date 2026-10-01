# TASK-SP-0006 — Records Follow Through

<!-- continuity:task {"acceptance": ["every manifest usage string is diffed against the shipped HTML, and no string asserts a placement the pages do not give it", "scripts/track_activity.py writes the four generated charts' hash values into the manifest, and a tracker run leaves each recorded hash equal to the file on disk", "scripts/check_profile_links.py also fails when a manifest entry's recorded hash does not match the file it names, and names the entry when it does", "scripts/generate_voice_notes.py --check compares every transcript the tour page prints under a clip that promises the clip's own words against the recorded script, and exits 1 naming the clip when they differ", "the tour page's transcript for What Is Still Being Built is verbatim with its clip, and the clip's stale count is recorded as an owner item rather than edited away", "visual-style.json roles.motion describes the motion assets that exist", "PROJECT.md, .continuity/documents.json and docs/CONTINUITY_INDEX.md describe the shipped page", "profile/README.md alt text matches the manifest and the tour page", "the sixth receipt on issue #1 no longer attributes a decision the owner never made", "the adapter check, the hotload check, both hsw modes, the link check, the voice check, the dark check and continuity validate all pass"], "depends_on": [], "goal": "Make the records that still contradict the shipped page agree with it, and make the two that can drift do so loudly instead of silently", "id": "SP-0006", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/16", "next_action": "rewrite the three unplaced stills' usage strings, then make the tracker write the chart hashes", "owner": "omp@windows-workstation", "priority": "P1", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "active", "why": "Three stills claim a placement the pages do not give them, the tour page prints a transcript that disagrees with the audio under it, PROJECT.md and the document inventory describe the deleted shipped/not-shipped table, the tracker rewrites the charts without updating their recorded hashes, and nothing compares a page transcript against its clip"} -->

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
  check SUCCESS and zero approvals. Issue #16 closed on merge. The publish
  target `Pukujan/Pukujan` took the mirrored profile page as `8e0ed80`, and
  `raw.githubusercontent.com/Pukujan/Pukujan/main/README.md` is byte-identical
  to `profile/README.md` (SHA-256
  `21fbfd48ce7d905ad970f7f0f1259c0e368139a18d278b56a25b8d0155aac47b`). The
  receipt is the seventh on issue #1.

## Checkpoint log

No checkpoints yet.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
