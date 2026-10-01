# Prompt record: Pujan (profile avatar)

Generated with the built-in image generation tool (`built-in image_gen`,
provider `openrouter`, model `qwen/qwen-image-3`). The published file is
`assets/profile/Pujan.png`, 460x460, role `avatar`.

## Why this file exists

The account avatar was a generated identicon: magenta blocks on a pale grey
field. It is not a placeholder GitHub assigns, it is simply what was uploaded
years ago, and it has two problems on a page built around a cream-and-royal-blue
illustration set. It is off-palette, and its light field is the one surface on
the page that cannot follow the theme, because GitHub shows the same avatar in
both.

The page it sits on is the first thing a visitor sees. An avatar drawn as the same
character as `Pujan and the Loose Ends.png` makes the page read as one designed
thing rather than a profile with a picture bolted on.

## Format

PNG at 460x460. GitHub renders an avatar at up to 460 pixels, so anything larger
is bytes nobody sees; the source render is 1024x1024 and is downsampled once with
Lanczos. 460x460 also leaves enough resolution for the retina case.

The source render is kept out of the repository. Only the 460x460 file is
committed, because the larger one is not used by anything.

## How it was made

Frame one of `Pujan and the Loose Ends.png` was passed in as an input image with
a single change: reframe the same character as a centred square head and
shoulders. Chaining from the illustration rather than describing the character
from scratch is what keeps the round glasses with the pink bridge, the cowlick,
the smile and the black sweater with its yellow button identical between the
avatar and its source.

## Palette decision

The field is deep royal blue rather than cream or near-black. A cream field
would be a bright disc on the dark page, and a near-black field would disappear
into it. Royal blue is already the page's primary accent, and it holds its shape
against both a white and a near-black surround, which matters because the avatar
cannot switch with the theme.

## Review

Accepted 2026-10-01, on the second candidate.

The first candidate was rejected. A side-by-side against `Pujan and the Loose
Ends.png` showed muted, thin, sketch-like lines where the illustration set uses
bold even outlines, so it read as an unrelated picture pasted onto the page
rather than the same hand. The second candidate was regenerated with an explicit
line-weight clause ("bold thick confident outlines of even weight, the same
heavy line weight used in Image 1, not thin delicate or sketchy lines") and an
explicit palette clause, and it matches.

Vision checks on the accepted file confirmed a flat vector head-and-shoulders
portrait, a bright royal blue field, bold thick outlines, the whole head and both
shoulders inside the frame with margin on all four sides, and no text, letter,
number, wordmark or logo anywhere. A circular-crop preview confirmed the face,
glasses, hair and shoulders all survive GitHub's round mask, and a side-by-side
confirmed the avatar and `Pujan and the Loose Ends.png` read as the same
character.

Note on the page's other drawing: the hero is a different figure. `AI Engineer`
is the same person in work gear, pink goggles and orange overalls at a bench, so
the tour header stacks that scene above a portrait of the author out of
glasses. The two were drawn from separate prompts and are not the same design.
Left as-is because re-drawing the hero means regenerating its still, its phone
framing, both motion sets and all four dark variants; it is an art-direction
call for the owner rather than a defect with one obvious fix.

## Reuse

If the character is ever redrawn, regenerate this from the new illustration with
the same single change, re-crop to 460x460, and update the hash in
`.content-system/asset-manifest.json`. Uploading the file to GitHub is a web-UI
action: the REST API can read an avatar but cannot set one.
