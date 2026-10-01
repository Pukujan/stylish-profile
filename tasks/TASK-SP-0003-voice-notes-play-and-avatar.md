# TASK-SP-0003 — Voice Notes Play And Avatar

<!-- continuity:task {"acceptance":["every voice-note link on the profile page points at a URL that opens and plays in a browser, verified by clicking one on the live page","scripts/check_profile_links.py rejects an audio link that points at a repository blob page, and resolves a Pages-hosted audio link back to the committed file so a missing clip fails the gate","scripts/derive_dark_assets.py --check re-derives each dark illustration and exits non-zero when a committed variant no longer matches its light source","both new checks run in the required gates job","the tour page header shows the account avatar beside the name, loading and circular with no overflow, in both the dark default and the light override","the avatar is recorded in the asset manifest and the filename legend with a prompt record, and the content adapter validates"],"depends_on":["SP-0002"],"goal":"Make every voice note open and play when clicked, verify the derived dark variants cannot go stale, and give the account an avatar drawn as the same character as the page illustrations","id":"SP-0003","issue_url":"https://github.com/Pukujan/stylish-profile/issues/1","next_action":"publish the avatar and the two new checks, then hand the avatar upload to the owner","owner":"Pukujan","priority":"P1","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"active","why":"Nine voice-note links pointed at repository blob pages that have no player, so clicking a note did nothing, and nothing in the suite could see it because the link checker skipped absolute URLs; the account avatar was also a default identicon that belonged to no part of the page's design"} -->

- Status: completed
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

### 2026-10-01 09:37:49 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":["profile/README.md, docs/index.html, docs/research/github-profile-pages.md, assets/profile/Pujan.png, .content-system/asset-manifest.json, .content-system/prompts/Pujan.md, .content-system/filename-legends/profile-page.json, scripts/check_profile_links.py, scripts/derive_dark_assets.py, scripts/refresh_profile.ps1, .github/workflows/gates.yml, tasks/TASK-SP-0002-projects-table-and-voice-notes.md, checkpoints/CURRENT.md"],"completed":["every voice note opens and plays when clicked, the derived dark variants cannot go stale without failing the gate, and the account has an avatar drawn as the same character as the page"],"decisions":["the avatar field is deep royal blue rather than cream or near-black, because cream would be a bright disc on the dark page and near-black would disappear into it, while royal blue is already the page's primary accent and holds its shape against both surrounds"],"evidence":["click-through on the live profile opens a native player and advances currentTime to 5.86s of 26.88s with no error; check_profile_links.py exits 1 on a blob audio link; derive_dark_assets.py --check reports 8 variants matching and exits 1 when one is corrupted; the live tour header loads the avatar at its natural 460x460 as a 56px circle with zero overflow in both themes"],"next_action":"upload the avatar to the account, which is a web-UI action the REST API does not expose, and delete the two throwaway probe repositories","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0003","timestamp":"2026-10-01T09:37:49Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"854a3c87ab2a6dcbdedb7ccc69e74f57b7e9ef80ae0ffcc40901454b89da034e","request_id":"e39780599f674f3188f6e663d18870a6","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0003"} -->

Completed:
- every voice note opens and plays when clicked, the derived dark variants cannot go stale without failing the gate, and the account has an avatar drawn as the same character as the page

Evidence:
- click-through on the live profile opens a native player and advances currentTime to 5.86s of 26.88s with no error; check_profile_links.py exits 1 on a blob audio link; derive_dark_assets.py --check reports 8 variants matching and exits 1 when one is corrupted; the live tour header loads the avatar at its natural 460x460 as a 56px circle with zero overflow in both themes

Decisions:
- the avatar field is deep royal blue rather than cream or near-black, because cream would be a bright disc on the dark page and near-black would disappear into it, while royal blue is already the page's primary accent and holds its shape against both surrounds

Changed:
- profile/README.md, docs/index.html, docs/research/github-profile-pages.md, assets/profile/Pujan.png, .content-system/asset-manifest.json, .content-system/prompts/Pujan.md, .content-system/filename-legends/profile-page.json, scripts/check_profile_links.py, scripts/derive_dark_assets.py, scripts/refresh_profile.ps1, .github/workflows/gates.yml, tasks/TASK-SP-0002-projects-table-and-voice-notes.md, checkpoints/CURRENT.md

Blocked/uncertain:
- none

Next:
- upload the avatar to the account, which is a web-UI action the REST API does not expose, and delete the two throwaway probe repositories

### 2026-10-01 16:42:06 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":["none"],"changed":["profile/README.md, docs/index.html, docs/research/github-profile-pages.md, assets/profile/Pujan.png, .content-system/asset-manifest.json, .content-system/prompts/Pujan.md, .content-system/filename-legends/profile-page.json, scripts/check_profile_links.py, scripts/derive_dark_assets.py, scripts/refresh_profile.ps1, .github/workflows/gates.yml, checkpoints/CURRENT.md"],"completed":["every voice note opens and plays when clicked, the derived dark variants cannot go stale without failing the gate, and the account has an avatar drawn as the same character as the page"],"decisions":["the avatar field is deep royal blue rather than cream or near-black, because cream would be a bright disc on the dark page and near-black would disappear into it, while royal blue is already the page's primary accent and holds its shape against both surrounds"],"evidence":["click-through on the live profile opens a native player and advances currentTime to 5.86s of 26.88s with no error; check_profile_links.py exits 1 on a blob audio link; derive_dark_assets.py --check reports 8 variants matching; the live tour header loads the avatar at its natural 460x460 as a 56px circle with zero overflow in both themes"],"next_action":"upload the avatar to the account, which is a web-UI action the REST API does not expose, and delete the two throwaway probe repositories","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0003","timestamp":"2026-10-01T16:42:06Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"73b8d2ef3711152671e0695bca310d3093fc7c1931c2400baffa858d0a79dcfc","request_id":"ed620bc2732a4218bd23b9b8825d2977","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0003"} -->

Completed:
- every voice note opens and plays when clicked, the derived dark variants cannot go stale without failing the gate, and the account has an avatar drawn as the same character as the page

Evidence:
- click-through on the live profile opens a native player and advances currentTime to 5.86s of 26.88s with no error; check_profile_links.py exits 1 on a blob audio link; derive_dark_assets.py --check reports 8 variants matching; the live tour header loads the avatar at its natural 460x460 as a 56px circle with zero overflow in both themes

Decisions:
- the avatar field is deep royal blue rather than cream or near-black, because cream would be a bright disc on the dark page and near-black would disappear into it, while royal blue is already the page's primary accent and holds its shape against both surrounds

Changed:
- profile/README.md, docs/index.html, docs/research/github-profile-pages.md, assets/profile/Pujan.png, .content-system/asset-manifest.json, .content-system/prompts/Pujan.md, .content-system/filename-legends/profile-page.json, scripts/check_profile_links.py, scripts/derive_dark_assets.py, scripts/refresh_profile.ps1, .github/workflows/gates.yml, checkpoints/CURRENT.md

Blocked/uncertain:
- none

Next:
- upload the avatar to the account, which is a web-UI action the REST API does not expose, and delete the two throwaway probe repositories

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
