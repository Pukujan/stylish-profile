# TASK-SP-0012 — Repository README Presentation

<!-- continuity:task {"acceptance": ["README.md keeps every existing section, claim, and link; no claim is added, removed, or reworded", "three illustrations are referenced with their manifest alt text, theme-paired through #gh-light-mode-only / #gh-dark-mode-only, and each path resolves", "the What you can make or use and How it adapts lists become tables carrying the same content", "the four gate ordering rules stay on the page, folded into a single details element", "python scripts/check_profile_links.py and continuity validate --root . are green, and the required gates job is green on the exact merge candidate", "docs/CONTINUITY_INDEX.md is re-rendered so its project-readme record matches the committed README bytes"], "depends_on": [], "goal": "Re-present the repository README so it carries the profile page's own visual language and a skimmable structure: three committed illustrations, two tables where the content is tabular, and the gate ordering rules folded into a details element, without changing any claim or any sentence of the argument.", "id": "SP-0012", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/41", "next_action": "None. SP-0012 shipped in pull request #42 and is closed out; the dark-plate follow-up lives in issue #39.", "owner": "omp@windows-workstation", "priority": "P3", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "completed", "why": "The repository README explains the project well but reads as a flat document: eight sections of prose, one bullet list, and no image. The profile page it documents opens with its own illustration and pairs every figure with the idea it explains, so the repository that argues for owning your visual weight documents itself without any of its own artwork. The longest section is a run of prose a reader must read in order to find the one rule they came for."} -->

- Status: completed
- Owner: omp@windows-workstation
- Priority: P3
- Depends on: none

## Goal

Re-present the repository README so it carries the profile page's own visual
language and a skimmable structure: three of the repository's committed
illustrations, two tables where the content is genuinely tabular, and the four
gate ordering rules folded into a `<details>` element. No claim is added,
removed, or reworded, and no link is dropped.

## Why

The README explains the project well but reads as a flat document: eight `##`
sections of prose, a single bullet list, and no image. The profile page this
repository builds opens with its own illustration and pairs every figure with
the idea it explains. A reader who arrives at the repository rather than at
`github.com/Pukujan` gets the whole argument as unbroken text, and the four
gate ordering rules — each of which cost a red `gates` run to learn — sit in
the middle of that prose where a reader has to read past them to reach the
next paragraph.

## Allowed files

- README.md
- tasks/**
- checkpoints/**
- .continuity/documents.json
- docs/CONTINUITY_INDEX.md

## Human outcome

A reader who opens the repository meets the same story the profile page tells,
carried by the same artwork, and can find the one operational rule they came
for without reading the whole page. Every existing claim, link, and section is
still there; the presentation is what changed.

## Scope and boundaries

- In scope: the presentation of `README.md` — which committed illustrations it
  references, which lists become tables, and how the gate ordering rules are
  folded away.
- Out of scope: `profile/README.md`, `docs/index.html`, the tour page, the
  voice notes, the animations, the dark variants, the tracking chart, and the
  set of featured projects.
- Out of scope: rewriting the prose. This is a re-presentation; the sentences
  stay. The README may not introduce a claim the linked repositories do not
  support.

## Acceptance criteria

- [x] `README.md` keeps every existing section, claim, and link; no claim is
      added, removed, or reworded
- [x] three illustrations are referenced with their manifest alt text,
      theme-paired through `#gh-light-mode-only` / `#gh-dark-mode-only`, and
      each path resolves
- [x] the "What you can make or use" and "How it adapts" lists become tables
      carrying the same content
- [x] the four gate ordering rules stay on the page, folded into a single
      `<details>` element
- [x] `python scripts/check_profile_links.py` and `continuity validate --root .`
      are green, and the required `gates` job is green on the exact merge
      candidate
- [x] `docs/CONTINUITY_INDEX.md` is re-rendered so its `project-readme` record
      matches the committed README bytes

## Evidence and sources

Recorded on branch `task/SP-0012-repo-readme-presentation`.

| Command | Result |
| --- | --- |
| `python scripts/check_profile_links.py` | `VALID: 43 local reference(s) resolved, 36 recorded hash(es) matched` |
| `python scripts/generate_voice_notes.py --check` | `checked 9 clip(s), 0 problem(s)` |
| `python scripts/derive_dark_assets.py --check` | `VALID: 8 dark variant(s) match their source` |
| `python scripts/build_locked_motion.py check --recipe scripts/motion-recipes/{figure,hero-phone,hero-wide}.json` | `OK` on all three recipes |
| `continuity validate --root .` | `VALID` |

## Related records

- Owning issue: https://github.com/Pukujan/stylish-profile/issues/41. Leaf;
  parent ancestry: none.
- Primary writer: omp@windows-workstation, branch
  `task/SP-0012-repo-readme-presentation`.
- Takes the id after `SP-0011`, which issue
  [#39](https://github.com/Pukujan/stylish-profile/issues/39) proposes and has
  not started.

## Checkpoint log

### 2026-10-04 — omp@windows-workstation

Completed:
- The repository README is re-presented: three committed illustrations carry the "Why this exists", "What this project is" and "Evidence and boundaries" sections, the "What you can make or use" and "How it adapts" lists are tables, and the four gate ordering rules are folded into a `<details>` element. No claim, sentence, or link changed.

Evidence:
- check_profile_links VALID 43 refs/36 hashes; generate_voice_notes --check 0 problems; derive_dark_assets --check VALID 8; build_locked_motion check OK on all three recipes; continuity validate VALID.

Decisions:
- Use the animated GIFs rather than the still PNGs for the figures, because only the GIFs carry a committed dark twin; theme-pair them with `#gh-light-mode-only` / `#gh-dark-mode-only`, the mechanism the profile page already uses.

Changed:
- README.md, tasks/TASK-SP-0012-repo-readme-presentation.md, checkpoints/CURRENT.md, .continuity/documents.json, docs/CONTINUITY_INDEX.md

Blocked/uncertain:
- none

Next:
- Run `python scripts/check_profile_links.py` and `continuity validate --root .`, then open the pull request against `main`.
