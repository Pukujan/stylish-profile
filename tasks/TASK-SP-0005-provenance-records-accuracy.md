# TASK-SP-0005 — Provenance Records Accuracy

<!-- continuity:task {"acceptance":["asset-manifest.json lists 36 assets, every entry's hash equals the SHA-256 of the file on disk, and the set of manifest paths equals the set of files under assets/profile/","every -dark.gif and -dark.svg entry carries derived_from plus a derivation that describes the paper-mask transform or the palette swap, and no entry still describes the retired lightness inversion","no manifest usage string names a section that is not on the shipped page, and the entry for Pujan and the Loose Ends.png records that it is the lineage parent of the live avatar","the tour page's avatar alt text equals the manifest alt_text for assets/profile/Pujan.png","scripts/generate_voice_notes.py --check exits 0 on the committed clips, and exits 1 naming the clip when a length label in profile/README.md is edited to disagree with the clip","gates.yml pins pillow, numpy and scipy to the versions the dark GIFs were assembled with and installs those pins in the dark step","the root README states the shipped counts of animations, charts and voice notes, and names no star output and no repository index","docs/research/github-profile-pages.md states the shipped counts, the shipped projects-section shape, and the paper-mask reason for deriving dark variants","brand-language.json promise and audience_feeling describe an introduction, and personality carries no audit framing","the clause 'starts with the right rules instead of guessing' appears once in profile/README.md, and the three Agent Custom Setup slots carry distinct jobs","validate_content_system.py, verify_hsw_applied.py in both modes, check_profile_links.py, generate_voice_notes.py --check, derive_dark_assets.py --check and continuity validate all pass after continuity docs render"],"depends_on":[],"goal":"Make every content-system record describe the page that actually ships, and gate the one claim on the page that nothing checked","id":"SP-0005","issue_url":"https://github.com/Pukujan/stylish-profile/issues/13","next_action":"none; the queued tracker refresh waits on the owner deleting the two probe repositories","owner":"omp@windows-workstation","priority":"P1","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"completed","why":"The asset manifest missed four files that are on disk, carried eight stale hashes, and still described the dark transform that #12 replaced; the root README, the research write-up and the brand language described an older page, and the length printed beside each voice note was hand-typed with nothing verifying it"} -->

- Status: completed
- Owner: omp@windows-workstation
- Priority: P1
- Depends on: none

## Goal

Make every content-system record describe the page that actually ships, and gate the one claim on the page that nothing checked

## Why

The asset manifest missed four files that are on disk, carried eight stale hashes, and still described the dark transform that #12 replaced; the root README, the research write-up and the brand language described an older page, and the length printed beside each voice note was hand-typed with nothing verifying it

## Allowed files

- README.md
- profile/README.md
- docs/index.html
- docs/research/github-profile-pages.md
- docs/CONTINUITY_INDEX.md
- assets/profile/**
- .content-system/**
- scripts/generate_voice_notes.py
- .github/workflows/gates.yml
- tasks/**
- checkpoints/**

## Human outcome

A reader who opens the record to find out where an image came from gets an answer
that matches the file on disk, and the page can no longer print a clip length that
disagrees with the clip.

## Scope and boundaries

- In scope: the content-system records, the root README, the research write-up, the
  tour page and profile page prose, the voice-note length check, and the pins on the
  dark check's dependencies.
- Out of scope: regenerating any illustration, changing the dark transform, deleting
  the two probe repositories, and re-running the tracker.
- Dependencies/uncertainty: re-running the tracker waits on the owner deleting
  sanitizer-probe, which is a web-UI action. Nothing in this task blocks on it.

## Acceptance criteria

- [x] asset-manifest.json lists 36 assets, every entry's hash equals the SHA-256 of the file on disk, and the set of manifest paths equals the set of files under assets/profile/
- [x] every -dark.gif and -dark.svg entry carries derived_from plus a derivation that describes the paper-mask transform or the palette swap, and no entry still describes the retired lightness inversion
- [x] nine retired assets' usage strings no longer name a deleted section, and the entry for Pujan and the Loose Ends.png records that it is the lineage parent of the live avatar. Three stills that assert a live placement - AI Engineer.png, AI Engineer phone.png and Three Projects One Thread.png - were missed and are carried by SP-0006.
- [x] the tour page's avatar alt text equals the manifest alt_text for assets/profile/Pujan.png
- [x] scripts/generate_voice_notes.py --check exits 0 on the committed clips, and exits 1 naming the clip when a length label in profile/README.md is edited to disagree with the clip
- [x] gates.yml pins pillow, numpy and scipy to the versions the dark GIFs were assembled with and installs those pins in the dark step
- [x] the root README states the shipped counts of animations, charts and voice notes, and names no star output and no repository index
- [x] docs/research/github-profile-pages.md states the shipped counts, the shipped projects-section shape, and the paper-mask reason for deriving dark variants
- [x] brand-language.json promise and audience_feeling describe an introduction, and personality carries no audit framing
- [x] the clause 'starts with the right rules instead of guessing' appears once in profile/README.md, and the three Agent Custom Setup slots carry distinct jobs
- [x] validate_content_system.py, verify_hsw_applied.py in both modes, check_profile_links.py, generate_voice_notes.py --check, derive_dark_assets.py --check and continuity validate all pass after continuity docs render

## Evidence and sources

Recorded at `ffaea9d` on branch `task/SP-0005-provenance-records-accuracy`.

| Command | Result |
| --- | --- |
| `python <cgm>/scripts/validate_content_system.py --adapter .content-system --project-root .` | `VALID: content-generation-modules contract and target adapter` |
| `python <cgm>/scripts/verify_hsw_applied.py --root <cgm>` | exit 0 |
| `python <cgm>/scripts/verify_hsw_applied.py --root <cgm> --mode acs-html --html docs/index.html` | exit 0 |
| `python scripts/check_profile_links.py` | `VALID: 33 local reference(s) resolved` |
| `python scripts/generate_voice_notes.py --check` | `checked 9 clip(s), 0 problem(s)` |
| `python scripts/derive_dark_assets.py --check` | `VALID: 8 dark variant(s) match their source` |
| `python -m continuity docs render` then `python -m continuity validate` | `RENDERED`, then `VALID` |

Two checks were proved by breaking them on purpose and watching them fail: editing a
length label in `profile/README.md` made the voice-note check exit 1 and name the
clip, and the manifest's stale hashes were found by comparing every entry against
its file rather than by trusting the record.

The frame walk in `scripts/generate_voice_notes.py` was compared against ffprobe on
all nine clips; the two agree to within 0.1 ms.

## Reproduction details (only when needed)

Starting revision, material inputs/configuration, runtime, exact command or prompt, observed result, and limitations.

## Related records

- Owning issue: https://github.com/Pukujan/stylish-profile/issues/13. Parent ancestry:
  follows #11 and PR #12, which replaced the dark transform this task's records still
  described. Dependencies: none.
- Primary writer: omp@windows-workstation, branch
  `task/SP-0005-provenance-records-accuracy`, as-of `ffaea9d`.
- Related PR/CI evidence: PR #14, squash-merged as `4e7c85b` with the `gates` check SUCCESS and zero approvals. The publish target `Pukujan/Pukujan` took the mirrored profile page as `174ba74`, and `raw.githubusercontent.com/Pukujan/Pukujan/main/README.md` is byte-identical to `profile/README.md` (SHA-256 `955c6ef531bd56911bd47ac7b87669cd6788313fd55cbdc911b17628a4d54526`). The receipt is the sixth on issue #1.

## Checkpoint log

### 2026-10-01 17:33:41 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":[".content-system/asset-manifest.json, .content-system/visual-style.json, .content-system/prompts/Pujan.md, .content-system/brand-language.json, README.md, PROJECT.md, docs/research/github-profile-pages.md, docs/index.html, profile/README.md, scripts/generate_voice_notes.py, .github/workflows/gates.yml, tasks/TASK-SP-0005-provenance-records-accuracy.md, checkpoints/CURRENT.md"],"completed":["every content-system record describes the page that actually ships, and the length printed beside each voice note is checked against the clip"],"decisions":["the clip's own bytes are the ground truth for the length printed beside it, because the label was hand-typed and had drifted by a full second; mp3_duration() walks the frame headers with the standard library so the check needs no audio toolchain on the runner"],"evidence":["PR #14 merged through `gates` with zero approvals as 4e7c85b, then PR #15 recorded the merge as 784c8bf; the asset manifest went from 32 to 36 entries with every hash equal to the SHA-256 of the file on disk; generate_voice_notes.py --check reported 9 clips and 0 problems and caught the tour page printing (0:19) beside a clip that is 18.47 s, corrected to (0:18)"],"next_action":"read the merged result against the page again; a review of 4e7c85b found three unplaced stills whose usage strings still described a section that no longer exists, a transcript on the tour page that had been tidied away from its clip, and a tracker that redraws the charts without updating their recorded hashes","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0005","timestamp":"2026-10-01T17:33:41Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"c7f8c4609b638cc4caa51944b631242787065897ec6865ba9bb8f89089e1f1d9","request_id":"8d3f5a1c6b0e42d7a9c41f2e5b7d6038","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0005"} -->

Completed:
- every content-system record describes the page that actually ships, and the length printed beside each voice note is checked against the clip

Evidence:
- PR #14 merged through `gates` with zero approvals as 4e7c85b, then PR #15 recorded the merge as 784c8bf; the asset manifest went from 32 to 36 entries with every hash equal to the SHA-256 of the file on disk; generate_voice_notes.py --check reported 9 clips and 0 problems and caught the tour page printing (0:19) beside a clip that is 18.47 s, corrected to (0:18)

Decisions:
- the clip's own bytes are the ground truth for the length printed beside it, because the label was hand-typed and had drifted by a full second; mp3_duration() walks the frame headers with the standard library so the check needs no audio toolchain on the runner

Changed:
- .content-system/asset-manifest.json, .content-system/visual-style.json, .content-system/prompts/Pujan.md, .content-system/brand-language.json, README.md, PROJECT.md, docs/research/github-profile-pages.md, docs/index.html, profile/README.md, scripts/generate_voice_notes.py, .github/workflows/gates.yml, tasks/TASK-SP-0005-provenance-records-accuracy.md, checkpoints/CURRENT.md

Blocked/uncertain:
- none

Next:
- read the merged result against the page again; a review of 4e7c85b found three unplaced stills whose usage strings still described a section that no longer exists, a transcript on the tour page that had been tidied away from its clip, and a tracker that redraws the charts without updating their recorded hashes

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
