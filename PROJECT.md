# Stylish Profile — Project Contract

<!-- continuity:project {"id":"stylish-profile","protocol_version":"0.1.0-draft","schema":"project-continuity.project.v1","title":"Stylish Profile"} -->

<!-- pcm:github-progression:start -->
## GitHub-owned progression

GitHub Issues are required for PCM-governed project work and own task scope, acceptance, priority, ownership, dependencies, lifecycle and durable project progression. Merged default-branch history owns accepted code and normative/domain documents; PR checks and merge records own delivery facts. Checked-in PROJECT/CURRENT/TASK/checkpoint/handoff documents are mandatory versioned projections for task state, not a parallel authority. Local files, registries, context packs and chat are ephemeral execution aids. Domain-document ownership stays with the target project.

Every issue progress update MUST link the leaf child issue that owns the work, its parent ancestry and dependencies (or explicitly none). A top-level deliverable identifies itself as the leaf and says parent: none. Create one child per independently deliverable scope, never one per comment. Record task ID, primary writer and branch on the issue before creating its repository projection. Re-read live issues and relevant source revisions before resuming; the issue verifier checks identity/status, not semantic agreement.

Authorized owner/user direction can revise intent: record it on the owning GitHub issue with a correction/supersession link before dependent work. It cannot alter observed CI/merge facts or waive required gates. Stale projections yield to their field's authority. If direction, ownership or evidence conflicts remain unresolved, pause affected work and record uncertainty; continue independent safe work. One primary writer owns each task branch/checkpoint stream. Coordinate shared-document edits through linked issues/PRs, re-read the current base and reconcile concurrent changes; never force-push or overwrite another writer. Issue prose is not an atomic lock.

Label observed results, repository/external evidence, agent reports and inference separately. Preserve contradictory evidence with source/revision and mark conclusions disputed or unknown until resolved. Append correction/supersession evidence; never rewrite checkpoint history. An upstream correction MUST identify affected descendants and assumptions on their issues; pause, re-plan and revalidate dependent work before resuming. Follow explicit parent/dependency links within the affected scope; cycles or unknown lineage block affected claims. No graph database, local canonical ledger or autonomous polling agent is required.

Before every push, synchronize relevant docs and task/checkpoint projections, CURRENT/HANDOFF when affected, and reviewed catalog/generated index. Record leaf/parent/dependency links, source issue/comment revision, as-of status, evidence, blockers and next action. Commit product/docs first; `continuity checkpoint` then commits and synchronously pushes the checkpoint with a stable request ID. After every successful push, manually publish a leaf issue receipt keyed by request ID and exact pushed SHA, linking changed docs/checkpoint, PR, tests and pending gates; add a linked parent progression update. Retry a missing receipt without another checkpoint/push; inspect for the same key before posting. --receipt-repo and --receipt-issue are opt-in and still require a proven lookup; omit them and the receipt stays manual. Automatic issue-comment synchronization is not implemented; issue #67 is CLOSED (owner freeze decision 2026-09-25) and its unmet guaranteed-completion acceptance transferred to #110.

Required CI and GitHub auto-merge are mandatory. Arm auto-merge only after the increment's final push: a later push races the merge window and strands outside accepted history. Verify protection, required reviews/checks on the exact current-base or merge-queue candidate, and auto-merge; missing, failed, skipped, stale or unverified gates fail closed: no completion or cleanup. After CI/merge, append the exact check results, PR/merge SHA and live issue status to the leaf and link the parent update; fetch and verify accepted history. Reconcile material doc/status corrections in a new synchronized increment. Receipt-only transitions need no recursive doc commit: docs retain an explicit as-of/pending state and point to the live issue. Never label local-only or merely pushed work delivered. Preserve unsafe resources and keep incomplete issues open.
<!-- pcm:github-progression:end -->

## Main goal

Publish one profile page at `github.com/Pukujan` that tells a reader what Pujan builds, which projects are real, and what is still unfinished — and keep the page's activity numbers true by regenerating them from the GitHub API on a schedule rather than typing them by hand.

## Why

The previous profile page led with third-party statistics cards. They were the loudest element, they said nothing about what any project does, and the services behind them have since degraded: two return payment errors and one no longer resolves. A reader deciding whether the work deserves an hour got no help from the one page built to help them.

There is a second reason. The featured repositories exist to stop long work from silently drifting — a pinned version, a required check, a recorded decision. A profile page that hand-copies its own numbers into Markdown would contradict the thing it is advertising.

## Scope

- The publishable page at `profile/README.md`, written to be mirrored into `Pukujan/Pukujan` so it renders at `github.com/Pukujan`.
- The static tour page at `docs/index.html`, which plays every voice note beside the project it belongs to, because GitHub strips `<audio>` from Markdown.
- Six narrative illustrations under `assets/profile/`, each generated against a recorded visual contract and reviewed before acceptance, each with a committed animation and a derived dark variant, and each running four frames. Two further figures exist only as animations, because the motion is the point: a block reused until it becomes a grid, and one push fanning out into several finished pipelines. Those two run five frames.
- The auto-tracking layer: `scripts/track_activity.py` and `.github/workflows/track.yml`, which regenerate the commit counts, today's projects, the current project and the activity chart from the GitHub API on a daily schedule and commit the result, alongside `profile/tracking.json` carrying the full data they fetched.
- The content adapter at `.content-system/`, which records the product brief, brand language, visual contract, asset manifest and review rubric.
- `docs/research/github-profile-pages.md`, the recorded comparison of comparable profile repositories and the 2026 GitHub rendering limits.

## Non-goals

- Not a hosted product, service, or package. The repository is the deliverable.
- No third-party runtime on the page: no statistics-card services, no badge CDNs, no icon CDNs.
- No benchmark, performance or adoption claim. The page reports what the GitHub API returns and nothing more.
- Not the home of the featured projects. Agent Custom Setup, Project Continuity Modules, Content Generation Modules and Inference Recommendation Engine each own their own repository, issue log and release process; this repository only links to them and pins their revisions.
- No private repository names, counts or activity anywhere in published output.

## Definition of success

1. `https://github.com/Pukujan` renders the page with its hero illustration, four project sections, the figure showing the habit they share, the activity block and the spoken tour links.
2. The activity block regenerates on schedule without human input, and re-running the generator against unchanged data produces byte-identical output.
3. The required `gates` check passes on the pull request that publishes the page, and auto-merge lands it with zero approvals.
4. Every relative link and image reference in every Markdown and HTML file resolves, verified by `scripts/check_profile_links.py` in CI.
5. The content adapter validates against the pinned helper revision, and each narrative asset carries a prompt record and a hash that matches the committed file.
6. No published file contains a secret, a private repository name, or a claim the linked repositories cannot support.
