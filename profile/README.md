<picture>
<source media="(prefers-color-scheme: dark) and (max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/AI%20Engineer%20phone-dark.gif">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/AI%20Engineer-dark.gif">
<source media="(max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/AI%20Engineer%20phone.gif">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/AI%20Engineer.gif" alt="Animated drawing of an anime-style engineer at a workbench raising a flask of glowing liquid while a comic burst pops behind him and small round robots run across the floor." width="100%">
</picture>

# Hi, I'm Pujan

**AI engineer.** I automate the repetitive parts of engineering work, and I do it by building one component well and reusing it: reusable agent infrastructure, repeated pipeline stages, and the contracts that keep them honest.

**Long projects rarely fail because the work was too hard.** They fail because something got dropped: a decision nobody wrote down, a check nobody ran, a handoff nobody made. So I automate the parts that would otherwise be dropped.

You can [listen to the tour](https://pukujan.github.io/stylish-profile/docs/) if you would rather hear this than read it.

## Start here

[Agent Custom Setup](https://github.com/Pukujan/agent-custom-setup) is the piece the rest sit on. The other three repositories here begin a session by loading it, so if it hands out the wrong rules, everything downstream is wrong in a way that still looks fine. That is why it comes first, and why it is the one to get right before anything else.

The [live module registry](https://github.com/Pukujan/agent-custom-setup/blob/main/registry.json) lists what it can load, and [POLICY.md](https://github.com/Pukujan/agent-custom-setup/blob/main/POLICY.md) says what it will refuse to do.

## What I'm building

Document-heavy AI means the input is a contract, a filing, a case file, or a policy pack, and the output has to survive someone checking it. That work has two hard parts: making a model useful on messy real documents, and keeping a long project honest about what has actually been verified. **Everything below is tooling for the second part, plus the routing layer that decides which model or pipeline actually runs.**

- **[Agent Custom Setup](https://github.com/Pukujan/agent-custom-setup)** — a project hands itself to a fresh AI agent, and the agent starts with the right rules instead of guessing. ([listen, 0:27](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Agent%20Custom%20Setup.mp3))
- **[Project Continuity Modules](https://github.com/Pukujan/project-continuity-modules)** — long work survives a break: what changed, what was verified, and what is still open. ([listen, 0:29](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Project%20Continuity%20Modules.mp3))
- **[Content Generation Modules](https://github.com/Pukujan/content-generation-modules)** — writing and images that sound like a person rather than a template. ([listen, 0:25](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Content%20Generation%20Modules.mp3))
- **[Inference Recommendation Engine](https://github.com/Pukujan/inference-recommendation-engine)** — provider-neutral routing for model calls, decided by policy instead of a hard-coded provider. ([listen, 0:22](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Inference%20Recommendation%20Engine.mp3))

One habit runs through all four: leave a trail behind you.

<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/Projects%20on%20One%20Thread.gif#gh-light-mode-only" alt="Animated drawing of four cards joined by one blue thread, each holding a simple icon for an agent, a continuity trail, a content page and a routing fork, with a dot travelling along the thread." width="100%">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/Projects%20on%20One%20Thread-dark.gif#gh-dark-mode-only" alt="Animated drawing of four cards joined by one blue thread, each holding a simple icon for an agent, a continuity trail, a content page and a routing fork, with a dot travelling along the thread." width="100%">

Agent Custom Setup decides what rules a session starts with. Project Continuity Modules decides what survives between sessions. Content Generation Modules decides what the output sounds and looks like. Inference Recommendation Engine decides which model actually answers.

<details>
<summary>More about each project</summary>

### Agent Custom Setup

It pins the versions of the tools a project depends on, checks that the pinned code is the code that actually loaded, and **fails the install when it is not**. That check is the reason this page's own repository cannot silently drift from the versions it claims.

*Why it exists:* an agent that starts from a blank prompt will confidently invent a workflow. One that starts from a checked contract will follow yours.

### Project Continuity Modules

Long work survives a break. Checkpoints record what changed, what was verified, and what is still open; **a GitHub issue owns the scope**; a pull request can only merge after the required checks pass, and a missing or skipped check fails closed rather than open.

*Why it exists:* the expensive failure is not a bad decision. It is a good decision that nobody recorded.

### Content Generation Modules

Writing and images that sound like a person rather than a template. It routes each kind of human-facing output to its own contract, keeps generated filenames speakable, and records where every image came from: its prompt, its role, its dimensions, and the review that accepted it.

*Why it exists:* a page that reads like a brochure is a page nobody finishes. This page is built with it.

### Inference Recommendation Engine

Provider-neutral routing for model calls. It recommends an inference route from an explicit policy instead of a hard-coded provider, and it is tested with property-driven tests rather than example fixtures.

*Why it exists:* provider choice changes monthly. The decision logic should not live in twenty call sites.

</details>

## How I work

**Build it once.** One block, then two, then three, then a grid — and the original one turns yellow to mark which copy the rest came from.

<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/Reusable%20Blocks.gif#gh-light-mode-only" alt="Animated drawing of one blue block being duplicated until six identical blocks form a two-by-three grid, then the original block turning yellow." width="100%">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/Reusable%20Blocks-dark.gif#gh-dark-mode-only" alt="Animated drawing of one blue block being duplicated until six identical blocks form a two-by-three grid, then the original block turning yellow." width="100%">

**Run it once, get every result.** One push travels down the stem, the stem forks, and each branch finishes on its own.

<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/One%20Push%20Many%20Pipelines.gif#gh-light-mode-only" alt="Animated drawing of a single dot travelling down a stem that forks into three branches, filling a box at the end of each branch." width="100%">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/One%20Push%20Many%20Pipelines-dark.gif#gh-dark-mode-only" alt="Animated drawing of a single dot travelling down a stem that forks into three branches, filling a box at the end of each branch." width="100%">

Those are the two things I actually automate. Everything else on this page is downstream of them.

## Tools

Python · TypeScript · JavaScript · HTML · Shell · PowerShell · Git · GitHub Actions

<!-- TRACKING:START -->
## What's fresh

2026-10-01: 29 commit(s) across 4 project(s).

| Project | Last push |
| --- | --- |
| [octo-database](https://github.com/Pukujan/octo-database) | 2026-10-01 |
| [stylish-profile](https://github.com/Pukujan/stylish-profile) | 2026-10-01 |
| [content-generation-modules](https://github.com/Pukujan/content-generation-modules) | 2026-10-01 |
| [Pukujan](https://github.com/Pukujan/Pukujan) | 2026-10-01 |

<picture>
<source media="(prefers-color-scheme: dark) and (max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity-narrow-dark.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity-dark.svg">
<source media="(max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity-narrow.svg">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity.svg" alt="Daily commit counts across public Pukujan repositories over the last 14 days, 1200 total." width="100%">
</picture>

**Current project:** [agent-custom-setup](https://github.com/Pukujan/agent-custom-setup) with 91 commit(s) in the last 7 days.

[All repositories](https://github.com/Pukujan?tab=repositories).
<!-- TRACKING:END -->

## Listen instead

Nine short voice notes, if you would rather hear the story than read it. GitHub strips audio markup from a profile page, so these are links: click one and it plays in the browser.

- **[Welcome to My Corner](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Welcome%20to%20My%20Corner.mp3)** (0:16) — who is speaking, and what is on this page
- **[Who I Am in Thirty Seconds](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Who%20I%20Am%20in%20Thirty%20Seconds.mp3)** (0:18) — the two things I care about
- **[The Short Tour](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/The%20Short%20Tour.mp3)** (0:26) — the projects, in order
- **[Why Loose Ends Matter](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Why%20Loose%20Ends%20Matter.mp3)** (0:23) — the reasoning behind the tooling
- **[What Is Still Being Built](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/What%20Is%20Still%20Being%20Built.mp3)** (0:17) — where the work stands today

Each project has its own note too, linked from its row above. The [tour page](https://pukujan.github.io/stylish-profile/docs/) plays all nine in place, each beside the project it belongs to, and that is the easier way to listen.

## Find me

- Site: [design-bakery.com](https://www.design-bakery.com)
- LinkedIn: [in/pujan3645](https://www.linkedin.com/in/pujan3645/)
- Open an issue and ask: [agent setup](https://github.com/Pukujan/agent-custom-setup/issues), [project continuity](https://github.com/Pukujan/project-continuity-modules/issues), [content generation](https://github.com/Pukujan/content-generation-modules/issues), [model routing](https://github.com/Pukujan/inference-recommendation-engine/issues). That is the fastest way to reach me.

<sub>Illustrations drawn from the palette of <a href="https://www.design-bakery.com">design-bakery.com</a>. Page and assets built in <a href="https://github.com/Pukujan/stylish-profile">Pukujan/stylish-profile</a>.</sub>
