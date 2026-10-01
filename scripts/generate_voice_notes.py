"""Regenerate the spoken clips from the recorded text.

The clips are checked in, so this script is not part of the publish path. It
exists so the text in `.content-system/voice-notes.json` is the source of truth
and every clip can be rebuilt from it, which is what keeps the provenance record
honest: the committed file and the words it says cannot drift apart.

The voice is the Ayaka reference the owner ranked highest in the voice lab
record. The API key is read from an env file at runtime and is never printed,
echoed, or written into any provenance record.

Run with the voice-lab interpreter, which has the Fish Audio SDK installed:

    D:/claude/hades-voice-lab/venv/Scripts/python.exe scripts/generate_voice_notes.py

Options:
    --only "<file name>"  rebuild just that clip
    --check               verify the committed clips against the record, no API call
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import quote, unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
VOICE_LAB = Path("D:/claude/hades-voice-lab")
CONFIG = REPO_ROOT / ".content-system" / "voice-notes.json"
MANIFEST = REPO_ROOT / ".content-system" / "asset-manifest.json"
PROFILE_PAGE = REPO_ROOT / "profile" / "README.md"
TOUR_PAGE = REPO_ROOT / "docs" / "index.html"
OUT_DIR = REPO_ROOT / "assets" / "profile" / "voice-notes"
REL_DIR = "assets/profile/voice-notes"

# The tour page prints what each clip says. It is the only place a listener can
# read along, so it has to be the clip's own words rather than a tidied version
# of them; nothing compared the two before.
NOTE_OPEN = '<div class="note"'
AUDIO_SRC = re.compile(r'<audio[^>]*\bsrc="([^"]+)"')
SUMMARY = re.compile(r"<summary>(.*?)</summary>", re.S)
TRANSCRIPT = re.compile(r'<p class="transcript">(.*?)</p>', re.S)
# The label that promises the text below is the clip's own words. The four
# project notes say "What it does" and print a description instead, which is a
# different promise and is deliberately not compared word for word.
VERBATIM_LABEL = "read the transcript"

# Layer III bitrate tables, indexed by the four-bit field in the frame header.
# The page's clips are 128 kbps mono, but a re-run at another rate must still
# measure correctly rather than silently mis-report its own length.
BITRATES = {
    3: (None, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, None),
    2: (None, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, None),
    0: (None, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, None),
}
SAMPLE_RATES = {3: (44100, 48000, 32000), 2: (22050, 24000, 16000), 0: (11025, 12000, 8000)}

# A label is a link's own text ("[listen, 0:27](...)") or a parenthetical after
# one ("(...) (0:16)"). Both forms appear on the profile page.
LABEL = re.compile(r"(\d+):(\d{2})")

def mp3_duration(data: bytes) -> float:
    """Length of an MPEG audio file in seconds, read from its own frames.

    The clips are constant-bitrate and carry no Xing/Info header, so a byte
    count over a nominal bitrate would be a guess. Walking the frame headers is
    exact for constant and variable bitrate alike and needs nothing outside the
    standard library, which matters because this runs in CI.
    """
    offset = 0
    if data[:3] == b"ID3":
        # Skip the tag so its bytes are not counted as audio.
        offset = 10 + (
            (data[6] & 0x7F) << 21 | (data[7] & 0x7F) << 14
            | (data[8] & 0x7F) << 7 | (data[9] & 0x7F)
        )

    total = 0.0
    i = offset
    end = len(data)
    while i + 4 <= end:
        if data[i] != 0xFF or data[i + 1] & 0xE0 != 0xE0:
            i += 1
            continue
        version = (data[i + 1] >> 3) & 0x03
        layer = (data[i + 1] >> 1) & 0x03
        bitrate_index = (data[i + 2] >> 4) & 0x0F
        rate_index = (data[i + 2] >> 2) & 0x03
        if layer != 1 or version == 1 or bitrate_index in (0, 15) or rate_index == 3:
            i += 1
            continue
        bitrate = BITRATES[version][bitrate_index]
        rate = SAMPLE_RATES[version][rate_index]
        padding = (data[i + 2] >> 1) & 0x01
        samples, coefficient = (1152, 144) if version == 3 else (576, 72)
        total += samples / rate
        i += coefficient * bitrate * 1000 // rate + padding
    return total

def page_labels(clip_file: str) -> list[int]:
    """Every length label the profile page attaches to this clip, in seconds."""
    encoded = quote(clip_file)
    found: list[int] = []
    for line in PROFILE_PAGE.read_text(encoding="utf-8").splitlines():
        if f"{REL_DIR}/{encoded}" not in line:
            continue
        for minutes, seconds in LABEL.findall(line):
            found.append(int(minutes) * 60 + int(seconds))
    return found

def page_notes() -> dict[str, dict]:
    """Every note the tour page prints, keyed by clip file.

    One note block holds one audio element, its label and the text under it, so
    splitting on the note open tag keeps each clip's text with its own clip
    rather than borrowing the next one's.
    """
    if not TOUR_PAGE.is_file():
        return {}
    text = TOUR_PAGE.read_text(encoding="utf-8")
    found: dict[str, dict] = {}
    for block in text.split(NOTE_OPEN)[1:]:
        src = AUDIO_SRC.search(block)
        if src is None:
            continue
        label = SUMMARY.search(block)
        para = TRANSCRIPT.search(block)
        found[unquote(src.group(1).rsplit("/", 1)[-1])] = {
            "label": " ".join(unescape(label.group(1)).split()) if label else "",
            "text": " ".join(unescape(para.group(1)).split()) if para else None,
        }
    return found


def check(config: dict, manifest: dict) -> int:
    """Report any clip whose bytes, hash, recorded text, page label or page transcript disagrees."""
    by_path = {a["path"]: a for a in manifest["assets"]}
    problems = 0
    for clip in config["clips"]:
        path = OUT_DIR / clip["file"]
        if not path.is_file():
            print(f"MISSING {clip['file']}")
            problems += 1
            continue
        data = path.read_bytes()
        entry = by_path.get(f"{REL_DIR}/{clip['file']}")
        if clip.get("bytes") != len(data):
            print(f"BYTES   {clip['file']}: recorded {clip.get('bytes')}, file {len(data)}")
            problems += 1
        if entry is None:
            print(f"UNLISTED {clip['file']}: no manifest entry")
            problems += 1
        else:
            if entry.get("hash") != hashlib.sha256(data).hexdigest():
                print(f"HASH    {clip['file']}: manifest hash does not match the file")
                problems += 1
            if entry.get("spoken_text") != clip["text"]:
                print(f"TEXT    {clip['file']}: manifest text differs from the record")
                problems += 1

        # The page prints a length beside each link. It is hand-typed, so a
        # regenerated clip would leave a stale number that nothing else here
        # would notice.
        claimed = page_labels(clip["file"])
        actual = round(mp3_duration(data))
        if not claimed:
            print(f"LABEL   {clip['file']}: no length label on the profile page")
            problems += 1
        elif set(claimed) != {actual}:
            shown = ", ".join(f"{s // 60}:{s % 60:02d}" for s in sorted(set(claimed)))
            print(f"LABEL   {clip['file']}: page says {shown}, clip is "
                  f"{actual // 60}:{actual % 60:02d}")
            problems += 1

    # The page prints what the listener hears. A transcript that has been tidied
    # or corrected by hand reads as a faithful copy and is not one.
    notes = page_notes()
    for clip in config["clips"]:
        note = notes.get(clip["file"])
        if note is None:
            print(f"NOTE    {clip['file']}: no note for this clip on the tour page")
            problems += 1
            continue
        if note["label"].casefold() != VERBATIM_LABEL:
            continue
        if note["text"] != " ".join(clip["text"].split()):
            print(f"SPOKEN  {clip['file']}: the tour page's transcript differs from the record")
            problems += 1
    known = {clip["file"] for clip in config["clips"]}
    for name in sorted(set(notes) - known):
        print(f"NOTE    {name}: note on the tour page with no recorded clip")
        problems += 1

    print(f"checked {len(config['clips'])} clip(s), {problems} problem(s)")
    return 1 if problems else 0


def load_client():
    """Build the Fish Audio client with the key from the owner's env file."""
    if not VOICE_LAB.is_dir():
        raise SystemExit(f"voice lab not found at {VOICE_LAB}")
    sys.path.insert(0, str(VOICE_LAB))
    from fishaudio import FishAudio  # noqa: PLC0415
    from generate_fish_set import read_key  # noqa: PLC0415

    return FishAudio(api_key=read_key())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="regenerate just the clip with this file name")
    parser.add_argument("--check", action="store_true", help="verify without calling the API")
    args = parser.parse_args(argv)

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if args.check:
        return check(config, manifest)

    client = load_client()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0

    for clip in config["clips"]:
        if args.only and clip["file"] != args.only:
            continue
        audio = client.tts.convert(
            text=clip["text"],
            reference_id=config["reference_id"],
            format="mp3",
            model=config["model"],
        )
        data = bytes(audio)
        (OUT_DIR / clip["file"]).write_bytes(data)
        clip["bytes"] = len(data)
        written += 1
        print(f"wrote {clip['file']}: {len(data)} bytes")

    if not written:
        print("nothing matched --only; no clip regenerated")
        return 1

    CONFIG.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Keep the manifest's hash and spoken text in step with the files just
    # written, so the provenance record cannot describe a different clip.
    by_path = {a["path"]: a for a in manifest["assets"]}
    for clip in config["clips"]:
        entry = by_path.get(f"{REL_DIR}/{clip['file']}")
        if entry is None:
            continue
        entry["hash"] = hashlib.sha256((OUT_DIR / clip["file"]).read_bytes()).hexdigest()
        entry["spoken_text"] = clip["text"]

    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"updated {CONFIG.name} and {MANIFEST.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
