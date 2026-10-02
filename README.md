# Stylish Profile

A profile page for [github.com/Pukujan](https://github.com/Pukujan) that explains four projects and shows live activity, instead of showing a wall of statistics cards.

## Why this exists

Open the old profile page and the loudest element was a pair of third-party statistics images. They reported commit counts and language shares. They told a visitor nothing about what any project does, and they rendered whatever that service decided to render that day. Two of the services behind them now return payment errors and one no longer resolves.

**A reader deciding whether the work is worth an hour got no help from the one page built to help them.** This repository builds the replacement, and it draws its own numbers rather than borrowing someone else's.

## What this project is

One Markdown page, a static HTML tour, six hand-drawn illustrations plus an avatar, eight short animations, four generated charts, and nine spoken notes. The page opens by saying who this is and what the work is, presents four featured projects each with a spoken note, then explains how the work gets done, what tools it uses, and what changed recently.

It is a static entry point. No runtime, no build step, no server, no database. The only moving part is a scheduled script that reads public GitHub data and commits a chart.

## What you can make or use

- **The profile page** at [`profile/README.md`](profile/README.md), written to be mirrored into the `Pukujan/Pukujan` profile repository so it renders at `github.com/Pukujan`.
- **A spoken tour** at [`docs/index.html`](docs/index.html), a static page that plays every voice note with a real audio player, one beside each project. GitHub strips `<audio>` from Markdown, so a page is the only place the clips can actually play; the profile page links to the same files.
- **Six narrative illustrations** under [`assets/profile/`](assets/profile), each generated against a recorded visual contract and reviewed before acceptance. Each one also ships as an animation under [`assets/profile/anim/`](assets/profile/anim), built by `scripts/build_motion_gif.py` from frames generated against the still, with a ping-pong return so the loop does not snap. The hero ships in a wide and a phone framing.
- **A dark variant of every image**, derived from the light asset by `scripts/derive_dark_assets.py` rather than generated again, so the two stay in step and the transform is reproducible.
- **Four generated charts** under [`assets/profile/generated/`](assets/profile/generated), two layouts each in a light and a dark palette, redrawn from live GitHub data on a daily schedule.
- **A research write-up** at [`docs/research/github-profile-pages.md`](docs/research/github-profile-pages.md) covering what comparable profile repositories do and what a GitHub README can and cannot render in 2026.

## What the page says about recent work

The page carries a tracking block that refreshes itself: commits in the window across the featured projects, a row per project showing when it last received a push, a chart of daily commits, and the project with the most commits this week. It closes with a link to the full repository list rather than an inline dump of it.

[`scripts/track_activity.py`](scripts/track_activity.py) draws that block and the charts. It reads commit history from the GitHub REST API, renders the charts as SVG with hand-written markup, and rewrites only the text between the two tracking markers in `profile/README.md` and `docs/index.html`.

- It is **idempotent**: two runs against unchanged data produce byte-identical files, so a scheduled run that finds nothing new commits nothing.
- It **fails closed**: a missing or duplicated marker pair aborts the run and writes no files.
- It **strips its own source of noise**: an empty repository returns HTTP 409 from the commits endpoint and is recorded as zero commits rather than crashing the run.
- The bars in the charts animate once on load using SVG animation, and the finished geometry is written on the shapes themselves, so a renderer that ignores animation still shows the completed chart.

### Why the daily run is a workstation task

Publishing the refresh means pushing to a protected `main`, and the workflow token cannot do that. A `GITHUB_TOKEN` push is rejected by the branch ruleset, and a pull request opened with that token has its `pull_request` runs held for approval by GitHub, which turns a daily refresh into a daily approval step. Neither is a setting that can be turned off.

[`scripts/refresh_profile.ps1`](scripts/refresh_profile.ps1) therefore runs the same steps on the workstation, where the owner's authenticated git credentials carry the ruleset's admin bypass. It fast-forwards, regenerates the block, re-renders the continuity index that pins three of the rewritten files, verifies every link and every recorded hash, checks the rewritten records against the content-system contract, commits only if something changed, pushes, and mirrors the page into `Pukujan/Pukujan`. It is registered as a daily scheduled task and logs to `%LOCALAPPDATA%\stylish-profile-refresh\refresh.log`.

`.github/workflows/track.yml` keeps the same regeneration available on demand, without a schedule, for the case where the page needs refreshing from somewhere other than this machine.

## How it works

1. `.content-system/` records the product brief, the brand language, the visual contract, the asset manifest, and the review rubric.
2. Every illustration is generated from a prompt recorded in `.content-system/prompts/`, reviewed, and entered in the manifest with its role, dimensions, alt text, crop behavior, rejection conditions, and a SHA-256 hash of the committed file.
3. Voice notes are generated with a recorded voice selection, and their spoken text is stored beside them so the clips can be regenerated. `scripts/generate_voice_notes.py --check` proves the committed clip, its recorded byte count, its manifest hash and its recorded text still agree, that the length printed beside its link on the page is still the length of the clip, and that every transcript the tour page prints under a clip is still that clip's own words rather than a tidied version of them.
4. `scripts/track_activity.py` collects activity data, draws the charts, writes their new hashes back into the asset manifest, and rewrites the tracking block between its two markers. `scripts/check_profile_links.py` walks every Markdown and HTML file, resolves each relative reference, and fails when one points at a file that is not committed; it checks the manifest the same way, failing when a recorded hash no longer matches the file it names.
5. `.github/workflows/gates.yml` runs the continuity record check, the content adapter check, the writing contract check, the link and manifest-hash check, the voice-note and transcript check, and the dark-variant check. `.github/workflows/track.yml` regenerates the activity block on demand. `.github/workflows/auto-merge.yml` arms squash auto-merge on every pull request push. The daily refresh is `scripts/refresh_profile.ps1`, registered as a scheduled task.

## How it adapts

The page is read on phones far more often than on a desk, so nothing here assumes a wide column.

- The hero image ships in two framings. Below 640 pixels the page serves the portrait version through a `picture` element, because the wide file scaled into a phone column renders its subtitle about four pixels tall.
- Both charts ship in two arrangements. The narrow files stack the chart above the project list instead of putting them side by side.
- The motion figures sit side by side on a wide screen and stack below 640 pixels.
- Text sizes, spacing, and the page gutter tighten below 640 pixels.

## Evidence and boundaries

- The page's claims about the four featured projects point at their public repositories. The repositories, not this page, are the evidence.
- The illustrations are illustrations of the story. They are not screenshots, not benchmarks, and not evidence of shipped behavior.
- The activity numbers are read from the public GitHub API and committed with the rest of the page, so a reader can re-run the script and compare. **They are counts, not achievements**, and the page presents them as news rather than as a score.
- Generated images and voice notes carry recorded provenance in `.content-system/asset-manifest.json`. The voice notes are newly generated for this page; no third-party reference audio is published here.
- This page does not claim a support promise, a measured performance figure, or a capability its linked repositories do not demonstrate.

## Try it

```bash
python scripts/check_profile_links.py
python scripts/track_activity.py --dry-run
```

The first command exits non-zero and names the file when a link or image path does not resolve. The second prints exactly what the tracking block would say and writes nothing, so you can compare it against the committed page before trusting it.

### Running the gates locally

`gates` in [`.github/workflows/gates.yml`](.github/workflows/gates.yml) is the one required status check on `main`. Reproduce it before pushing by running the same scripts it runs, from the repository root:

```bash
python scripts/check_profile_links.py
python scripts/generate_voice_notes.py --check
python scripts/derive_dark_assets.py --check
for r in scripts/motion-recipes/*.json; do python scripts/build_locked_motion.py check --recipe "$r"; done
continuity docs render && continuity validate --root .
```

The workflow also runs the continuity record check and the pinned content-system adapter checks, which need that adapter checked out at the revision named in the workflow.

Three ordering rules, each of which cost a red `gates` run to learn:

- **`continuity docs render` and `continuity validate --root .` go last, immediately before the push.** `docs/CONTINUITY_INDEX.md` records a hash for each of eight documents — `PROJECT.md`, `README.md`, `profile/README.md`, `docs/index.html`, `.content-system/asset-manifest.json`, `.content-system/project-brief.json`, `docs/research/github-profile-pages.md` and `.coord/assignment.json`. Editing any one of them after a render leaves the index stale, and the runner re-renders it and disagrees.
- **Do not pass `--blocked ""` to `continuity checkpoint`.** The empty string is written through as `"blocked": [""]`, which the pinned validator rejects as `string shorter than 1`. Omit the flag when nothing is blocked and the record carries an empty array.
- **`derive_dark_assets.py --check` is a byte comparison**, so it only passes when the dark files were derived with the same Pillow, numpy and scipy that `gates.yml` pins. Compare the local versions against those pins before re-deriving, or the runner will reject a file nobody can reproduce.

`gates` also triggers on pushes to `main` and cancels superseded runs, so a green pull-request run does not settle the merge commit: read the run for the exact SHA.

To read the page as it will appear, open [`profile/README.md`](profile/README.md) in a Markdown preview, or open [`docs/index.html`](docs/index.html) directly in a browser for the tour with its audio player.
