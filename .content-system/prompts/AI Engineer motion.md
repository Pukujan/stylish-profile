# Prompt record: AI Engineer (motion)

- Asset: `assets/profile/anim/AI Engineer.gif` (900x600, 4 frames, role `motion`)
- Phone asset: `assets/profile/anim/AI Engineer phone.gif` (480x720, 4 frames)
- Dark assets: `AI Engineer-dark.gif`, `AI Engineer phone-dark.gif` — derived, not generated
- Provider: built-in image_gen (openrouter, `qwen/qwen-image-3`)
- Recorded: 2026-10-01

## Why this file exists

The page's opening claim is that a reusable block is raised into a structure and the
same block then goes everywhere. A still frame shows the pose but not the motion, and the
motion is the claim. The hero is the one picture a reader sees before deciding whether to
read anything else, so it carries the most information per pixel on the page.

## Format

GIF, because a probe of GitHub's markdown renderer on 2026-10-01 showed a `.gif` image
receiving the `data-animated-image` attribute while `.apng` displayed as a single frozen
frame. Three generated frames are replayed in ping-pong order, so the loop returns
without a visible snap:

```
frame 1  seated  ->  frame 2  raised  ->  frame 3  lowered  ->  frame 2  raised  ->  repeat
```

Durations 1100, 800, 900, 800 ms.

## Frames

Frame one is the committed still `assets/profile/AI Engineer.png`. Frames two and three
were produced by passing the previous frame back in as an input image with exactly one
entry in `changes[]`.

1. **Seated.** The block rests at the top of the modular structure on the bench.
2. **Raised.** Change prompt: *"The engineer raises the block they are holding to head
   height, lifting it clear of the structure. The camera is completely locked: every
   other object, the three round companions, the conveyor belt, the finished copy of the
   structure, the bench and the background stay in exactly the same pixel position."*
3. **Lowered.** Change prompt: *"The engineer lowers the block from head height down to
   the bench, bringing it to rest against the front of the structure. The camera is
   completely locked: every other object stays in exactly the same pixel position."*

Prompt skeleton for every frame: flat hand-drawn vector illustration, thick uniform black
ink outlines, warm cream background, royal blue and warm yellow only, deliberately naive
sketchy linework, completely flat lighting with no gradients or shadows, and no text,
letters, numbers, captions, labels, signatures, watermarks, logos or wordmarks anywhere.

## Result

A vision pass over a magnified crop of the hand and the block confirmed the block moves
between all three frames, and that the step from raised to lowered is larger than the
step from seated to raised — which is why the ping-pong order reads as one deliberate
raise-and-place rather than as a jitter.

A separate vision pass over the full frames confirmed the three companions and the
conveyor are present and unchanged in frame two, that the block is at shoulder height
there, and that no frame contains a logo or a wordmark.

## Dark variant

`AI Engineer-dark.gif` is not generated. It is a palette transform of the light GIF by
`scripts/derive_dark_assets.py`, so it is byte-stable and re-runs with the tracker rather
than costing a model call per frame.
