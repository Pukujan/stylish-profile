# Prompt record — Projects on One Thread

- **Asset:** `assets/profile/Projects on One Thread.png`
- **Role:** system (square, 1024x1024)
- **Provider:** built-in image_gen (openrouter, `qwen/qwen-image-3`)
- **Recorded:** 2026-10-01
- **Exact title:** `Projects on one thread`
- **Exact subtitle:** `leave a trail behind you`

## Why this asset exists

Issue #24 rejected the previous figure — `Three Projects One Thread` — for
malformed glyphs in the subtitle and labels, a broken and doubled connecting
line, a clipboard floating free of the robot, a missing arm, and an outline that
thickened mid-stroke. It was also titled `Three Projects` while the page lists
four. The rebuild drops the count from the title entirely and composites the
icons from separate keyed sprites so nothing can float or break.

## Environment plate

The plate is drawn empty — no icons — so the four card interiors are clean
space for the sprites, and the thread runs through the lower quarter of the
cards rather than across their middle.

```
subject: A flat hand-drawn editorial diagram on a completely flat solid cream
#FFF9F0 background, square composition: at the top, two lines of hand-lettered
text in thick black ink with sharp legible correctly spelled letters — the first
line reads 'Projects on one thread' and the second smaller line reads 'leave a
trail behind you'; below the text a row of four identical empty rounded
rectangle cards drawn with thick uniform black ink outlines, each card
completely empty inside with no text and no icons; one single thick royal blue
#4169E1 hand-drawn stitched line runs horizontally through the lower quarter of
all four cards near their bottom edge, like a seam, and continues past the cards
to both side edges of the image; nothing else, no characters, no objects, no
gradients, no texture noise, no shadows

style: flat hand-drawn editorial diagram, thick confident uniform ink outlines,
clean flat vector shapes, palette limited to cream, black ink, royal blue, warm
yellow and orange

aspect_ratio: 1:1
image_size: 1024x1024
```

Attempts 1 and 2 (`figure-plate-01.png`, `figure-plate-02.png`) were rejected:
attempt 1 ran the thread through the vertical middle of the cards, leaving no
clear space for an icon; attempt 2 had the right layout but no subtitle, and the
manifest's text policy requires one. Attempt 3, above, is the accepted plate.

## Icon sprites

Each icon is one object on flat cream so the builder can key it out and contain
it inside its card. The shared clause: thick confident uniform black ink
outlines, clean flat vector shapes, no gradients, no text, no letters, one
single object centred on a completely flat solid cream `#FFF9F0` background with
generous empty margin, palette limited to cream, black ink, royal blue
`#4169E1`, warm yellow `#FFC93C` and orange `#FF7A29`.

- **Agent** (`icon-agent-01.png`): a cute round robot head with one dot eye and
  a small antenna, holding a tiny checklist clipboard with three check marks.
- **Continuity** (`icon-continuity-01.png`): a bookmark ribbon with a dotted
  trail of small circles curving behind it, like checkpoints along a path.
- **Content** (`icon-content-01.png`): a sheet of paper with a small framed
  picture inside it and two short text lines.
- **Routing** (`icon-routing-01.png`): one thick line from the left forking into
  three routes with small arrows, and one solid royal blue dot on the middle
  route showing the chosen recommendation.
- **Dot** (`dot-01.png`): a single solid royal blue hand-drawn dot with a thick
  black ink outline and a slightly irregular wobbly edge — the marker that
  travels along the thread in the animation.

## Review decision

Accepted 2026-10-01. A vision pass over the plate confirms both lines of
lettering spelled exactly, four closed cards and one continuous thread. The
icons are contained inside their cards by measurement: the builder fits each to
a box narrower than the card, so the wide fork cannot spill past the outline —
the detached-element defect the owner rejected.

## Verification

- Dimensions 1024x1024, mode RGB, no alpha channel.
- SHA-256 of the committed file:
  `5eec9f69bc248e08f59e2771b18c69480f56f1996d51358e589d083a68a15f08`
- Recipe `scripts/motion-recipes/figure.json`.
