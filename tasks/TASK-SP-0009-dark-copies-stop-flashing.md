# TASK-SP-0009 — Dark Copies Stop Flashing

<!-- continuity:task {"acceptance": ["all eight committed dark GIFs measure 0 source-unchanged flashing pixels, by re-running the probe over assets/profile/anim/*.gif excluding the -dark files", "the page area of the new construction is within 1% of the per-frame mean on both hero animations", "a vision pass over One Push Many Pipelines, The Badge Wall, What You Can Check and Pujan and the Loose Ends finds no dark hole punched into a drawn object", "python scripts/derive_dark_assets.py --check passes on every committed variant and every changed hash is updated in .content-system/asset-manifest.json", "the 48,617 px of page cream the dark hero keeps are unchanged by the new construction", "every existing gate stays green: check_profile_links, generate_voice_notes --check, the pinned CGM adapter validator, the hsw writing scans, build_locked_motion check on every recipe, and continuity validate"], "depends_on": ["SP-0008"], "goal": "Stop the derived dark GIFs flashing where a moving sprite crosses page-coloured territory, by deciding the page mask once for the whole loop instead of once per frame", "id": "SP-0009", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/28", "next_action": "regenerate the eight dark GIFs, update the manifest hashes, run the full local gate set, then push the branch, open the pull request and merge it", "owner": "omp@windows-workstation", "priority": "P1", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "active", "why": "The dark copies of the profile animations flash. Where the same pixel keeps the same colour in two consecutive frames of the light drawing, its dark output can still differ, so a region blinks between the dark page colour and a cream mark colour as the animation plays. The page mask that decides 'this is the page' is decided per frame by asking which light region touches the frame edge, and that answer moves when a drawn outline's anti-aliasing changes. 21,094 pixels flash on One Push Many Pipelines alone, and the box interiors the animation fills blink cream and dark every frame"} -->

- Status: active
- Owner: omp@windows-workstation
- Priority: P1
- Depends on: SP-0008

## Goal

Stop the derived dark GIFs flashing where a moving sprite crosses page-coloured
territory, by deciding the page mask once for the whole loop instead of once per
frame.

## Why

The dark copies of the profile animations flash. Where the same pixel keeps the
same colour in two consecutive frames of the light drawing, its dark output can
still differ, so a region blinks between the dark page colour and a cream mark
colour as the animation plays. It is visible: the interiors of the boxes in
`One Push Many Pipelines` flash cream and dark every frame.

The cause is that `_paper_mask` in `scripts/derive_dark_assets.py` is decided
per frame: it asks which light region reaches the frame edge, and a one-pixel
anti-aliased change in a drawn outline moves that answer. On `One Push Many
Pipelines` the page mask covers 505,408 pixels in frame 1 and 491,573 in frame
2, and the two differ over 34,949 pixels that are byte-identical in the light
source. Total across the eight committed dark GIFs: 24,148 flashing pixels.

## Allowed files

- scripts/derive_dark_assets.py
- assets/profile/anim/*-dark.gif
- .content-system/asset-manifest.json
- tasks/**
- checkpoints/**
- PROJECT.md
- docs/CONTINUITY_INDEX.md

## Human outcome

The dark illustrations hold still. A reader scrolling the page in dark mode sees
the drawing move and nothing else; no region blinks between the dark page and a
cream patch as a sprite crosses it.

## Scope and boundaries

- In scope: the page mask in `scripts/derive_dark_assets.py`, the eight derived
  dark GIFs, and the manifest hashes and derivation text that describe them.
- Out of scope: the halo (fixed under SP-0008), the light GIFs, the drawings
  themselves, the page copy and order, and the voice notes.

## Acceptance criteria

- [x] all eight committed dark GIFs measure 0 source-unchanged flashing pixels, by re-running the probe over `assets/profile/anim/*.gif` excluding the `-dark` files
- [x] the page area of the new construction is within 1% of the per-frame mean on both hero animations
- [x] a vision pass over `One Push Many Pipelines`, `The Badge Wall`, `What You Can Check` and `Pujan and the Loose Ends` finds no dark hole punched into a drawn object
- [x] `python scripts/derive_dark_assets.py --check` passes on every committed variant and every changed hash is updated in `.content-system/asset-manifest.json`
- [x] the 48,617 px of page cream the dark hero keeps are unchanged by the new construction
- [x] every existing gate stays green: `check_profile_links`, `generate_voice_notes --check`, the pinned CGM adapter validator, the hsw writing scans, `build_locked_motion.py check` on every recipe, and `continuity validate`

## Evidence and sources

Recorded on branch `task/SP-0009-dark-copies-stop-flashing`.

| Command | Result |
| --- | --- |
| `python scripts/derive_dark_assets.py --check` | `VALID: 8 dark variant(s) match their source` |
| `python scripts/check_profile_links.py` | `VALID: 35 local reference(s) resolved, 36 recorded hash(es) matched` |
| `python scripts/generate_voice_notes.py --check` | `checked 9 clip(s), 0 problem(s)` |
| `python scripts/build_locked_motion.py check --recipe scripts/motion-recipes/{figure,hero-phone,hero-wide}.json` | `OK` on all three |
| pinned CGM `validate_content_system.py --adapter .content-system` | `VALID: content-generation-modules contract and target adapter` |
| pinned CGM `verify_hsw_applied.py --root <cgm>` | `VALID: HSW always-on contract OK` |
| pinned CGM `verify_hsw_applied.py --mode acs-html --html docs/index.html` | `VALID: HSW always-on contract OK and HTML tell scan clean` |

### The construction

A pixel counts as page if the border-connected pass calls it page in this frame,
or if it holds nearly the same colour as a frame in which that pass did:

```
page_i = ( papers[i] | ( union_j papers[j] & |rgb_i - rgb_j| <= 2 ) ) & candidate_i
```

The second clause is loop-constant except for the colour test, so a pixel that
does not change between two frames gets the same answer in both, which is why
the flash is 0 by construction rather than by tuning. `PAPER_MATCH_TOLERANCE`
is 2. The first clause is `papers[i]`, which is a subset of `union_j papers[j]`,
so **every pixel the construction darkens was called page by the border pass in
some frame** — measured, 0 pixels violate this on any frame of any asset.

### Why the tolerance is 2

The box interiors in `One Push Many Pipelines` are the page colour exactly,
`(253, 247, 238)` in frame 0, and they drift two levels at frame 2. Two levels
of drift is enough to make the pass answer differently in the two frames, and
that is the 21,094 pixel flash. Measured coverage of the three box interiors:

| Tolerance | box 1 (f0/f1/f2/f3) | box 2 | box 3 |
| --- | --- | --- | --- |
| 0 | 0.00 / 0.00 / 1.00 / 0.90 | 1.00 / 1.00 / 0.62 / 0.67 | 1.00 / 1.00 / 0.78 / 0.83 |
| 2 | 1.00 / 1.00 / 1.00 / 0.94 | 1.00 / 1.00 / 1.00 / 0.79 | 1.00 / 1.00 / 1.00 / 0.83 |
| 6 | 1.00 / 1.00 / 1.00 / 0.95 | 1.00 / 1.00 / 1.00 / 0.81 | 1.00 / 1.00 / 1.00 / 0.83 |

T=0 leaves box 1 cream in frames 0 and 1 — the cream trail criterion 2 forbids —
so it does not fix the headline symptom. T=2 is the smallest value that darkens
all three interiors. Two is also far from every drawn object: the nearest light
thing that is not page is the grey the small robot in `AI Engineer` is drawn in,
15 levels away, and Pujan's drawer white is 12.

Safety does not rest on a per-run size bound. Two claims carry it, both
measured on the committed bytes:

- **Containment.** Every pixel the construction darkens was called page by the
  border-connected pass in some frame. `page_i ⊆ ⋃_j papers[j]`, 0 violations on
  every frame of all eight assets; and `papers[i] ∩ candidate_i ⊆ page_i`, 0
  missing pixels, so the construction is a strict superset of the shipped page
  mask.
- **No drawn dark ink is ever covered.** Of the pixels the fix newly darkens
  (compared with the shipped GIF), **0** were dark ink in the light drawing
  (max channel ≥ 140). A drawn line, rule or letter is never a candidate.

| Asset | newly darkened vs shipped | of those, dark ink in light |
| --- | --- | --- |
| One Push Many Pipelines | 41,041 | 0 |
| The Badge Wall | 2,981 | 0 |
| What You Can Check | 1,411 | 0 |
| Pujan and the Loose Ends | 1,163 | 0 |
| AI Engineer | 6 | 0 |
| AI Engineer phone | 43 | 0 |
| Projects on One Thread | 0 | 0 |
| Reusable Blocks | 0 | 0 |

An earlier draft of this note claimed that every pixel the tolerance adds more
than eight levels from the frame's own field belongs to a run of at most
nineteen pixels. That claim is false as written: measured on that set, the
largest component is 190 px on `What You Can Check` (its tilted card, light
colour `(253, 246, 227)`, distance 10 from the field), which alone refutes a
nineteen-pixel bound. Measured bounds on the tolerance-added set, per asset:

| Asset | tolerance-added, >8 levels from field | largest component |
| --- | --- | --- |
| One Push Many Pipelines | 27 | 7 |
| The Badge Wall | 138 | 19 |
| What You Can Check | 876 | 190 |
| Pujan and the Loose Ends | 472 | 15 |
| AI Engineer | 6 | 1 |
| AI Engineer phone | 16 | 16 |

Those large entries are the page-coloured card faces, which is why the bound
was never the safety argument: `What You Can Check`'s card is the page colour,
ten levels from the field only because the field drifts, and it was already
darkened by the shipped GIF in three of its four frames. The three probes above
replace the bound.

### Criterion 1 — flash, measured on the committed bytes

Source-unchanged pixels (byte-identical in consecutive light frames) whose dark
output differs:

| Asset | before | after |
| --- | --- | --- |
| One Push Many Pipelines | 21,094 | **0** |
| The Badge Wall | 1,775 | **0** |
| What You Can Check | 923 | **0** |
| Pujan and the Loose Ends | 271 | **0** |
| AI Engineer | 5 | **0** |
| AI Engineer phone | 80 | **0** |
| Projects on One Thread | 0 | **0** |
| Reusable Blocks | 0 | **0** |
| **Total** | **24,148** | **0** |

### Criterion 2 — page area

Mean of the per-frame page area against the mean of the per-frame light
`_paper_mask`:

| Asset | mean page | mean light | change |
| --- | --- | --- | --- |
| AI Engineer | 399,708.2 | 399,707.2 | +0.00% |
| AI Engineer phone | 196,459.7 | 196,452.5 | +0.00% |
| One Push Many Pipelines | 498,785.6 | 490,430.0 | +1.70% |
| Reusable Blocks | 390,897.2 | 390,897.2 | +0.00% |

Both hero animations are at +0.00%, inside the 1% bound. One Push is above 1%
but it is not a hero animation, and its added territory is its own box interiors
coming back.

### Criterion 3 — no hole in a drawn object

Because every darkened pixel was called page by some frame's border pass, a hole
can only appear where that pass is wrong in some frame. The construction is a
strict superset of the shipped page mask — `papers[i] ∩ candidate_i ⊆ page_i`
with 0 missing pixels, and `page_i ⊆ ⋃_j papers[j]` with 0 violations on every
frame of all eight assets — so it can only add darkness, never remove it.

Three probes, run on the committed bytes against the shipped GIFs, settle it.
The third exists because `marks` is now taken from frame 0 rather than derived
per frame, so the light-ink channel changed too and a `PANEL`-only probe cannot
see it.

**Probe 1 — newly darkened pixels.** Of the pixels the fix turns `PANEL` that
were not `PANEL` in the shipped GIF, **0** were dark ink in the light drawing
(max channel ≥ 140). A drawn line, rule or letter is never a candidate.

| Asset | newly `PANEL` | of those, dark ink in light |
| --- | --- | --- |
| One Push Many Pipelines | 41,041 | 0 |
| The Badge Wall | 2,981 | 0 |
| What You Can Check | 1,411 | 0 |
| Pujan and the Loose Ends | 1,163 | 0 |
| AI Engineer | 6 | 0 |
| AI Engineer phone | 43 | 0 |
| Projects on One Thread | 0 | 0 |
| Reusable Blocks | 0 | 0 |

**Probe 2 — the added set's shipped history.** The pixels the fix adds were
already `PANEL` in the shipped GIF's *other* frames: on `What You Can Check` the
added set is `PANEL` in 0.85 of shipped frame 0, 0.15 of frame 1, 0.67 of frame
2 and 0.15 of frame 3 — an alternating pattern. That is the flicker being
stabilised, not a hole being introduced.

**Probe 3 — lost light ink (the `marks` channel).** Pixels that were `PAPER_INK`
in the shipped GIF and are not in the new one: 228 on `What You Can Check` and
50 on `Pujan and the Loose Ends`, 0 on the other six. Every one of them is page
coloured in the light source — distance 0 from the frame's field on `What You
Can Check`, 2 on `Pujan` — and every one became `PANEL`. They are page specks
the shipped per-frame `marks` pass misclassified as diagram ink and painted
light; on a dark page that is a cream dot. The new frame-0 `marks` pass does not
classify them as ink, so they fall through to `PANEL`, which is what a
page-coloured pixel should be. No text lost ink: the largest component is 12 px
on `What You Can Check` and 13 px on `Pujan`, scattered, not a glyph run. The
converse direction is clean too: **0** pixels gained `PAPER_INK` on any of the
eight assets, so the light-ink channel only ever lost page specks.

A vision pass over the four named assets at the chosen tolerance finds no flat
dark rectangle punched into a drawn object. Vision reports were checked against
pixels and did not hold, in both directions: the "blue triangle" in One Push is
real artwork (frame 4's box interior is `(30, 82, 212)`), the small robot does
not float, and a claim that `What You Can Check`'s tagline darkened was refuted
by probe 3 (all affected pixels page coloured) and by a second pass that found
the new bytes cleaner than the shipped ones. Verdicts come from pixels, not from
the vision model.

### Criterion 5 — the survivor set

The 48,617 px of page cream the dark hero keeps (the bench face and the
pegboard, both `(253, 244, 232)`, distance 0 from the field) is preserved
exactly: `survLost = 0` for the union construction and for every tolerance
measured, 0 through 12. The tolerance clause never touches the survivor set,
because those pixels are never border-connected and so never enter `papers[j]`.

### Rejected constructions, with numbers

- **A loop-constant closed ink barrier** — the issue's own named next action.
  `reach = border_reach(~(OR of every frame's ink))`, then `page_i = reach &
  candidate_i`. Flash 0 by theorem, but page area collapses: One Push −10.45%,
  Reusable Blocks −20.9%. It also destroys 11,805 px of the hero survivor set on
  `AI Engineer` and 16,325 px on the phone. Every morphological variant
  (`ink_or_close1`, `ink_or_erode1/2`, `ink_and`, `ink_frame0`, `noncand_or`,
  `noncand_and`, majority/any2/largest) either keeps the collapse or destroys
  38,000-101,000 px of the survivor set. Rejected on measurement.
- **A loop-constant page colour compared per frame** (`|rgb_i - field_loop| <=
  K`). Does not reach flash 0: 21,627 pixels of `One Push Many Pipelines` are
  byte-identical between consecutive frames and still get different `papers[i]`,
  so a frame-local term on a loop-constant field cannot make the answer
  loop-constant. Rejected on measurement.
- **Plain union with no colour gate.** Punches a dark rectangle through the
  `AI Engineer` robot — vision-confirmed, and every other panel intact at T=0, 6
  and 8.
- **Intersection, histogram T=0, field-guard families.** Intersection costs
  5.35-20.94% of page area. Histogram T=0 loses 4 px of the survivor set and 43
  px on the phone, and never fully covers One Push's box interiors. The
  field-guard family never reaches 0 flash, because the guard is asymmetric
  across frames: 1,534 / 1,036 / 982 / 455 / 603 at T=4/6/8/10/12.

## Related records

- Owning issue: https://github.com/Pukujan/stylish-profile/issues/28. Leaf; parent ancestry: none. Dependencies: SP-0008, whose measurements and probe this task's numbers come from.
- Primary writer: omp@windows-workstation, branch `task/SP-0009-dark-copies-stop-flashing`.
- Supersedes the derivation text SP-0008 wrote into `.content-system/asset-manifest.json` for the eight motion dark variants, because the transform it describes has changed.

## Checkpoint log

### 2026-10-02 04:05:40 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":["scripts/derive_dark_assets.py, 6 assets/profile/anim/*-dark.gif, .content-system/asset-manifest.json, tasks/TASK-SP-0009-dark-copies-stop-flashing.md, checkpoints/CURRENT.md, .continuity/documents.json, docs/CONTINUITY_INDEX.md"],"completed":["The dark GIFs no longer flash: the page mask is decided once for the whole loop instead of once per frame, and flash is 0 on all eight committed variants (was 24,148)."],"decisions":["Keep PAPER_MATCH_TOLERANCE at 2: smallest value that darkens all three One Push box interiors, and far from every drawn object. The loop-union superset is a strict superset of the shipped page mask, so it can only add darkness."],"evidence":["derive_dark_assets.py --check VALID on 8 variants; build_locked_motion.py check OK on every recipe; check_profile_links VALID 35 refs/36 hashes; generate_voice_notes --check 0 problems; pinned CGM adapter VALID; both hsw scans VALID; continuity validate VALID."],"next_action":"Open the pull request against main, verify the required gates check on the exact merge candidate, merge with gh pr merge --squash, then post the leaf receipt to issue #28 keyed by request ID and pushed SHA.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0009","timestamp":"2026-10-02T04:05:40Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"3d5a45c6292ebd229d5b77d5cd04385aba61815f2c975de77b000890ee070830","request_id":"379e3a170a404f8f97c9d9631b0c32cb","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0009"} -->

Completed:
- The dark GIFs no longer flash: the page mask is decided once for the whole loop instead of once per frame, and flash is 0 on all eight committed variants (was 24,148).

Evidence:
- derive_dark_assets.py --check VALID on 8 variants; build_locked_motion.py check OK on every recipe; check_profile_links VALID 35 refs/36 hashes; generate_voice_notes --check 0 problems; pinned CGM adapter VALID; both hsw scans VALID; continuity validate VALID.

Decisions:
- Keep PAPER_MATCH_TOLERANCE at 2: smallest value that darkens all three One Push box interiors, and far from every drawn object. The loop-union superset is a strict superset of the shipped page mask, so it can only add darkness.

Changed:
- scripts/derive_dark_assets.py, 6 assets/profile/anim/*-dark.gif, .content-system/asset-manifest.json, tasks/TASK-SP-0009-dark-copies-stop-flashing.md, checkpoints/CURRENT.md, .continuity/documents.json, docs/CONTINUITY_INDEX.md

Blocked/uncertain:
- none

Next:
- Open the pull request against main, verify the required gates check on the exact merge candidate, merge with gh pr merge --squash, then post the leaf receipt to issue #28 keyed by request ID and pushed SHA.
