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
- [x] no manifest usage string names a section that is not on the shipped page, and the entry for Pujan and the Loose Ends.png records that it is the lineage parent of the live avatar
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

No checkpoints yet.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
