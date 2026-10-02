# TASK-SP-0010 — Profile Page Leads With the Market

<!-- continuity:task {"acceptance": ["profile/README.md runs hero, short introduction naming Agent Custom Setup, the market, what Pujan does about it, the daily commits, the featured projects, then the rest", "the market section states the reader's situation without asserting an unsourced claim about the industry, so project-brief.json boundaries still holds", "no banned term from .content-system/brand-language.json appears in either surface", "docs/index.html tells the same story as the README at the same points, with the same section id and heading", "every existing gate stays green: check_profile_links, generate_voice_notes --check, the pinned content-system adapter validator, both hsw scans, derive_dark_assets.py --check, build_locked_motion.py check, and continuity validate"], "depends_on": ["SP-0009"], "goal": "Reorder and rewrite the profile page so it runs hero, short introduction naming the featured project, the market, what Pujan does about it, the daily commits, the projects, then everything else, with the market framed for a reader rather than described in audit language.", "id": "SP-0010", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/36", "next_action": "file the dark-plate and video-generation follow-up issue with a supersession link to project-brief.json mechanism[1]", "owner": "omp@windows-workstation", "priority": "P2", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "completed", "why": "The page opens by explaining what Pujan is rather than why any of it matters. The first line after the heading is the job title AI engineer, and the section that should set up the problem is headed The work and opens with Document-heavy AI means the input is a contract. A reader who lands on the page gets a title and a technical register before a reason to keep reading, and the same two blocks are mirrored in docs/index.html. Nothing in the built assets changes: no images, no animations, no voice notes."} -->

- Status: completed
- Owner: omp@windows-workstation
- Priority: P2
- Depends on: SP-0009

## Goal

Reorder and rewrite the profile page so it runs hero, a short introduction
naming the featured project, the market, what Pujan does about it, the daily
commits, the featured projects, then everything else, with the market framed for
a reader rather than described in audit language.

## Why

The page opens by explaining what Pujan is rather than why any of it matters.
The first line after `# Hi, I'm Pujan` is `**AI engineer.**`, and the section
that should set up the problem is headed `## The work` and opens with
`Document-heavy AI means the input is a contract…`. A reader who lands on the
page gets a title and a technical register before a reason to keep reading.

`docs/index.html` mirrors both blocks, so a fix in one surface without the other
leaves the two pages telling different stories.

## Allowed files

- profile/README.md
- docs/index.html
- .content-system/project-brief.json
- .content-system/asset-manifest.json
- tasks/**
- checkpoints/**
- .continuity/documents.json
- docs/CONTINUITY_INDEX.md
- PROJECT.md

## Human outcome

A reader who lands on the page learns what the page is for and who it is for
before they meet any mechanism. The projects and the daily commits still make
the same claims they made before; they are reached through a reason to care.

## Scope and boundaries

- In scope: the order and the wording of `profile/README.md` and the same
  wording in `docs/index.html`, plus any record that describes the page's
  structure.
- Out of scope: the images, the animations, the dark variants, the voice notes,
  the tracking chart, the projects table, and the set of featured projects.
- The rewrite may not introduce a claim the linked repositories do not
  demonstrate. `project-brief.json` `boundaries` is the rule; a market-shift
  assertion needs a sourced `evidence` entry or it does not ship.

## Acceptance criteria

- [x] `profile/README.md` runs hero, short introduction naming `Agent Custom
      Setup`, the market, what Pujan does about it, the daily commits, the
      featured projects, then the rest
- [x] the market section states the reader's situation without asserting an
      unsourced claim about the industry, so `project-brief.json` `boundaries`
      still holds
- [x] no banned term from `.content-system/brand-language.json` appears in
      either surface
- [x] `docs/index.html` tells the same story as the README at the same points,
      with the same section id and heading
- [x] every existing gate stays green: `check_profile_links`,
      `generate_voice_notes --check`, the pinned content-system adapter
      validator, both hsw scans, `derive_dark_assets.py --check`,
      `build_locked_motion.py check`, and `continuity validate`

## Evidence and sources

Recorded on branch `task/SP-0010-profile-voice-and-order`.

| Command | Result |
| --- | --- |
| `python scripts/check_profile_links.py` | `VALID: 35 local reference(s) resolved, 36 recorded hash(es) matched` |
| `python scripts/generate_voice_notes.py --check` | `checked 9 clip(s), 0 problem(s)` |
| `python scripts/derive_dark_assets.py --check` | `VALID: 8 dark variant(s) match their source` |
| `python scripts/build_locked_motion.py check --recipe scripts/motion-recipes/{figure,hero-phone,hero-wide}.json` | `OK` on all three |
| pinned content-system `validate_content_system.py --adapter .content-system` | `VALID: content-generation-modules contract and target adapter` |
| pinned content-system `verify_hsw_applied.py --root <cgm>` | `VALID: HSW always-on contract OK` |
| pinned content-system `verify_hsw_applied.py --mode acs-html --html docs/index.html` | `VALID: HSW always-on contract OK and HTML tell scan clean` |
| `continuity validate --root .` | `VALID` |

### What changed in the copy

Two substantive edits against the held draft, both to satisfy
`project-brief.json` `boundaries` and `brand-language.json`:

- The market opener read `AI moved out of demos and into document-heavy work`,
  which asserts a market shift the linked repositories do not demonstrate. It
  now reads `The work is document-heavy AI systems: a contract, a filing, a case
  file, a policy pack.`, which states the reader's situation and uses the
  brand-language preferred term for AI/ML work.
- Three of the four `What I do about it` bullets used the same `not X` shape
  (`not a blank prompt`, `not a template`, `not a hard-coded provider`). The
  fourth now reads `The model route follows a policy.`, leaving two.

Both edits are mirrored in `docs/index.html`.

### Record correction carried in this increment

`content-adapter` in `.continuity/documents.json` recorded
`4c8048e298295190683ebdbd42ac5337aa2c57b069f99729da1ffa27ecffd071` for
`.content-system/asset-manifest.json`. That is the CRLF hash of the file; the
committed blob is LF and hashes to `4c1ff489bb14e1df…`, because `.gitattributes`
sets `* text=auto eol=lf`. The recorded value was therefore a line-ending
artifact, and SP-0009's own commit left the document reading `NEEDS_REVIEW`.
This increment corrects the value to the committed bytes. It is a fact fix for a
file SP-0009 changed, not a re-bless of bytes this increment read.

Four other documents (`project-brief`, `project-contract`, `project-readme`,
`render-limits-research`) read `NEEDS_REVIEW` on `main` before this increment
and still do; they are outside this task's scope and were left alone.

## Related records

- Owning issue: https://github.com/Pukujan/stylish-profile/issues/36. Leaf;
  parent ancestry: none. Depends on SP-0009, whose merge this branches after.
- Primary writer: omp@windows-workstation, branch
  `task/SP-0010-profile-voice-and-order`.
- Not a continuation of #28: that issue's scope list puts page copy and order
  out of scope.

## Checkpoint log

### 2026-10-02 04:19:40 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":["profile/README.md, docs/index.html, tasks/TASK-SP-0010-profile-voice-and-order.md, tasks/TASK-SP-0009-dark-copies-stop-flashing.md, checkpoints/CURRENT.md, .continuity/documents.json, docs/CONTINUITY_INDEX.md"],"completed":["The profile page now leads with the market instead of the audit register: hero, short introduction naming Agent Custom Setup, the market, what Pujan does about it, the daily commits, the featured projects, then the rest, mirrored in docs/index.html."],"decisions":["Two edits against the held draft: the market opener no longer asserts a market shift the linked repositories do not demonstrate, and the fourth bullet no longer repeats the 'not X' shape the other two use. Both satisfy project-brief boundaries and brand-language."],"evidence":["check_profile_links VALID 35 refs/36 hashes; generate_voice_notes --check 0 problems; derive_dark_assets --check VALID 8; build_locked_motion check OK on every recipe; pinned content-system adapter VALID; both hsw scans VALID; continuity validate VALID."],"next_action":"Open the pull request against main, verify the required gates check on the exact merge candidate, merge with gh pr merge --squash, post the leaf receipt to issue #36, then dispatch track-activity so the mirror to Pukujan/Pukujan picks the new copy up.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0010","timestamp":"2026-10-02T04:19:40Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"0beac123d083cef1036b4e66e24e8b218426f826ab3de397a8b6ac69b153fb91","request_id":"c0724c1ee5c0424d9beb20e67a1e76be","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0010"} -->

Completed:
- The profile page now leads with the market instead of the audit register: hero, short introduction naming Agent Custom Setup, the market, what Pujan does about it, the daily commits, the featured projects, then the rest, mirrored in docs/index.html.

Evidence:
- check_profile_links VALID 35 refs/36 hashes; generate_voice_notes --check 0 problems; derive_dark_assets --check VALID 8; build_locked_motion check OK on every recipe; pinned content-system adapter VALID; both hsw scans VALID; continuity validate VALID.

Decisions:
- Two edits against the held draft: the market opener no longer asserts a market shift the linked repositories do not demonstrate, and the fourth bullet no longer repeats the 'not X' shape the other two use. Both satisfy project-brief boundaries and brand-language.

Changed:
- profile/README.md, docs/index.html, tasks/TASK-SP-0010-profile-voice-and-order.md, tasks/TASK-SP-0009-dark-copies-stop-flashing.md, checkpoints/CURRENT.md, .continuity/documents.json, docs/CONTINUITY_INDEX.md

Blocked/uncertain:
- none

Next:
- Open the pull request against main, verify the required gates check on the exact merge candidate, merge with gh pr merge --squash, post the leaf receipt to issue #36, then dispatch track-activity so the mirror to Pukujan/Pukujan picks the new copy up.
