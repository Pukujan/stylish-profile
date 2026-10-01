# Prompt record — AI Engineer

- **Asset:** `assets/profile/AI Engineer.png`
- **Role:** hero (wide, 1536x1024)
- **Provider:** built-in image_gen
- **Recorded:** 2026-10-01
- **Exact title:** `AI Engineer`
- **Exact subtitle:** `Reusable components, automated pipelines`

## Why this asset exists

The page previously opened with a picture about dropped work. That explained the
problem the featured repositories solve, but it never said what the person behind them
does. This asset answers the reader's first question directly: an engineer who automates
repetitive engineering work by building one component well and reusing it.

The repeated identical block is the whole idea. It appears on the conveyor, in the
structure being assembled, and again in the finished smaller copy, so the same component
is visibly reused at two scales.

## Prompt (attempt 2, accepted)

```
subject: A flat hand-drawn vector illustration of a young engineer at a wide workbench
assembling identical reusable modular blocks into a machine, with three small round
robot companions each carrying one block.

action: The engineer slots a single reusable block into a growing modular structure; a
conveyor line of identical blocks feeds the bench; a second, smaller copy of the same
structure stands finished beside it, showing the same component reused at two sizes.

scene: A warm cream workshop with a faint blueprint grid on the back wall, a pegboard of
simple unlabelled tools, and a short conveyor belt running along the bench.

composition: Engineer and the modular structure occupy the right two-thirds; quiet empty
cream space on the left holds only the title and subtitle; the whole subject stays inside
a centre crop that survives a narrow column.

lighting: flat even lighting, no shadows, no gradients

style: flat hand-drawn vector, thick ink outlines, rounded line caps, limited palette of
royal blue #4169E1, warm yellow #FFD93D, orange #FF8C42, pink #FF6B9D and ink #1A1A1A on
cream #FFF9F0, generous negative space, editorial poster feel, no photorealism, no 3D
render, no gloss

text: Title: AI Engineer. Subtitle: Reusable components, automated pipelines. No other
text anywhere: no logo, no wordmark, no brand mark, no labels, no captions, no signage,
no text on tools, boxes, screens or blocks.

aspect_ratio: 3:2
image_size: 1536x1024
```

## Rejected attempt 1

Same prompt without the `No other text anywhere` clause and without the pegboard being
described as unlabelled.

**Rejection reason:** the render added a two-word logo block in the top-left corner. That
is copy the asset never declared, and it violates the visual contract's rule that a
narrative asset carries only its declared title and subtitle.

**Fix:** the text clause was tightened to name every place a stray wordmark could appear,
and the tools were described as unlabelled.

## Review decision

Accepted 2026-10-01. A vision pass over the accepted file confirms exactly three text
strings — `AI Engineer`, `Reusable components,`, `automated pipelines.` — and no logo or
wordmark. The render is flat hand-drawn vector with thick ink outlines on a cream field,
the repeated block is legible at both sizes, and the left third is reserved space.

## Verification

- Dimensions 1536x1024, mode RGB, no alpha channel.
- SHA-256 of the committed file:
  `5e4a97fb4aa5961ed2c6107d87ce37dee9227cf341fe86daf35b7cf6ce1c44b1`
