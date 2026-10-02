<picture>
<source media="(prefers-color-scheme: dark) and (max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/AI%20Engineer%20phone-dark.gif">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/AI%20Engineer-dark.gif">
<source media="(max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/AI%20Engineer%20phone.gif">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/AI%20Engineer.gif" alt="Animated drawing of an anime-style engineer at a workbench raising a flask of glowing liquid while a comic burst pops behind him and small round robots run across the floor." width="100%">
</picture>

# Hi, I'm Pujan

**I build systems that keep long AI projects from losing their place.** That is the whole job: the rules a project hands a fresh agent, the record of what it has already been through, and the routing that decides which model answers.

My featured project is **[Agent Custom Setup](https://github.com/Pukujan/agent-custom-setup)** — a project hands itself to a fresh agent, and the agent starts with the right rules instead of guessing.

Everything else below grows from that one habit: leave a trail behind you.

## The market

The work is document-heavy AI systems: a contract, a filing, a case file, a policy pack. The models are good enough for it now. The failure has moved somewhere else.

**Long projects rarely fail because the work was too hard.** They fail because something got dropped: a decision nobody wrote down, a check nobody ran, a handoff nobody made.

That shows up in four places. A fresh agent starts from a blank prompt and confidently invents a workflow. A pipeline is trusted because it ran once, and nobody can say what it produced last week. A page or an image reads like a template, because nothing decided how it should sound. And the choice of which model answers lives in twenty call sites, so it cannot change when the provider does.

## What I do about it

I build one small tool for each of those four places, and I build each one once so it can be reused.

- **A session starts from the rules your project actually uses, not a blank prompt.** A fresh agent begins with the right contract instead of confidently inventing a workflow.
- **Long work survives a break.** What changed, what was checked and what is still open stays on the record, so the next person does not have to ask.
- **Output sounds like a person, not a template.** Writing and images come out in your voice and your palette, so the result feels made rather than generated.
- **The model route follows a policy.** Which model answers is decided by rule, so it can change when the provider does.

The commits below are the honest version of that claim.

<!-- TRACKING:START -->
## What's fresh

2026-10-02: 7 commit(s) across 3 project(s).

| Project | Last push |
| --- | --- |
| [stylish-profile](https://github.com/Pukujan/stylish-profile) | 2026-10-02 |
| [octo-database](https://github.com/Pukujan/octo-database) | 2026-10-02 |
| [agent-stack-train](https://github.com/Pukujan/agent-stack-train) | 2026-10-02 |

<picture>
<source media="(prefers-color-scheme: dark) and (max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity-narrow-dark.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity-dark.svg">
<source media="(max-width: 640px)" srcset="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity-narrow.svg">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/generated/activity.svg" alt="Daily commit counts across public Pukujan repositories over the last 14 days, 1224 total." width="100%">
</picture>

**Current project:** [agent-custom-setup](https://github.com/Pukujan/agent-custom-setup) with 87 commit(s) in the last 7 days.

[All repositories](https://github.com/Pukujan?tab=repositories).
<!-- TRACKING:END -->

## Featured projects

Four projects, each open on GitHub, each one a piece of the same habit.

- **[Agent Custom Setup](https://github.com/Pukujan/agent-custom-setup)** — a project hands itself to a fresh AI agent, and the agent starts with the right rules instead of guessing. ([listen, 0:27](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Agent%20Custom%20Setup.mp3))
- **[Project Continuity Modules](https://github.com/Pukujan/project-continuity-modules)** — long work survives a break: what changed, what was checked, and what is still open. ([listen, 0:29](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Project%20Continuity%20Modules.mp3))
- **[Content Generation Modules](https://github.com/Pukujan/content-generation-modules)** — writing and images that sound like a person rather than a template. ([listen, 0:25](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Content%20Generation%20Modules.mp3))
- **[Inference Recommendation Engine](https://github.com/Pukujan/inference-recommendation-engine)** — provider-neutral routing for model calls, decided by policy instead of a hard-coded provider. ([listen, 0:22](https://pukujan.github.io/stylish-profile/assets/profile/voice-notes/Inference%20Recommendation%20Engine.mp3))

<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/Projects%20on%20One%20Thread.gif#gh-light-mode-only" alt="Animated drawing of four cards joined by one blue thread, each holding a simple icon for an agent, a continuity trail, a content page and a routing fork, with a dot travelling along the thread." width="100%">
<img src="https://raw.githubusercontent.com/Pukujan/stylish-profile/main/assets/profile/anim/Projects%20on%20One%20Thread-dark.gif#gh-dark-mode-only" alt="Animated drawing of four cards joined by one blue thread, each holding a simple icon for an agent, a continuity trail, a content page and a routing fork, with a dot travelling along the thread." width="100%">

Agent Custom Setup decides what rules a session starts with. Project Continuity Modules decides what survives between sessions. Content Generation Modules decides what the output sounds and looks like. Inference Recommendation Engine decides which model actually answers.

<details>
<summary>More about each project</summary>

### Agent Custom Setup

It pins the versions of the tools a project depends on, so a project cannot silently drift from the versions it claims.

The [live module registry](https://github.com/Pukujan/agent-custom-setup/blob/main/registry.json) lists what it can load, and [POLICY.md](https://github.com/Pukujan/agent-custom-setup/blob/main/POLICY.md) says what it will refuse to do.

*Why it exists:* an agent that starts from a blank prompt will confidently invent a workflow. One that starts from your project's own rules will follow yours.

### Project Continuity Modules

Long work survives a break. What changed, what was checked, and what is still open stays on the record, so the next person does not have to reconstruct it.

*Why it exists:* the expensive failure is not a bad decision. It is a good decision that nobody recorded.

### Content Generation Modules

Writing and images that sound like a person rather than a template. It routes each kind of human-facing output to its own contract, so a page reads like it was written for someone.

*Why it exists:* a page that reads like a brochure is a page nobody finishes. This page is built with it.

### Inference Recommendation Engine

Provider-neutral routing for model calls. It recommends an inference route from an explicit policy instead of a hard-coded provider.

*Why it exists:* provider choice changes monthly. The decision should not live in twenty call sites.

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
