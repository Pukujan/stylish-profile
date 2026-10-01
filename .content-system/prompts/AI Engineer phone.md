# Prompt record: AI Engineer phone

Generated with the built-in image generation tool (`built-in image_gen`,
provider `openrouter`, model `qwen/qwen-image-3`). The published file is
`assets/profile/AI Engineer phone.png`, 1024x1536, role `hero phone`.

## Why this file exists

The wide hero is 1536x1024 with a three-to-two aspect ratio. Scaled into a
390-pixel phone column it becomes about 260 pixels tall, which renders the
subtitle at roughly four pixels: legible in a specification, useless to a
reader. This variant carries the same title and the same subtitle at a size
that survives a phone, so the page serves it through a
`<picture><source media="(max-width: 640px)">` element instead of shrinking the
wide file.

## Prompt

Input image: `assets/profile/AI Engineer.png` (composition, characters,
palette and drawing style are inherited from it).

Subject: a tall portrait version of the same flat hand-drawn illustration,
recomposed for a narrow phone screen: the words "AI Engineer" set very large
and stacked on two lines in the upper third, and beneath them the two-line
subtitle "Reusable components," and "automated pipelines.", with the same cast
of small hand-drawn characters and machines gathered in the lower half around a
tidy vertical arrangement of repeated identical modular blocks.

Changes: recompose into a tall portrait frame; set the title much larger
relative to the frame; set the subtitle on two lines; arrange the repeated
modular blocks vertically instead of horizontally; keep every character,
machine and colour identical to the input.

Scene: flat cream (#FFF9F0) background, the same warm yellow (#FFD93D) accent
shapes and royal blue (#4169E1) details as the wide hero.

Composition: tall portrait frame, title in the upper third, subtitle below it,
the illustrated scene filling the lower half, generous cream margins left and
right.

Lighting: completely flat and even; no shading, no gradients, no drop shadows.

Style: identical to the wide hero — flat hand-drawn vector illustration, thick
black ink outlines, cream background, royal blue, warm yellow, pink and black
only, warm editorial explainer drawing.

Text: exactly three text strings and nothing else — the title "AI Engineer" and
the subtitle "Reusable components," and "automated pipelines.". Sharp,
correctly spelled, dark ink letters with a heavy outline so they stay legible at
small sizes. No other text, no captions, no labels, no numbers, no signatures,
no watermarks, no logos, no wordmarks, no corner marks.

Aspect ratio 2:3, image size 1024x1536.

## Result

Accepted on the first attempt. A vision check read exactly three strings — "AI
Engineer" and "Reusable components, automated pipelines." — found no logo,
wordmark or stray word, confirmed the cream background and flat outlined style,
and reported the title as occupying roughly the top third of the frame.

The full prompt recipe used for review lives on the asset entry in
`.content-system/asset-manifest.json`.
