#!/usr/bin/env python3
"""Fail the `gates` check when a reference resolves to nothing.

The profile README and its HTML demo link images, audio clips, and each other by
repository-relative path. A renamed asset silently turns those into 404s on
github.com, which no schema validator catches. This walks the tracked Markdown
and HTML, resolves every relative reference, and exits non-zero on a miss.

The asset manifest is checked the same way, because it is the record of where
each committed image, chart and clip came from: an entry whose hash no longer
matches its file points at bytes that are not there any more. Nothing else in
the suite compares the two, which is how eight stale hashes sat in the record
while every other check stayed green.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".content-system" / "asset-manifest.json"
SCANNED_SUFFIXES = (".md", ".html")
SKIPPED_DIRS = {".git", ".continuity", "node_modules", "__pycache__"}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
HTML_REFERENCE = re.compile(
    r"<(?:img|source|audio|video|a|link)\b[^>]*?\b(?:src|href)\s*=\s*[\"']([^\"']+)[\"']",
    re.IGNORECASE,
)
EXTERNAL_SCHEMES = ("http://", "https://", "//", "mailto:", "data:", "#")

PAGES_HOST = "pukujan.github.io"
PAGES_PREFIX = "/stylish-profile/"
AUDIO_SUFFIXES = (".mp3", ".wav", ".m4a", ".ogg", ".flac")


def remote_audio_problem(reference: str) -> str | None:
    """Reject audio links that cannot play, and audio links with no committed file.

    A repository blob URL renders a file viewer with a Raw button, not a player,
    so a voice note linked that way silently does nothing when clicked. GitHub
    Pages serves the same bytes as `audio/mp3`, which the browser plays on click.
    Absolute URLs are skipped by the local resolver below, so without this the
    whole class of dead audio links passes the gate.
    """
    parsed = urlparse(reference)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path.lower().endswith(AUDIO_SUFFIXES):
        return None
    host = parsed.netloc.lower()
    if host == "github.com" and "/blob/" in path:
        return "points at a file-viewer page, which cannot play; link the Pages URL"
    if host != PAGES_HOST:
        return None
    if not path.startswith(PAGES_PREFIX):
        return f"is hosted at {PAGES_HOST} but outside {PAGES_PREFIX}"
    target = ROOT / path[len(PAGES_PREFIX):]
    if not target.exists():
        return f"resolves to {target.relative_to(ROOT)}, which is not committed"
    return None


def tracked_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCANNED_SUFFIXES:
            continue
        if SKIPPED_DIRS & set(path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def references(text: str) -> list[str]:
    found = MARKDOWN_LINK.findall(text)
    found.extend(HTML_REFERENCE.findall(text))
    return found


def resolve(source: Path, reference: str) -> Path | None:
    if not reference or reference.lower().startswith(EXTERNAL_SCHEMES):
        return None
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc:
        return None
    relative = unquote(parsed.path).lstrip("/")
    if not relative:
        return None
    if reference.startswith("/"):
        return ROOT / relative
    return source.parent / relative


def manifest_hashes() -> tuple[list[str], int]:
    """Every recorded hash that does not match the file it names, and how many were read."""
    if not MANIFEST.is_file():
        return [], 0
    entries = json.loads(MANIFEST.read_text(encoding="utf-8")).get("assets", [])
    problems: list[str] = []
    checked = 0
    for entry in entries:
        path = entry.get("path")
        recorded = entry.get("hash")
        if not path or not recorded:
            continue
        checked += 1
        target = ROOT / path
        if not target.is_file():
            problems.append(f"{path}: recorded in the manifest but not committed")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != recorded:
            problems.append(
                f"{path}: recorded hash {recorded[:12]} does not match the committed file"
            )
    return problems, checked


def main() -> int:
    problems: list[str] = []
    checked = 0
    for source in tracked_files():
        for reference in references(source.read_text(encoding="utf-8")):
            problem = remote_audio_problem(reference)
            if problem:
                problems.append(f"{source.relative_to(ROOT)}: {reference} {problem}")
                continue
            target = resolve(source, reference)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                problems.append(
                    f"{source.relative_to(ROOT)}: {reference} -> missing {target.relative_to(ROOT)}"
                )
    recorded_problems, recorded = manifest_hashes()
    problems.extend(recorded_problems)
    if problems:
        print(f"INVALID: {len(problems)} unresolved reference(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"VALID: {checked} local reference(s) resolved, {recorded} recorded hash(es) matched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
