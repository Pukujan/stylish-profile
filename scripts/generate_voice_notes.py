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
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOICE_LAB = Path("D:/claude/hades-voice-lab")
CONFIG = REPO_ROOT / ".content-system" / "voice-notes.json"
MANIFEST = REPO_ROOT / ".content-system" / "asset-manifest.json"
OUT_DIR = REPO_ROOT / "assets" / "profile" / "voice-notes"
REL_DIR = "assets/profile/voice-notes"


def load_client():
    """Build the Fish Audio client with the key from the owner's env file."""
    if not VOICE_LAB.is_dir():
        raise SystemExit(f"voice lab not found at {VOICE_LAB}")
    sys.path.insert(0, str(VOICE_LAB))
    from fishaudio import FishAudio  # noqa: PLC0415
    from generate_fish_set import read_key  # noqa: PLC0415

    return FishAudio(api_key=read_key())


def check(config: dict, manifest: dict) -> int:
    """Report any clip whose bytes, hash or recorded text disagree."""
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
    print(f"checked {len(config['clips'])} clip(s), {problems} problem(s)")
    return 1 if problems else 0


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
