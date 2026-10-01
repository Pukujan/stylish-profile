# What the best GitHub profile pages do, and what GitHub will actually render

Research recorded 2026-10-01, before this page was built. Two questions: which profile
repositories are worth copying, and which rendering techniques survive GitHub's
sanitizer today.

Everything below was read from live sources on that date. Claims that are reasoning
rather than observation are marked **inferred**.

## The comparison set

| Repository | Mechanism | What it gets right | What it costs |
| --- | --- | --- | --- |
| [victoria-lo/victoria-lo](https://github.com/victoria-lo/victoria-lo) | One hand-made GIF hero, 20 adjacent shields.io badges, a daily Action that refreshes a blog list | The visual weight is one bespoke illustration nobody else can copy; the only live element is five lines of text | 21 external requests per view; badge labels are empty, so a screen reader reads the URL |
| [platane/platane](https://github.com/platane/platane) | A contribution-grid snake committed as an animated SVG, served as two variants through `<picture>` | Zero third-party runtime; the motion is entirely the owner's | Needs a scheduled Action to regenerate the SVG |
| [DenverCoder1/DenverCoder1](https://github.com/DenverCoder1/DenverCoder1) | Six `<details>` sections plus a typing SVG | Real density without a wall of scroll | The typing SVG is one hobby deployment away from disappearing |
| [ryanpolasky/ryme.md](https://github.com/ryanpolasky/ryme.md) | A browser tool that emits profile banners as SVG with CSS `@keyframes` baked into the file | Proves an SVG referenced by `<img>` animates on github.com with no JavaScript | The generator is a separate product to maintain |

**The pattern:** the pages that hold up are the ones whose visual weight is a file in
their own repository. The pages that decay are the ones whose visual weight is somebody
else's server.

## What GitHub renders in 2026

GitHub converts Markdown to HTML and then sanitizes it, removing "things that could harm
you… such as `script` tags, inline-styles, and `class` or `id` attributes"
([github/markup](https://github.com/github/markup)).

**Stripped:** inline `<svg>`, `<script>`, `<style>`, `<iframe>`, `<embed>`, `<object>`
content, `<audio>`, `<video>` with an arbitrary source, and every inline `style=`
attribute.

**Alive:** `<img src alt width height align>`, `<picture>` with
`<source media srcset>`, `<details>` and `<summary>`, `<a href>`, tables, headings, and
the `#gh-dark-mode-only` / `#gh-light-mode-only` URL fragment pair. The `<picture>`
theme mechanism is documented in
[GitHub's own guide](https://github.blog/developer-skills/github/how-to-make-your-images-in-markdown-on-github-adjust-for-dark-mode-and-light-mode/).

**The SVG workaround:** inline SVG is dead, but an SVG stored as a file and referenced
through `<img>` loads in image context and animates. This is what platane's snake does.
Verified here rather than assumed: a generated chart's bars were sampled at 110 ms
intervals inside the embedded SVG and grew from zero to their final heights over about
1.3 seconds, then held. A renderer that ignores the animation still shows the finished
chart, because the final geometry is written on the shapes themselves.

**Motion means GIF, not APNG.** GitHub's Markdown renderer marks a `.gif` image with
`data-animated-image`. It does not mark `.apng`, `.png`, `.webp` or `.jpg`. An APNG
therefore displays as a single frozen frame, which is why every animation on this page
is a GIF.

**Responsive images survive the sanitizer.** A `<picture>` element with a
`<source media="(max-width: 640px)">` and a fallback `<img>` is passed through intact;
GitHub wraps the pair in a `<themed-picture data-catalyst-inline="true">` element and
the browser still performs the swap. Measured on this repository: at a 1200 px viewport
the wide chart loaded (`naturalWidth 1000`), and at 390 px the narrow file loaded and
rendered at exactly the column width with zero horizontal overflow. That is the
mechanism behind the two hero framings and the two chart arrangements.

**One 2026 regression worth knowing:** since roughly April 2026 GitHub renders
*external* CDN SVGs as block elements, which breaks any "row of inline icons" layout,
and `display:inline` cannot fix it because inline styles are stripped
([discussion #192845](https://github.com/orgs/community/discussions/192845),
[#193030](https://github.com/orgs/community/discussions/193030)). Icons hosted inside
the repository are unaffected.

## Service risk, probed live

| Service | Status on 2026-10-01 |
| --- | --- |
| `github-readme-stats.vercel.app` | Alive, but its own README calls the public instance "best-effort" and rate-limited |
| `streak-stats.demolab.com` | Alive; the old Heroku deployment is dead |
| `img.shields.io` static badges | Alive; the `/github/…` dynamic endpoints share a rate limit and return 429s |
| `github-readme-activity-graph.vercel.app` | **HTTP 402** — behind a Vercel billing wall |
| `github-profile-trophy.vercel.app` | **HTTP 402** |
| `profile-summary-for-github.com` | **DNS no longer resolves** |

Four of the services that profile pages commonly embed were dead or degraded on the day
of this check. The old `Pukujan/Pukujan` page depended on one of them.

## Audio

`<audio>` is stripped from Markdown, so a repository README cannot play a clip. Two
mechanisms work in practice:

1. A static page with `<audio controls>`, typically on GitHub Pages.
2. An audio-only MP4 uploaded through GitHub's web editor, which becomes a
   `user-attachments` URL that renders as an inline player. It starts muted and needs a
   manual upload through the web UI.

A link to the file's blob page on github.com does **not** open a player for audio. It
renders the file viewer, whose only controls are Raw and View raw, so a voice note
linked that way does nothing when clicked. This was wrong on the first version of this
page and stayed wrong because the link checker skipped absolute URLs. The three
delivery paths, measured on a committed MP3:

| URL form | Response | On click |
| --- | --- | --- |
| `github.com/.../blob/main/....mp3` | HTML file viewer | nothing |
| `raw.githubusercontent.com/...mp3` | `content-disposition: attachment` | downloads |
| `pukujan.github.io/stylish-profile/...mp3` | `Content-Type: audio/mp3` | plays |

Only the last one plays on click, so the notes are linked from the Pages host. The
checker now resolves Pages-hosted audio back to the committed file and rejects a blob
link with the reason.

## What this page does, and why

- **No third-party runtime dependency.** No statistics cards, no badge services, no
  icon CDNs. The only external references are the four project repositories, the GitHub
  profile, a LinkedIn profile and one personal site; every image and every clip is
  served from this repository.
- **Repo-hosted illustrations.** Seven raster images - six narrative illustrations and
  the avatar - generated against a recorded visual contract, with their prompts, roles,
  dimensions, alt text, crop behavior and review decisions stored in
  `.content-system/`. Raster rather than SVG because the contract requires narrative
  assets to carry a real prompt record and a verified file hash. The hero also ships a
  phone framing, so the wide file is never scaled into a phone column.
- **The illustrations move.** All six narrative illustrations also ship as a GIF whose
  frames were generated one at a time from the previous frame, then assembled on a
  shared palette with a ping-pong return so the loop does not snap; the avatar is the
  one raster image that stays still. Two further figures - a block reused until it
  becomes a grid, and one push fanning out into several finished pipelines - exist
  only as animations, because the motion is the point. Between them they show the
  two habits the page describes.
- **Charts drawn by the repository itself.** Four SVGs written by a committed script
  from live GitHub API data - two layouts, each in a light and a dark palette.
- **Dark variants are derived, not drawn again.** A transform reads each light asset
  and writes its dark twin, so the two cannot drift and the result is reproducible from
  the committed source. A second generation pass would cost a model call per frame and
  would not be byte-stable. The transform darkens the paper only: an earlier version
  inverted every pixel's lightness, which turned the character's cream skin black
  because the skin and the paper are the same colour. Finding the paper by its
  connection to the frame edge is what keeps the drawing's own colours intact.
- **The argument is open; the detail is folded away.** On the profile page the projects
  section lists each repository as one line with a link to its spoken note, and the long
  description of all four sits behind a single `<details>`. The tour page presents the
  same four as a table of name, one line and repository link. A reader who wants the
  argument never opens the fold; a reader who wants the reasoning can. The tour page
  uses `<details>` for the voice-note transcripts.
- **GitHub Pages for audio.** The nine voice notes live on a static tour page with real
  players, one beside each project, because Markdown cannot host one.
- **Two theme mechanisms, never combined.** GitHub's theme rule matches the anchor it
  wraps around a bare image, so an image inside a `<picture>` never swaps colour: both
  modes render at once. A bare image with the theme fragment tracks GitHub's own toggle
  exactly but cannot carry a phone variant, and `<picture>` sources are the only form
  that can swap colour and layout together. Illustrations use the first, charts the
  second, and no figure mixes them.
- **A link check in CI.** Every relative reference in every Markdown and HTML file is
  resolved during the required `gates` check, so a renamed asset cannot silently turn
  into a broken image on the profile. It also resolves Pages-hosted audio back to the
  committed clip and rejects a blob link, because a blob link looks correct in Markdown
  and does nothing in a browser.
- **A dark-variant check in CI.** The dark illustrations are derived from the light ones
  by a committed transform, so the check re-derives each one and compares bytes. The
  transform is deterministic, which makes that a real test: a regenerated light picture
  cannot leave its dark twin behind.

## Delivering an auto-refreshing block

An activity block that regenerates itself has to get its commit onto `main`, and branch
protection decides whether that is possible. Probed live on 2026-10-01:

- A workflow running as `github-actions[bot]` **cannot create a pull request** even with
  `contents: write` and `pull-requests: write`. GitHub refuses with "GitHub Actions is
  not permitted to create or approve pull requests". Flipping
  `can_approve_pull_request_reviews` on the repository lifts that specific refusal.
- The same bot **cannot push to a protected `main`**, and it does not inherit a
  repository-admin bypass actor on the ruleset. A push by the authenticated owner with
  the same ruleset active succeeds and prints `Bypassed rule violations`.
- A pull request opened by the bot can be armed for auto-merge, and a workflow run
  dispatched against its head branch does produce the required check run — but in the
  probe window the pull request stayed blocked with an empty status rollup. The check
  that satisfies branch protection has to come from the pull request's own events. When
  it does, the pull request merges with no approval of the *merge* — a probe pull
  request reached `MERGED` at `2026-10-01T06:34:43Z` with `gates` green and nobody
  clicking anything. What it did need was one approval of the *workflow run*.

The practical conclusion, and it took a live probe to reach: **a workflow token cannot
complete this loop on its own.** The blocking piece is not branch protection but the
approval gate on `pull_request` runs created with `GITHUB_TOKEN`, which GitHub applies by
design and which no repository setting disables. A bot-opened pull request does merge
with zero approvals once its check has reported — verified end to end — but the check
cannot report without someone releasing the held run first. A scheduled refresh that
needs a human every day is not a scheduled refresh.

So the daily regeneration runs on the workstation, under the owner's authenticated
credentials, which do carry the ruleset bypass. The workflow keeps the same regeneration
available on demand, without a schedule, and opens a pull request for the case where it
is run from somewhere else.

## What remains unverified

- GitHub publishes no machine-readable sanitizer whitelist, so the "alive" list is
  assembled from documentation plus live repository evidence.
- GitHub Mobile's fidelity for animated SVG was not established.
- Whether GitHub's theme and the operating system's `prefers-color-scheme` can disagree
  in a way that picks the wrong `<picture>` variant was not tested, because this page
  ships no theme-paired images.
