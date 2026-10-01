# TASK-SP-0006 — Records Follow Through

<!-- continuity:task {"acceptance": ["every manifest usage string is diffed against the shipped HTML, and no string asserts a placement the pages do not give it", "scripts/track_activity.py writes the four generated charts' hash values into the manifest, and a tracker run leaves each recorded hash equal to the file on disk", "scripts/check_profile_links.py also fails when a manifest entry's recorded hash does not match the file it names, and names the entry when it does", "scripts/generate_voice_notes.py --check compares every transcript the tour page prints under a clip that promises the clip's own words against the recorded script, and exits 1 naming the clip when they differ", "the tour page's transcript for What Is Still Being Built is verbatim with its clip, and the clip's stale count is recorded as an owner item rather than edited away", "visual-style.json roles.motion describes the motion assets that exist", "PROJECT.md, .continuity/documents.json and docs/CONTINUITY_INDEX.md describe the shipped page", "profile/README.md alt text matches the manifest and the tour page", "the sixth receipt on issue #1 no longer attributes a decision the owner never made", "the adapter check, the hotload check, both hsw modes, the link check, the voice check, the dark check and continuity validate all pass"], "depends_on": [], "goal": "Make the records that still contradict the shipped page agree with it, and make the two that can drift do so loudly instead of silently", "id": "SP-0006", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/16", "next_action": "rewrite the three unplaced stills' usage strings, then make the tracker write the chart hashes", "owner": "omp@windows-workstation", "priority": "P1", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "active", "why": "Three stills claim a placement the pages do not give them, the tour page prints a transcript that disagrees with the audio under it, PROJECT.md and the document inventory describe the deleted shipped/not-shipped table, the tracker rewrites the charts without updating their recorded hashes, and nothing compares a page transcript against its clip"} -->

- Status: active
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

Link repository state at a revision and cite external factual claims directly. Record commands and results for claims that need verification.

## Reproduction details (only when needed)

Starting revision, material inputs/configuration, runtime, exact command or prompt, observed result, and limitations.

## Related records

- Owning issue: https://github.com/Pukujan/stylish-profile/issues/16. Parent
  ancestry: follows #13 and PR #14, which closed the manifest-hash work but left
  three usage strings, the transcript divergence and the tracker write-back.
  Dependencies: none.
- Primary writer: omp@windows-workstation, branch
  `task/SP-0006-records-follow-through`, as-of `784c8bf`.
- Related PR/CI evidence: pending the pull request for this branch.

## Checkpoint log

No checkpoints yet.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
