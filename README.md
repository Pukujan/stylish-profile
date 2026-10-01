# Stylish Profile

A profile page for [github.com/Pukujan](https://github.com/Pukujan) that explains four projects and shows live activity, instead of showing a wall of statistics cards.

## Why this exists

Open the old profile page and the loudest element was a pair of third-party statistics images. They reported commit counts and language shares. They told a visitor nothing about what any project does, and they rendered whatever that service decided to render that day. Two of the services behind them now return payment errors and one no longer resolves.

**A reader deciding whether the work is worth an hour got no help from the one page built to help them.** This repository builds the replacement, and it draws its own numbers rather than borrowing someone else's.

## What this project is

One Markdown page, a static HTML tour, six hand-drawn illustrations, two short animations, four generated charts, and five spoken notes. The page opens with a sentence about the work, presents four featured projects, then shows what changed today and what is still being built.

It is a static entry point. No runtime, no build step, no server, no database. The only moving part is a scheduled script that reads public GitHub data and commits a chart.

## What you can make or use

- **The profile page** at [`profile/README.md`](profile/README.md), written to be mirrored into the `Pukujan/Pukujan` profile repository so it renders at `github.com/Pukujan`.
- **A spoken tour** at [`docs/index.html`](docs/index.html), a static page that plays all five voice notes with a real audio player. GitHub strips `<audio>` from Markdown, so a page is the only place the clips can actually play.
- **Six narrative illustrations** under [`assets/profile/`](assets/profile), each generated against a recorded visual contract and reviewed before acceptance. The hero ships in a wide and a phone framing, swapped by viewport width.
- **Two five-frame animations** under [`assets/profile/anim/`](assets/profile/anim): one block being reused until it becomes a grid, and one push fanning out into several finished pipelines.
- **Four generated charts** under [`assets/profile/generated/`](assets/profile/generated), redrawn from live GitHub data on a daily schedule.
- **A research write-up** at [`docs/research/github-profile-pages.md`](docs/research/github-profile-pages.md) covering what comparable profile repositories do and what a GitHub README can and cannot render in 2026.

## What changed today

The page carries a tracking block that refreshes itself: commits in the last day grouped by project, the project with the most commits this week, the current star count, and a collapsible table of every public repository.

[`scripts/track_activity.py`](scripts/track_activity.py) draws that block and the four charts. It reads commit history from the GitHub REST API, renders the charts as SVG with hand-written markup, and rewrites only the text between the two tracking markers in `profile/README.md` and `docs/index.html`.

- It is **idempotent**: two runs against unchanged data produce byte-identical files, so a scheduled run that finds nothing new commits nothing.
- It **fails closed**: a missing or duplicated marker pair aborts the run and writes no files.
- It **strips its own source of noise**: an empty repository returns HTTP 409 from the commits endpoint and is recorded as zero commits rather than crashing the run.
- The bars in the charts animate once on load using SVG animation, and the finished geometry is written on the shapes themselves, so a renderer that ignores animation still shows the completed chart.

## How it works

1. `.content-system/` records the product brief, the brand language, the visual contract, the asset manifest, and the review rubric.
2. Every illustration is generated from a prompt recorded in `.content-system/prompts/`, reviewed, and entered in the manifest with its role, dimensions, alt text, crop behavior, rejection conditions, and a SHA-256 hash of the committed file.
3. Voice notes are generated with a recorded voice selection, and their spoken text is stored beside them so the clips can be regenerated.
4. `scripts/track_activity.py` collects activity data, draws the charts, and rewrites the tracking block between its two markers. `scripts/check_profile_links.py` walks every Markdown and HTML file, resolves each relative reference, and fails when one points at a file that is not committed.
5. `.github/workflows/gates.yml` runs the continuity record check, the content adapter check, the writing contract check, and the link check. `.github/workflows/track.yml` runs the tracker on a daily schedule. `.github/workflows/auto-merge.yml` arms squash auto-merge on every pull request push.

## How it adapts

The page is read on phones far more often than on a desk, so nothing here assumes a wide column.

- The hero image ships in two framings. Below 640 pixels the page serves the portrait version through a `picture` element, because the wide file scaled into a phone column renders its subtitle about four pixels tall.
- Both charts ship in two arrangements. The narrow files stack the chart above the project list instead of putting them side by side.
- The two animations sit side by side on a wide screen and stack below 640 pixels.
- Text sizes, spacing, and the page gutter tighten below 640 pixels.

## Evidence and boundaries

- The page's claims about the four featured projects point at their public repositories. The repositories, not this page, are the evidence.
- The illustrations are illustrations of the story. They are not screenshots, not benchmarks, and not evidence of shipped behavior.
- The activity and star numbers are read from the public GitHub API and committed with the rest of the page, so a reader can re-run the script and compare. **They are counts, not achievements**, and the page says so where it shows them.
- Generated images and voice notes carry recorded provenance in `.content-system/asset-manifest.json`. The voice notes are newly generated for this page; no third-party reference audio is published here.
- This page does not claim a support promise, a measured performance figure, or a capability its linked repositories do not demonstrate.

## Try it

```bash
python scripts/check_profile_links.py
python scripts/track_activity.py --dry-run
```

The first command exits non-zero and names the file when a link or image path does not resolve. The second prints exactly what the tracking block would say and writes nothing, so you can compare it against the committed page before trusting it.

To read the page as it will appear, open [`profile/README.md`](profile/README.md) in a Markdown preview, or open [`docs/index.html`](docs/index.html) directly in a browser for the tour with its audio player.
