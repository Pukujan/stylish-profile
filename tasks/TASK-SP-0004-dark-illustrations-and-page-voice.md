# TASK-SP-0004 — Dark Illustrations And Page Voice

<!-- continuity:task {"acceptance":["every dark illustration keeps the character's own colours, has a visible edge against a #0f0f0f page, and shows readable text, confirmed on the rendered page rather than on the file alone","scripts/derive_dark_assets.py --check re-derives all eight variants and exits 0, and exits 1 naming the file when one variant is corrupted","the required gates job installs what the new transform imports, so the dark check runs rather than erroring on a missing module","no heading on either the profile page or the tour page is a disclaimer, and neither page carries a State-and-Evidence table","the tracking block still regenerates byte-identically, so a second run over unchanged data rewrites no bytes","the tour page loads the light assets under prefers-color-scheme light and the dark assets otherwise, with zero broken images and zero horizontal overflow","the content adapter validates after the retired chart assets are removed from the manifest and the filename legend"],"depends_on":["SP-0003"],"goal":"Make the dark illustrations look like the drawings they came from, and rewrite the profile page so a visitor is welcomed instead of handed an audit trail","id":"SP-0004","issue_url":"https://github.com/Pukujan/stylish-profile/issues/11","next_action":"ship the branch and open the pull request","owner":"omp@windows-workstation","priority":"P1","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"active","why":"The dark copies were built by inverting every pixel's lightness, so the character's cream skin went black, the black hair went white, and each figure came out as a photographic negative with a background indistinguishable from the page behind it; the page itself opened on a table describing its own sections, carried a State-and-Evidence table, and spent a paragraph defending a star total of one"} -->

- Status: active
- Owner: omp@windows-workstation
- Priority: P1
- Depends on: SP-0003

## Goal

Make the dark illustrations look like the drawings they came from, and rewrite the profile page so a visitor is welcomed instead of handed an audit trail

## Why

The dark copies were built by inverting every pixel's lightness, so the character's cream skin went black, the black hair went white, and each figure came out as a photographic negative with a background indistinguishable from the page behind it; the page itself opened on a table describing its own sections, carried a State-and-Evidence table, and spent a paragraph defending a star total of one

## Allowed files

- profile/README.md
- docs/index.html
- assets/profile/**
- .content-system/**
- scripts/derive_dark_assets.py
- scripts/track_activity.py
- .github/workflows/gates.yml
- tasks/**
- checkpoints/**

## Human outcome

Opening the profile in dark mode shows the same drawings as in light mode, with the
character's face, hair and clothes intact and the text still readable, so the picture reads
as a deliberate panel rather than a negative. Opening it in either mode meets a person who
says what they build, not a record of what has been verified about them.

## Scope and boundaries

- In scope: the dark-variant transform and the gate that checks it; the prose, headings and
  section order of the profile page and the tour page; the theme handling of the tour page's
  images and chart; retiring the star chart from both pages.
- Out of scope: the voice notes, their transcripts, and their delivery path, which SP-0003
  settled; the reference account, which is read-only; the illustrations themselves, whose
  sources are unchanged and whose three unused ones stay committed as design-system records.
- Dependencies/uncertainty: the transform now imports scipy for the connected-component pass
  that finds the paper, so the gate installs it; a machine without scipy cannot re-derive.

## Acceptance criteria

- [x] every dark illustration keeps the character's own colours, has a visible edge against a #0f0f0f page, and shows readable text, confirmed on the rendered page rather than on the file alone
- [x] scripts/derive_dark_assets.py --check re-derives all eight variants and exits 0, and exits 1 naming the file when one variant is corrupted
- [x] the required gates job installs what the new transform imports, so the dark check runs rather than erroring on a missing module
- [x] no heading on either the profile page or the tour page is a disclaimer, and neither page carries a State-and-Evidence table
- [x] the tracking block still regenerates byte-identically, so a second run over unchanged data rewrites no bytes
- [x] the tour page loads the light assets under prefers-color-scheme light and the dark assets otherwise, with zero broken images and zero horizontal overflow
- [x] the content adapter validates after the retired chart assets are removed from the manifest and the filename legend

## Evidence and sources

- The old transform, measured: `AI Engineer` light field `(254,247,234)` mapped to dark field
  `(10,10,8)`, which is within 3 levels of GitHub's `#0d1117` and the tour page's `#0f0f0f`.
  `DARK_FIELD` and `DARK_INK` were defined at lines 62 and 63 and referenced nowhere.
- The paper mask covers 54.3 percent of `AI Engineer` and 48.5 percent of `The Badge Wall`,
  measured by counting the border-connected region.
- An ink halo of 8 px was chosen by rendering the same title at 0, 8, 14 and 22 px. At 0 the
  title is dark on dark; at 14 and 22 the outline is thick enough to blur the strokes.
- `python scripts/derive_dark_assets.py --check` reports `VALID: 8 dark variant(s) match their
  source`.
- Rendered on the live page in dark mode: the illustration has a visible edge, the figure
  keeps peach skin, black hair and an orange apron, and the internal text reads
  "AI Engineer", "Reusable components, automated pipelines."
- Rendered in both themes: light loads `AI%20Engineer.gif` and `activity.svg`, dark loads
  `AI%20Engineer-dark.gif` and `activity-dark.svg`, 0 broken, 0 horizontal overflow.
- A second tracker run over unchanged data leaves `profile/README.md` byte-identical.

## Related records

- Required leaf owning issue, parent ancestry and dependencies: https://github.com/Pukujan/stylish-profile/issues/11
- Primary writer / branch / source issue revision / as-of status: omp@windows-workstation, branch task/SP-0004-dark-illustrations-and-page-voice
- Related PR/CI evidence and push receipt (request ID / SHA):

## Checkpoint log

No checkpoints yet.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
