# TASK-SP-0001 — Profile Page

<!-- continuity:task {"acceptance": ["github.com/Pukujan renders the mirrored page with the hero illustration, four project sections, the shipped/not-shipped table and the live activity block", "scripts/track_activity.py regenerates commit counts, the current project, star totals and the repository index from the GitHub API, and two consecutive runs over unchanged data produce byte-identical output", "the required gates check passes on the publishing pull request and auto-merge lands it with zero approvals", "scripts/check_profile_links.py resolves every relative reference in every Markdown and HTML file and exits zero", "the content adapter validates against the pinned helper revision and every narrative asset hash matches the committed file", "no published file contains a secret, a private repository name, or a claim the linked repositories cannot support"], "depends_on": [], "goal": "Publish a profile page at github.com/Pukujan that explains four featured projects and keeps its own activity numbers true by regenerating them from the GitHub API on a schedule.", "id": "SP-0001", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/1", "next_action": "none - the page shipped and was verified; the v2 shape of the page is tracked by SP-0002", "owner": "omp@windows-workstation", "priority": "P1", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "completed", "why": "The current page's loudest element is a third-party statistics card, so a first-time reader learns nothing about what the projects do, and the page's own numbers would be hand-copied into Markdown in a repository whose whole point is that nothing is hand-copied."} -->

- Status: completed
- Owner: omp@windows-workstation
- Priority: P1
- Depends on: none

## Goal

Publish a profile page at `github.com/Pukujan` that explains four featured projects — Agent Custom Setup, Project Continuity Modules, Content Generation Modules and Inference Recommendation Engine — and keeps its own activity numbers true by regenerating them from the GitHub API on a schedule.

## Why

The previous page's loudest element was a third-party statistics card. A first-time reader learned nothing about what any project does, and two of the services behind those cards now return payment errors while a third no longer resolves.

There is a second reason. The featured repositories exist to stop long work from silently drifting — a pinned version, a required check, a recorded decision. A profile page that hand-copies its own numbers into Markdown would contradict the thing it is advertising.

## Allowed files

- `profile/README.md` — the publishable page.
- `README.md` — the project README.
- `PROJECT.md`, `tasks/`, `checkpoints/`, `HANDOFF.md`, `.continuity/` — PCM projections.
- `.content-system/` — the content adapter: brief, brand language, visual contract, asset manifest, review rubric, prompt records, filename legends.
- `assets/profile/` and `assets/profile/generated/` — narrative images, voice notes, generated SVGs.
- `docs/index.html`, `docs/research/` — the tour page and the research write-up.
- `scripts/`, `.github/workflows/`, `.coord/` — the link checker, the activity tracker, CI, and the hotload assignment.
- `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`.

## Human outcome

A reader who has never heard of these projects can tell, in under a minute, what kind of engineer wrote them, which repositories are real, what each one is for, and what is still unfinished. The numbers on the page are produced by a scheduled generator rather than typed by hand, so the page cannot quietly become untrue.

## Scope and boundaries

- In scope:
  - The publishable page and the tour page, including the auto-regenerated activity block.
  - The activity tracker, its daily workflow, and the generated SVG charts.
  - Four narrative illustrations with recorded prompts, review decisions and file hashes.
  - Five voice notes with a recorded voice selection and stored transcripts.
  - The content adapter and its validation, plus the required-check CI.
  - The research write-up on comparable profile repositories and 2026 GitHub rendering limits.
- Out of scope:
  - Any change to the four featured repositories, to `victoria-lo/*`, or to any repository other than this one and `Pukujan/Pukujan`.
  - Publishing private repository names, counts or activity.
  - A hosted service, a published package, or any benchmark or performance claim.
- Dependencies/uncertainty:
  - The activity block depends on the GitHub REST API. Whether a workflow token can push the refresh to `main` under branch protection was tested and **cannot**; the refresh has to run under the authenticated owner or hand its commit to the owner to merge. Recorded in issue #1.
  - The GitHub Pages tour URL only resolves once Pages is enabled on `main` `/docs`; until then the page states the URL as the intended target.
  - Whether GitHub keeps rendering repository-hosted SVG through `<img>` was verified by live repository evidence, not by a published contract.

## Acceptance criteria

- [x] `https://github.com/Pukujan` renders the mirrored page with the hero illustration, the four project sections, the shipped/not-shipped table, and the live activity block.
- [x] `scripts/track_activity.py` regenerates commit counts, the current project, star totals and the repository index from the GitHub API, and two consecutive runs over unchanged data produce byte-identical output.
- [x] The required `gates` check passes on the publishing pull request, and auto-merge lands it with zero approvals.
- [x] `scripts/check_profile_links.py` resolves every relative reference in every Markdown and HTML file and exits zero.
- [x] The content adapter validates against the pinned helper revision, and every narrative asset hash matches the committed file.
- [x] Six narrative illustrations and two five-frame animations ship with recorded prompts, review decisions and committed file hashes.
- [x] The tour page renders at 390, 768 and 1440 pixel widths with zero horizontal overflow, and a vision review of the screenshots confirms the hero framing swap, the animation stacking, and the chart variant swap.
- [x] No published file contains a secret, a private repository name, or a claim the linked repositories cannot support.

## Evidence and sources

Repository state at the revision recorded in the checkpoint:

- `python -m continuity validate --root .` → `VALID`.
- `python <cgm-0.5.7>/scripts/validate_content_system.py --root <cgm-0.5.7> --adapter .content-system --project-root .` → `CGM_VERIFY mode=helper status=OK` then `VALID`, exit 0.
- `python <acs>/modules/coordination/multi-agent-hotload/v0.1.0/scripts/hotload_check.py --cgm-root <cgm-0.5.7> --adopter-root .` → `hotload_check: OK`, `cgm_validate=VALID`, exit 0.
- `python <cgm-0.5.7>/scripts/verify_hsw_applied.py --root <cgm-0.5.7> --mode acs-html --html docs/index.html` → `VALID: HSW always-on contract OK and HTML tell scan clean`, exit 0.
- `python scripts/check_profile_links.py` → `VALID: 30 local reference(s) resolved`, exit 0.
- Pinned helper revisions: content-generation-modules `c069613ca8b3e02bcf5aba1960160583537f8a3a` (0.5.7); project-continuity-modules `4e2385474b4af9249ca009cbdcb38c4498932475` (CLI 0.6.0).
- Responsive check in Chromium against `http://127.0.0.1:8791/docs/index.html`: horizontal overflow 0 at 390, 768 and 1440 pixels; the portrait hero served at 390 and the wide hero at 768 and 1440; the narrow charts served at 390 and the wide charts above that; 5 audio players and 8 images present at every width with 0 broken.
- `GITHUB_TOKEN=$(gh auth token) python scripts/track_activity.py --days 14` run twice over unchanged data → the seven written files byte-identical (compared by SHA-256), exit 0 both times.

External claims and their sources are recorded in `docs/research/github-profile-pages.md`, with the service probes and the render-limit findings attributed to the GitHub documentation and the linked community discussions.

## Reproduction details

- Starting revision: the empty default branch of `Pukujan/stylish-profile`, created 2026-10-01.
- Runtime: Python 3.12.10 on Windows; the CI job runs Python 3.12 on `ubuntu-latest`. Chart rendering and screenshot capture used Chromium through Playwright; animation frames were assembled with Pillow 12.3.0.
- Exact commands: see Evidence and sources. Each was run against the working tree at the revision recorded in the checkpoint, and each is reproduced verbatim in `.github/workflows/gates.yml`.
- Observed result: every command exited zero with the output quoted above.
- Limitations: the GitHub Pages tour URL was not live at the time of the checkpoint, and the scheduled activity workflow had not yet run on its cron.

## Related records

- Required leaf owning issue, parent ancestry and dependencies: [issue #1](https://github.com/Pukujan/stylish-profile/issues/1) is the leaf; parent: none; dependencies: none.
- Primary writer / branch / source issue revision / as-of status: `omp@windows-workstation`; branch `task/SP-0001-profile-page`; source issue revision is the issue body as created 2026-10-01; status active as of 2026-10-01.
- Related PR/CI evidence and push receipt: recorded in the checkpoint log below after the push.

## Checkpoint log

- 2026-10-01, omp@windows-workstation: every acceptance criterion above was verified against the live repository before this task was closed. The page has since moved to a second shape - a projects table with a spoken note per project, every image animated, dark variants derived - which is tracked separately as SP-0002 rather than reopened here.


## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
