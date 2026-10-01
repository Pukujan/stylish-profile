#!/usr/bin/env python3
"""Fail the `gates` check when a profile page points at a file that is not committed.

The profile README and its HTML demo link images, audio clips, and each other by
repository-relative path. A renamed asset silently turns those into 404s on
github.com, which no schema validator catches. This walks the tracked Markdown
and HTML, resolves every relative reference, and exits non-zero on a miss.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SCANNED_SUFFIXES = (".md", ".html")
SKIPPED_DIRS = {".git", ".continuity", "node_modules", "__pycache__"}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
HTML_REFERENCE = re.compile(
    r"<(?:img|source|audio|video|a|link)\b[^>]*?\b(?:src|href)\s*=\s*[\"']([^\"']+)[\"']",
    re.IGNORECASE,
)
EXTERNAL_SCHEMES = ("http://", "https://", "//", "mailto:", "data:", "#")


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


def main() -> int:
    problems: list[str] = []
    checked = 0
    for source in tracked_files():
        for reference in references(source.read_text(encoding="utf-8")):
            target = resolve(source, reference)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                problems.append(
                    f"{source.relative_to(ROOT)}: {reference} -> missing {target.relative_to(ROOT)}"
                )
    if problems:
        print(f"INVALID: {len(problems)} unresolved local reference(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"VALID: {checked} local reference(s) resolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
