# TASK-SP-0003 — Voice Notes Play And Avatar

<!-- continuity:task {"acceptance":["every voice-note link on the profile page points at a URL that opens and plays in a browser, verified by clicking one on the live page","scripts/check_profile_links.py rejects an audio link that points at a repository blob page, and resolves a Pages-hosted audio link back to the committed file so a missing clip fails the gate","scripts/derive_dark_assets.py --check re-derives each dark illustration and exits non-zero when a committed variant no longer matches its light source","both new checks run in the required gates job","the tour page header shows the account avatar beside the name, loading and circular with no overflow, in both the dark default and the light override","the avatar is recorded in the asset manifest and the filename legend with a prompt record, and the content adapter validates"],"depends_on":["SP-0002"],"goal":"Make every voice note open and play when clicked, verify the derived dark variants cannot go stale, and give the account an avatar drawn as the same character as the page illustrations","id":"SP-0003","issue_url":"https://github.com/Pukujan/stylish-profile/issues/1","next_action":"publish the avatar and the two new checks, then hand the avatar upload to the owner","owner":"Pukujan","priority":"P1","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"active","why":"Nine voice-note links pointed at repository blob pages that have no player, so clicking a note did nothing, and nothing in the suite could see it because the link checker skipped absolute URLs; the account avatar was also a default identicon that belonged to no part of the page's design"} -->

- Status: active
- Owner: Pukujan
- Priority: P1
- Depends on: SP-0002

## Goal

Make every voice note open and play when clicked, verify the derived dark variants cannot go stale, and give the account an avatar drawn as the same character as the page illustrations

## Why

Nine voice-note links pointed at repository blob pages that have no player, so clicking a note did nothing, and nothing in the suite could see it because the link checker skipped absolute URLs; the account avatar was also a default identicon that belonged to no part of the page's design

## Allowed files

- profile/README.md
- docs/index.html
- docs/research/github-profile-pages.md
- assets/profile/**
- .content-system/**
- scripts/check_profile_links.py
- scripts/derive_dark_assets.py
- scripts/refresh_profile.ps1
- .github/workflows/gates.yml

## Human outcome

A visitor who clicks a voice note hears it instead of landing on a file viewer with
nothing to press. A regenerated illustration cannot quietly leave a stale dark copy on
the page. The picture beside the name belongs to the same drawing as the page.

## Scope and boundaries

- In scope: the audio delivery path and the gate that guards it; the dark-variant check and
  where it runs; the avatar asset, its record, and its placement in the tour header.
- Out of scope: setting the account avatar, which is a GitHub web-UI action the REST API
  does not expose; and any change to the reference account, which is read-only.
- Dependencies/uncertainty: the voice notes are committed binaries, so the check compares
  them against the record rather than re-synthesising them, which needs the Fish Audio key.

## Acceptance criteria

- [x] every voice-note link on the profile page points at a URL that opens and plays in a browser, verified by clicking one on the live page
- [x] scripts/check_profile_links.py rejects an audio link that points at a repository blob page, and resolves a Pages-hosted audio link back to the committed file so a missing clip fails the gate
- [x] scripts/derive_dark_assets.py --check re-derives each dark illustration and exits non-zero when a committed variant no longer matches its light source
- [x] both new checks run in the required gates job
- [x] the tour page header shows the account avatar beside the name, loading and circular with no overflow, in both the dark default and the light override
- [x] the avatar is recorded in the asset manifest and the filename legend with a prompt record, and the content adapter validates

## Evidence and sources

- Three delivery paths measured on a committed clip: a `blob` URL returns an HTML file
  viewer with no player, `raw.githubusercontent.com` returns
  `content-disposition: attachment`, and the Pages host returns `Content-Type: audio/mp3`.
- Click-through on the live profile: the link opens a native player, duration 26.88 s, and
  `play()` advances `currentTime` to 5.86 s with no error.
- `python scripts/check_profile_links.py` exits 1 with `points at a file-viewer page,
  which cannot play` when one blob link is reintroduced.
- `python scripts/derive_dark_assets.py --check` reports `VALID: 8 dark variant(s) match
  their source`, and exits 1 naming the file when one variant is corrupted.
- The `gates` step list for the merged revision shows both new steps ran and passed.
- The live profile page renders 9 images of 27 in the DOM, 0 broken, 0 overflow, 9 note
  links all on the Pages host, 0 blob links, at 1280 px and 390 px in both themes.

## Reproduction details (only when needed)

Starting revision, material inputs/configuration, runtime, exact command or prompt, observed result, and limitations.

## Related records

- Required leaf owning issue, parent ancestry and dependencies (or explicitly none):
- Primary writer / branch / source issue revision / as-of status:
- Related PR/CI evidence and push receipt (request ID / SHA):

## Checkpoint log

No checkpoints yet.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
