# Prompt record — What You Can Check

- Asset: `assets/profile/What You Can Check.png`
- Role: evidence (portrait)
- Requested dimensions: 1024x1536
- Provider: built-in image_gen (openrouter, `qwen/qwen-image-3`)
- Recorded: 2026-10-01

## Requested text

- Title: `What You Can Check`
- Subtitle: `Sources, not slogans`

## Attempt 1 (rejected)

The first prompt described the source cards as carrying "a short horizontal ink line
suggesting a source link". The renderer filled that suggestion with invented list copy —
`Academic Journals`, `Official Studies`, `Expert Interviews` and more — and dropped the
requested subtitle entirely. That violates the declared text policy (one title plus one
subtitle) and the rejection condition on crowded or substituted copy, so the asset was
regenerated.

## Attempt 2 (accepted)

```text
Subject: A flat hand-drawn editorial illustration in a tall portrait frame. A vertical
stack of three small blank paper cards floats down the centre; each card carries only a
simple icon and one short horizontal ink line, and a tiny round seal in the corner. Fine
dashed lines run from the bottom card down into a small open book and a pair of
headphones resting at the foot of the frame. The small round companion character with one
dot eye sits on the top card holding a short pencil. Hand-drawn squiggles, one halo ring,
and a soft warm yellow glow behind the stack. The ONLY words anywhere in the image are
the title 'What You Can Check' and the subtitle 'Sources, not slogans'. Every card, book
and background surface is otherwise completely wordless: no labels, no captions, no list
items, no headings, no lettering of any kind on the cards.
Action: A vertical stack of blank source cards feeds down into an open book and a pair of
headphones.
Scene: A tall cream-coloured panel with a narrow column of floating blank cards.
Composition: Portrait 2:3 composition; the card stack stays inside the middle vertical
band so it survives a narrow crop; the title sits in calm cream space at the top, the
subtitle sits below the stack at the bottom; both text lines are large, isolated and
surrounded by empty cream.
Lighting: Flat even editorial lighting, one soft warm halo behind the stack.
Style: Hand-drawn flat vector editorial illustration, thick ink outlines, generous cream
negative space, limited warm palette, icon-only cards.
Text: What You Can Check / Sources, not slogans
```

## Review

Accepted. Re-render carries only `What You Can Check` and `Sources, not slogans`; the
card interiors are icon lines with no readable characters. Style and palette match the
declared contract.
