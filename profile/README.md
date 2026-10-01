<picture>
<source media="(max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/AI%20Engineer%20phone.png">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/AI%20Engineer.png" alt="Hand-drawn illustration of an engineer at a workbench slotting one reusable block into a growing modular machine while three small round companions carry identical blocks and a second smaller copy of the same structure stands finished beside it." width="100%">
</picture>

# Pujan

**AI engineer.** I automate the repetitive parts of engineering work, and I do it by building one component well and reusing it: reusable agent infrastructure, repeated pipeline stages, and the contracts that keep them honest.

Most of what is on this page is infrastructure I use every day — **Agent Custom Setup**, **Project Continuity Modules**, **Content Generation Modules**, and **Inference Recommendation Engine**. They exist because I got tired of rebuilding the same scaffolding in every project.

**Long projects rarely fail because the work was too hard.** They fail because something got dropped: a decision nobody wrote down, a check nobody ran, a handoff nobody made. So I automate the parts that would otherwise be dropped.

[Read the research behind this page](https://github.com/Pukujan/stylish-profile/blob/main/docs/research/github-profile-pages.md) · [Listen to the tour](https://pukujan.github.io/stylish-profile/docs/) · [Open the issues](https://github.com/Pukujan/stylish-profile/issues)

## Current projects

Document-heavy AI means the input is a contract, a filing, a case file, or a policy pack, and the output has to survive someone checking it. That work has two hard parts: making a model useful on messy real documents, and keeping a long project honest about what has actually been verified. **Everything below is tooling for the second part, plus the routing layer that decides which model or pipeline actually runs.**

### Agent Custom Setup — [repository](https://github.com/Pukujan/agent-custom-setup)

A project hands itself to a fresh AI agent and the agent starts with the right rules instead of guessing. It pins the versions of the tools a project depends on, checks that the pinned code is the code that actually loaded, and **fails the install when it is not**. It is the reason this page's own repository cannot silently drift from the versions it claims.

*Why it exists:* an agent that starts from a blank prompt will confidently invent a workflow. One that starts from a checked contract will follow yours.

### Project Continuity Modules — [repository](https://github.com/Pukujan/project-continuity-modules)

Long work survives a break. Checkpoints record what changed, what was verified, and what is still open; **a GitHub issue owns the scope**; a pull request can only merge after the required checks pass, and a missing or skipped check fails closed rather than open.

*Why it exists:* the expensive failure is not a bad decision. It is a good decision that nobody recorded.

### Content Generation Modules — [repository](https://github.com/Pukujan/content-generation-modules)

Writing and images that sound like a person rather than a template. It routes each kind of human-facing output to its own contract, keeps generated filenames speakable, and records where every image came from: its prompt, its role, its dimensions, and the review that accepted it.

*Why it exists:* a page that reads like a brochure is a page nobody finishes. This page is built with it.

### Inference Recommendation Engine — [repository](https://github.com/Pukujan/inference-recommendation-engine)

Provider-neutral routing for model calls. It recommends an inference route from an explicit policy instead of a hard-coded provider, and it is tested with property-driven tests rather than example fixtures.

*Why it exists:* provider choice changes monthly. The decision logic should not live in twenty call sites.

## What is shipped, and what is not

"Shipped" here means three things: a public repository, a passing check suite, and a written record of what the thing does **not** do yet. Nothing on this page claims a support promise.

| Project | State | Evidence |
| --- | --- | --- |
| Agent Custom Setup | **In daily use** | Public registry of modules, a required-check workflow, 11 open issues tracking what is unfinished |
| Project Continuity Modules | **In daily use** | Published CLI and protocol spec, 31 open issues, adopted by the repositories on this page |
| Content Generation Modules | **In daily use** | Versioned module set with a validator, a changelog, and a released tag; this page's assets are built against it |
| Inference Recommendation Engine | **Working, still moving** | MIT licensed, property-driven test suite, 14 open issues |
| design-bakery.com | **Live** | The site this page's palette and shapes come from |

What is **not** shipped: no hosted service, no package on a public registry, and no benchmark result. Where I have not measured something, I say so instead of implying it.

## Featured project

### Agent Custom Setup

**Why this one:** it is the piece the other three sit on. Every other repository here starts a session by loading it, so if it is wrong, everything downstream is wrong in a way that looks fine.

It is also the smallest honest example of the habit: a version pin, a check that the pin is what actually loaded, and a hard failure when it is not. **No dashboards, no badges, no trust-me.**

- Repository: [github.com/Pukujan/agent-custom-setup](https://github.com/Pukujan/agent-custom-setup)
- Live module registry: [`registry.json`](https://github.com/Pukujan/agent-custom-setup/blob/main/registry.json)
- Policy: [`POLICY.md`](https://github.com/Pukujan/agent-custom-setup/blob/main/POLICY.md)

<!-- TRACKING:START -->
## What changed today

2026-10-01: 14 commit(s) across 2 project(s).

| Project | Commits today | Last push |
| --- | --- | --- |
| [octo-database](https://github.com/Pukujan/octo-database) | 11 | 2026-10-01 |
| [content-generation-modules](https://github.com/Pukujan/content-generation-modules) | 3 | 2026-10-01 |

<picture>
<source media="(max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity-narrow.svg">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity.svg" alt="Daily commit counts across public Pukujan repositories over the last 14 days, 1185 total." width="100%">
</picture>

**Current project:** [agent-custom-setup](https://github.com/Pukujan/agent-custom-setup) with 91 commit(s) in the last 7 days.

<picture>
<source media="(max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/stars-narrow.svg">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/stars.svg" alt="Public stars: 1 total, 1 repositories with at least one." width="100%">
</picture>

### Stars

Total public stars across tracked repositories: **1**.

That is a small number. The work is early, the count is real, and neither is a reason to round it up.

Starred repositories: [agent-custom-setup](https://github.com/Pukujan/agent-custom-setup) (1).

<details>
<summary>All public repositories</summary>

| Repository | Last push | Language | Stars |
| --- | --- | --- | --- |
| [octo-database](https://github.com/Pukujan/octo-database) | 2026-10-01 | TypeScript | 0 |
| [content-generation-modules](https://github.com/Pukujan/content-generation-modules) | 2026-10-01 | Python | 0 |
| [stylish-profile](https://github.com/Pukujan/stylish-profile) | 2026-10-01 | - | 0 |
| [inference-recommendation-engine](https://github.com/Pukujan/inference-recommendation-engine) | 2026-09-30 | Python | 0 |
| [agent-custom-setup](https://github.com/Pukujan/agent-custom-setup) | 2026-09-30 | HTML | 1 |
| [vastai-gpu-broker](https://github.com/Pukujan/vastai-gpu-broker) | 2026-09-30 | Python | 0 |
| [omp-gui](https://github.com/Pukujan/omp-gui) | 2026-09-29 | JavaScript | 0 |
| [project-continuity-modules](https://github.com/Pukujan/project-continuity-modules) | 2026-09-29 | Python | 0 |
| [agent-secret-vault](https://github.com/Pukujan/agent-secret-vault) | 2026-09-28 | - | 0 |
| [doc-generation-modules](https://github.com/Pukujan/doc-generation-modules) | 2026-09-28 | HTML | 0 |
| [Study-os](https://github.com/Pukujan/Study-os) | 2026-09-28 | Python | 0 |
| [hades-product](https://github.com/Pukujan/hades-product) | 2026-09-27 | Python | 0 |
| [multi-agent-modules](https://github.com/Pukujan/multi-agent-modules) | 2026-09-27 | Python | 0 |
| [jev-classifier](https://github.com/Pukujan/jev-classifier) | 2026-09-26 | Python | 0 |
| [research-action](https://github.com/Pukujan/research-action) | 2026-09-25 | TypeScript | 0 |
| [Eval-lab](https://github.com/Pukujan/Eval-lab) | 2026-09-25 | Python | 0 |
| [design-bakery](https://github.com/Pukujan/design-bakery) | 2026-09-24 | TypeScript | 0 |
| [exportable-harness-modules](https://github.com/Pukujan/exportable-harness-modules) | 2026-09-24 | Python | 0 |
| [harness-on-steroids](https://github.com/Pukujan/harness-on-steroids) | 2026-09-23 | Python | 0 |
| [custom-extensions](https://github.com/Pukujan/custom-extensions) | 2026-09-21 | JavaScript | 0 |
| [test-repo](https://github.com/Pukujan/test-repo) | 2026-09-20 | Python | 0 |
| [automated-agents](https://github.com/Pukujan/automated-agents) | 2026-09-16 | - | 0 |
| [fossil-demo](https://github.com/Pukujan/fossil-demo) | 2026-09-15 | - | 0 |
| [fluffy-system](https://github.com/Pukujan/fluffy-system) | 2026-09-14 | JavaScript | 0 |
| [fossil-core](https://github.com/Pukujan/fossil-core) | 2026-09-14 | Python | 0 |
| [ai-for-good](https://github.com/Pukujan/ai-for-good) | 2026-09-14 | TypeScript | 0 |
| [healthcare-documents](https://github.com/Pukujan/healthcare-documents) | 2026-09-13 | - | 0 |
| [research-assurance-v2](https://github.com/Pukujan/research-assurance-v2) | 2026-09-11 | Python | 0 |
| [project-assurance-modules](https://github.com/Pukujan/project-assurance-modules) | 2026-09-07 | Python | 0 |
| [study-os-pedagogical-IR](https://github.com/Pukujan/study-os-pedagogical-IR) | 2026-09-05 | Python | 0 |
| [study-os-benchmarker](https://github.com/Pukujan/study-os-benchmarker) | 2026-09-05 | Python | 0 |
| [RA-plugin](https://github.com/Pukujan/RA-plugin) | 2026-09-03 | Python | 0 |
| [interview-os-game](https://github.com/Pukujan/interview-os-game) | 2026-09-03 | - | 0 |
| [legalgraph-rag-test](https://github.com/Pukujan/legalgraph-rag-test) | 2026-09-02 | Python | 0 |
| [time-to-crawl](https://github.com/Pukujan/time-to-crawl) | 2026-09-01 | Python | 0 |
| [Pukujan](https://github.com/Pukujan/Pukujan) | 2026-06-26 | - | 0 |
| [litigation-prompt-engineering](https://github.com/Pukujan/litigation-prompt-engineering) | 2026-05-29 | JavaScript | 0 |

</details>
<!-- TRACKING:END -->

## How the pieces fit together

<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/Three%20Projects%20One%20Thread.png" alt="Hand-drawn diagram of three cards joined by one blue thread, each card holding a simple icon for an agent, a continuity trail, and a content page." width="420">

**Agent Custom Setup decides what rules a session starts with.** **Project Continuity Modules decides what survives between sessions.** **Content Generation Modules decides what the output sounds and looks like.** **Inference Recommendation Engine decides which model actually answers.** One habit runs through all four: leave a trail behind you.

## The two habits, moving

<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/Reusable%20Blocks.gif" alt="Animated drawing of one blue block being duplicated until six identical blocks form a two-by-three grid, then the original block turning yellow." width="330"> <img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/One%20Push%20Many%20Pipelines.gif" alt="Animated drawing of a single dot travelling down a stem that forks into three branches, filling a box at the end of each branch." width="330">

On the left: **build it once.** One block, then two, then three, then a grid — and the original one turns yellow to mark which copy the rest came from. On the right: **run it once, get every result.** One push travels down the stem, the stem forks, and each branch finishes on its own.

Those are the two things I actually automate. Everything else on this page is downstream of them.

## Why this page looks the way it does

<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/The%20Badge%20Wall.png" alt="Hand-drawn illustration of a small round companion holding an empty magnifying glass in front of a dense wall of blank badge and statistics cards." width="100%">

My previous profile page led with third-party statistics cards. Those cards were the loudest thing on the page, and a visitor learned nothing from them about what any project does — worse, two of the services behind them now return payment errors and one no longer resolves. So this page leads with the work instead, and the only live elements are ones I generate and commit myself.

The illustrations are drawn from the palette and the flat hand-drawn shapes of my own site, [design-bakery.com](https://www.design-bakery.com). They are illustrations of the story, not screenshots, and not evidence of anything.

## What you can check

<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/What%20You%20Can%20Check.png" alt="Hand-drawn illustration of a stack of blank source cards feeding down into an open book and a pair of headphones, with a small round companion holding a pencil." width="300">

Every claim above points at a public repository, and each of those repositories has an issue tracking what is done and what is not.

- The activity numbers on this page are generated from the GitHub API by [`scripts/track_activity.py`](https://github.com/Pukujan/stylish-profile/blob/main/scripts/track_activity.py) and committed by a scheduled workflow. You can re-run it and get the same numbers.
- The illustrations are generated, and their prompts and review decisions are recorded in this repository.
- **Nothing here is a benchmark result, and no number on this page is a performance claim.**

## Listen instead

Short voice notes, if you would rather hear the story than read it:

- **[Welcome to My Corner](https://github.com/Pukujan/stylish-profile/blob/main/assets/profile/voice-notes/Welcome%20to%20My%20Corner.mp3)** — who is speaking, and what is on this page
- **[Who I Am in Thirty Seconds](https://github.com/Pukujan/stylish-profile/blob/main/assets/profile/voice-notes/Who%20I%20Am%20in%20Thirty%20Seconds.mp3)** — the two things I care about
- **[The Short Tour](https://github.com/Pukujan/stylish-profile/blob/main/assets/profile/voice-notes/The%20Short%20Tour.mp3)** — the projects, in order
- **[Why Loose Ends Matter](https://github.com/Pukujan/stylish-profile/blob/main/assets/profile/voice-notes/Why%20Loose%20Ends%20Matter.mp3)** — the reasoning behind the tooling
- **[What Is Still Being Built](https://github.com/Pukujan/stylish-profile/blob/main/assets/profile/voice-notes/What%20Is%20Still%20Being%20Built.mp3)** — an honest note about what is not finished

The tour page plays all five in a row with a player, and it is easier to listen to than five separate links: **[open the tour](https://pukujan.github.io/stylish-profile/docs/)**.

## Find me

- Site: [design-bakery.com](https://www.design-bakery.com)
- LinkedIn: [in/pujan3645](https://www.linkedin.com/in/pujan3645/)
- Everything else: [github.com/Pukujan](https://github.com/Pukujan?tab=repositories)

<sub>This page and its assets are built and verified in <a href="https://github.com/Pukujan/stylish-profile">Pukujan/stylish-profile</a>.</sub>
