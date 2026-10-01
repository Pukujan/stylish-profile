#!/usr/bin/env python3
"""Regenerate the live activity data behind the profile page.

The profile shows what changed recently on a page no editor opens every
morning. This script keeps that current. It asks GitHub which commits the
owner authored, in which public active repositories, over the last N days;
writes the answer as machine-readable JSON; draws one flat cream SVG chart;
and rewrites the TRACKING blocks in the profile README and the HTML demo
page.

Every output is a pure function of the collected data plus the local date --
never a wall-clock minute -- so two runs against unchanged data leave every
byte identical and the workflow commits only when something actually moved.
If any API request fails after its retries, or a page file has a broken
marker pair, the script exits non-zero before writing anything: a late
refresh beats an empty one.

Commit counts come from the commits endpoint, never the public events feed.
As of 2026-10-01 the events API trims PushEvent payloads to
{before, head, push_id, ref, repository_id}, which carries no commit list.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

API_BASE = "https://api.github.com"
API_VERSION = "2022-11-28"
USER_AGENT = "stylish-profile-tracker"
MAX_ATTEMPTS = 4  # one request plus up to three retries
BACKOFF_SECONDS = (1, 2, 4)
REQUEST_TIMEOUT = 30

START_MARKER = "<!-- TRACKING:START -->"
END_MARKER = "<!-- TRACKING:END -->"

RAW_URL_ROOT = "https://raw.githubusercontent.com"

INK = "#1A1A1A"
BLUE = "#4169E1"
YELLOW = "#FFD93D"
ORANGE = "#FF8C42"
CREAM = "#FFF9F0"
FONT_STACK = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

MAX_REPO_ROWS = 40
SCHEMA_VERSION = "stylish-profile.tracking.v1"

# The charts this script writes are recorded in the asset manifest with a
# committed hash. Refreshing the SVG without refreshing that hash is how the
# record goes stale on the first scheduled run, so the write-back below is part
# of the same transaction as the chart itself.
MANIFEST_PATH = Path(".content-system") / "asset-manifest.json"
GENERATED_DIR = Path("assets/profile/generated")


class TrackerError(Exception):
    """Fatal problem with a clear message for the operator."""

class EmptyRepository(Exception):
    """A repository that exists but has no commits yet.

    The commits endpoint answers 409 Conflict for these, which is not an
    error worth aborting a run over: the honest answer is zero commits.
    """


def log(message: str) -> None:
    print(message)


# --------------------------------------------------------------------------
# CLI and credentials
# --------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Regenerate profile tracking data from the GitHub API."
    )
    parser.add_argument("--owner", default="Pukujan", help="GitHub login to track")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root to write into (default: this repo)",
    )
    parser.add_argument(
        "--tz-offset",
        type=int,
        default=-4,
        help="local timezone offset from UTC in whole hours (default: -4)",
    )
    parser.add_argument(
        "--days", type=int, default=14, help="chart window in days (default: 14)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="compute and print a summary of what would change; write nothing",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="GitHub token; falls back to GITHUB_TOKEN then GH_TOKEN",
    )
    args = parser.parse_args(argv)
    if not 1 <= args.days <= 90:
        parser.error("--days must be between 1 and 90")
    if not -12 <= args.tz_offset <= 14:
        parser.error("--tz-offset must be between -12 and 14")
    return args


def resolve_token(args: argparse.Namespace) -> str:
    token = args.token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise TrackerError(
            "no GitHub token: pass --token or set GITHUB_TOKEN or GH_TOKEN "
            "(the token value is never printed)"
        )
    return token


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

NEXT_LINK = re.compile(r'<([^>]+)>;\s*rel="next"')


def _retryable(status: int, headers) -> bool:
    if status >= 500:
        return True
    if status in (403, 429):
        return headers.get("x-ratelimit-remaining") == "0"
    return False


def fetch_json(
    url: str, token: str, empty_ok: bool = False
) -> tuple[object, str | None]:
    """GET one API URL; return (decoded body, raw Link header or None).

    Retries transient failures up to three times with a short backoff, then
    raises TrackerError. Callers treat any raise as "write nothing". With
    empty_ok set, a 409 means "repository has no commits" and raises
    EmptyRepository instead of aborting the run.
    """
    last_problem = "unknown error"
    for attempt in range(MAX_ATTEMPTS):
        if attempt:
            time.sleep(BACKOFF_SECONDS[min(attempt - 1, len(BACKOFF_SECONDS) - 1)])
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": API_VERSION,
                "User-Agent": USER_AGENT,
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
                body = json.loads(response.read().decode("utf-8"))
                return body, response.headers.get("Link")
        except urllib.error.HTTPError as error:
            if empty_ok and error.code == 409:
                raise EmptyRepository(url) from error
            if _retryable(error.code, error.headers):
                last_problem = f"HTTP {error.code} (server or rate limit)"
                continue
            raise TrackerError(f"{url}: HTTP {error.code} {error.reason}") from error
        except (urllib.error.URLError, TimeoutError) as error:
            last_problem = f"network failure: {error}"
            continue
        except json.JSONDecodeError as error:
            raise TrackerError(f"{url}: response was not valid JSON") from error
    raise TrackerError(
        f"{url}: giving up after {MAX_ATTEMPTS} attempts, {last_problem}"
    )


def fetch_paginated(url: str, token: str, empty_ok: bool = False) -> list:
    """Collect every page of a list endpoint, following Link rel="next"."""
    items: list = []
    next_url: str | None = url
    while next_url:
        body, link = fetch_json(next_url, token, empty_ok=empty_ok)
        if not isinstance(body, list):
            raise TrackerError(f"{next_url}: expected a JSON array")
        items.extend(body)
        match = NEXT_LINK.search(link) if link else None
        next_url = match.group(1) if match else None
    return items


# --------------------------------------------------------------------------
# Time helpers
# --------------------------------------------------------------------------

def local_tz(offset_hours: int) -> timezone:
    return timezone(timedelta(hours=offset_hours))


def local_now(offset_hours: int) -> datetime:
    return datetime.now(timezone.utc).astimezone(local_tz(offset_hours))


def iso_utc(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc(stamp: str) -> datetime:
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def local_date_of(stamp: str, offset_hours: int) -> str:
    return parse_utc(stamp).astimezone(local_tz(offset_hours)).strftime("%Y-%m-%d")


def push_seconds(stamp: str) -> float:
    """Sortable seconds for an API timestamp; 0 when missing or unparseable."""
    try:
        return parse_utc(stamp).timestamp()
    except (ValueError, TypeError):
        return 0.0


def window_dates(today: date, days: int) -> list[str]:
    start = today - timedelta(days=days - 1)
    return [(start + timedelta(days=delta)).strftime("%Y-%m-%d") for delta in range(days)]


# --------------------------------------------------------------------------
# Data collection
# --------------------------------------------------------------------------

def collect(owner: str, token: str, offset_hours: int, days: int) -> dict:
    """Fetch repos and windowed commits. Raises TrackerError on any failure."""
    now = local_now(offset_hours)
    today_str = now.strftime("%Y-%m-%d")
    dates = window_dates(now.date(), days)
    first_local = datetime.combine(
        now.date() - timedelta(days=days - 1),
        datetime.min.time(),
        tzinfo=local_tz(offset_hours),
    )
    since = iso_utc(first_local)
    until = iso_utc(now)
    log(f"window: {dates[0]} .. {today_str} (local UTC{offset_hours:+d})")

    repos_raw = fetch_paginated(
        f"{API_BASE}/users/{owner}/repos"
        "?per_page=100&sort=pushed&direction=desc&type=owner",
        token,
    )
    kept = [r for r in repos_raw if not r.get("fork") and not r.get("archived")]
    log(f"kept {len(kept)} of {len(repos_raw)} repositories (non-fork, non-archived)")

    per_repo: dict[str, dict] = {}
    for repo in kept:
        name = repo["name"]
        try:
            commits = fetch_paginated(
                f"{API_BASE}/repos/{owner}/{name}/commits"
                f"?author={owner}&since={since}&until={until}&per_page=100",
                token,
                empty_ok=True,
            )
        except EmptyRepository:
            # A repository with no commits at all answers 409 here. That is
            # zero commits, not a failure.
            log(f"  {name}: no commits yet (empty repository)")
            commits = []
        by_day: dict[str, int] = {}
        for item in commits:
            stamp = item.get("commit", {}).get("author", {}).get("date")
            if not stamp:
                continue
            day = local_date_of(stamp, offset_hours)
            if dates[0] <= day <= today_str:
                by_day[day] = by_day.get(day, 0) + 1
        per_repo[name] = {
            "by_day": by_day,
            "pushed_at": repo.get("pushed_at") or "",
            "language": repo.get("language") or "",
            "stars": int(repo.get("stargazers_count") or 0),
            "html_url": repo.get("html_url") or f"https://github.com/{owner}/{name}",
        }
        log(f"  {name}: {sum(by_day.values())} commit(s) in window")

    return {"owner": owner, "dates": dates, "per_repo": per_repo}


def derive(data: dict) -> tuple[dict, dict]:
    """Return (tracking json payload, render context)."""
    owner = data["owner"]
    dates = data["dates"]
    per_repo = data["per_repo"]
    today_str = dates[-1]

    def repo_rows(pairs: list[tuple[str, int]]) -> list[dict]:
        ordered = sorted(pairs, key=lambda pair: (-pair[1], pair[0].lower()))
        return [
            {
                "repo": name,
                "commits": count,
                "html_url": per_repo[name]["html_url"],
                "pushed_at": per_repo[name]["pushed_at"],
            }
            for name, count in ordered
            if count > 0
        ]

    today_rows = repo_rows(
        [(name, info["by_day"].get(today_str, 0)) for name, info in per_repo.items()]
    )
    today_total = sum(row["commits"] for row in today_rows)

    daily = [
        {
            "date": day,
            "commits": sum(info["by_day"].get(day, 0) for info in per_repo.values()),
        }
        for day in dates
    ]

    week_dates = dates[-7:] if len(dates) >= 7 else list(dates)
    week_rows = repo_rows(
        [
            (name, sum(info["by_day"].get(day, 0) for day in week_dates))
            for name, info in per_repo.items()
        ]
    )
    week_total = sum(row["commits"] for row in week_rows)

    current_project = None
    if week_rows:
        # Most commits; ties break on the most recent push, then repo name.
        best = max(
            sorted(week_rows, key=lambda row: row["repo"].lower()),
            key=lambda row: (row["commits"], push_seconds(row["pushed_at"])),
        )
        info = per_repo[best["repo"]]
        current_project = {
            "name": best["repo"],
            "commits": best["commits"],
            "pushed_at": info["pushed_at"],
            "language": info["language"],
            "stars": info["stars"],
            "html_url": info["html_url"],
        }

    stars_total = sum(info["stars"] for info in per_repo.values())
    stars_top = sorted(
        (
            {
                "repo": name,
                "stars": info["stars"],
                "html_url": info["html_url"],
            }
            for name, info in per_repo.items()
            if info["stars"] > 0
        ),
        key=lambda row: (-row["stars"], row["repo"].lower()),
    )

    rows_by_name = sorted(
        (
            {
                "name": name,
                "pushed_at": info["pushed_at"],
                "language": info["language"],
                "stars": info["stars"],
                "html_url": info["html_url"],
            }
            for name, info in per_repo.items()
        ),
        key=lambda row: row["name"].lower(),
    )
    repos = sorted(
        rows_by_name,
        key=lambda row: (-push_seconds(row["pushed_at"]), row["name"].lower()),
    )[:MAX_REPO_ROWS]

    payload = {
        "schema_version": SCHEMA_VERSION,
        "owner": owner,
        "generated_date": today_str,
        "today": {"date": today_str, "commits": today_total, "projects": today_rows},
        "daily": daily,
        "week": {"commits": week_total, "projects": week_rows},
        "current_project": current_project,
        "stars": {"total": stars_total, "top": stars_top},
        "repos": repos,
    }

    # For the "zero commits today" sentence: the newest local day anywhere in
    # the window, and which repos have commits on it.
    best_day = None
    for row in reversed(daily):
        if row["commits"] > 0:
            best_day = row["date"]
            break
    most_recent = None
    if best_day:
        names = sorted(
            (
                name
                for name, info in per_repo.items()
                if info["by_day"].get(best_day, 0) > 0
            ),
            key=str.lower,
        )
        most_recent = {"date": best_day, "repos": names}

    context = {
        "most_recent_day": most_recent,
        "newest_repo": repos[0]["name"] if repos else None,
        "window_days": len(dates),
    }
    return payload, context


def render_json(payload: dict) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=True) + "\n"


# --------------------------------------------------------------------------
# SVG rendering
# --------------------------------------------------------------------------

def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def grow_animation(
    bar_y: float, bar_h: float, baseline: float, delay: float
) -> str:
    """SMIL children that grow one bar from the baseline to its real height.

    SMIL is used instead of CSS keyframes because it needs no transform-box or
    transform-origin support, and every browser GitHub renders in runs it.
    The caller writes the final geometry on the rect itself, so a renderer that
    ignores SMIL still shows the finished static chart; the animation only ever
    replays the growth and freezes back onto those same numbers.
    """
    if bar_h <= 2.0:
        return ""
    timing = 'dur="0.55s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"'
    begin = f'begin="{delay:.2f}s"'
    return (
        f'<animate attributeName="y" from="{baseline:.1f}" to="{bar_y:.1f}"'
        f" {begin} {timing}/>"
        f'<animate attributeName="height" from="0" to="{bar_h:.1f}"'
        f" {begin} {timing}/>"
    )


def clip(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 1] + "-"

# GitHub keeps <picture>/<source media> intact in markdown (it wraps the pair in
# a themed-picture element), so a narrow chart can be served to phones without
# any script. 640px covers phones and small tablets in portrait.
PHONE_MEDIA = "(max-width: 640px)"

# The dark field matches the page background so a chart sits flush on a dark
# page instead of showing a lit rectangle, and the ink becomes the light ink.
# The accents are lifted, because the royal blue used for the bars is tuned to
# carry against cream and goes muddy against near-black.
DARK_PALETTE = {
    CREAM: "#0F0F0F",
    INK: "#EDEDED",
    BLUE: "#7A9BFF",
    YELLOW: "#FFE066",
    ORANGE: "#FFA05C",
}



def picture_block(raw_base: str, wide: str, narrow: str, alt: str) -> list[str]:
    """Markdown lines for one chart that swaps layout on phones and on dark pages.

    One picture element, four sources. The colour swap has to go through
    `prefers-color-scheme` rather than a `#gh-dark-mode-only` fragment, because
    GitHub's theme rule matches the anchor it wraps around a bare image and a
    `<picture>` gets no such anchor: an image inside a picture keeps the
    fragment on its `src`, which nothing matches, so both modes render at once.
    The chart needs the phone variant as well, and a bare image cannot carry
    one, so `prefers-color-scheme` is the only mechanism that does both.

    Order matters. The two dark sources come first so a dark phone picks the
    dark narrow chart; the last source is the fallback for anything that
    matched nothing, which is the light chart at full width.
    """
    stem_wide, stem_narrow = wide[:-4], narrow[:-4]
    return [
        "<picture>",
        f'<source media="(prefers-color-scheme: dark) and {PHONE_MEDIA}"'
        f' srcset="{raw_base}/{stem_narrow}-dark.svg">',
        f'<source media="(prefers-color-scheme: dark)"'
        f' srcset="{raw_base}/{stem_wide}-dark.svg">',
        f'<source media="{PHONE_MEDIA}" srcset="{raw_base}/{narrow}">',
        f'<img src="{raw_base}/{wide}" alt="{alt}" width="100%">',
        "</picture>",
    ]

def dark_svg(markup: str) -> str:
    """Return the same chart drawn on the dark field.

    The charts use four literal colours and nothing else, so a dark copy is the
    same markup with the palette swapped. Substituting the finished string keeps
    the light renderers untouched, and the literals are unambiguous: the only
    non-hex value any fill attribute carries is the SMIL keyword "freeze".
    """
    for light, dark in DARK_PALETTE.items():
        markup = markup.replace(light, dark)
    return markup


def svg_open(width: int, height: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
        f' viewBox="0 0 {width} {height}" role="img">',
        f"<title>{esc(title)}</title>",
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="24" fill="{CREAM}"/>',
        f'<g font-family="{FONT_STACK}">',
    ]


def activity_alt(payload: dict) -> str:
    total = sum(row["commits"] for row in payload["daily"])
    return (
        f"Daily commit counts across public {payload['owner']} repositories "
        f"over the last {len(payload['daily'])} days, {total} total."
    )

def render_activity_svg(payload: dict) -> str:
    daily = payload["daily"]
    days = len(daily)
    total = sum(row["commits"] for row in daily)
    max_count = max((row["commits"] for row in daily), default=0)
    today = payload["today"]
    lines = svg_open(1000, 340, f"Commits in the last {days} days: {total} total")

    lines.append(
        f'<text x="32" y="44" font-size="24" font-weight="600" fill="{INK}">'
        f"Commits in the last {days} days</text>"
    )
    lines.append(
        f'<text x="32" y="70" font-size="15" fill="{INK}">'
        f"{total} commit(s) total, {today['commits']} today ({today['date']})"
        "</text>"
    )

    baseline = 272.0
    chart_top = 96.0
    chart_left = 40.0
    chart_right = 600.0
    slot = (chart_right - chart_left) / days
    bar_w = min(24.0, slot * 0.6)

    lines.append(
        f'<line x1="{chart_left - 8:.1f}" y1="{baseline:.1f}"'
        f' x2="{chart_right:.1f}" y2="{baseline:.1f}" stroke="{INK}"'
        ' stroke-width="3" stroke-linecap="round"/>'
    )

    label_step = max(1, -(-days // 7))
    for index, row in enumerate(daily):
        x = chart_left + index * slot + (slot - bar_w) / 2
        count = row["commits"]
        is_today = index == days - 1
        if count == 0 or max_count == 0:
            bar_h, bar_y = 2.0, baseline - 2.0
        else:
            bar_h = max(6.0, round(count / max_count * (baseline - chart_top)))
            bar_y = baseline - bar_h
        rx = min(6.0, bar_w / 2)
        fill = ORANGE if is_today else BLUE
        animation = grow_animation(bar_y, bar_h, baseline, index * 0.06)
        lines.append(
            f'<rect x="{x:.1f}" y="{bar_y:.1f}" width="{bar_w:.1f}"'
            f' height="{bar_h:.1f}" rx="{rx:.1f}" fill="{fill}">{animation}</rect>'
        )
        if index % label_step == 0 or is_today:
            lines.append(
                f'<text x="{x + bar_w / 2:.1f}" y="300" font-size="12" fill="{INK}"'
                f' text-anchor="middle">{esc(row["date"][5:])}</text>'
            )

    lines.append(
        f'<line x1="624" y1="92" x2="624" y2="308" stroke="{INK}"'
        ' stroke-width="3" stroke-linecap="round" opacity="0.35"/>'
    )
    panel_x = 648
    lines.append(
        f'<text x="{panel_x}" y="112" font-size="18" font-weight="600"'
        f' fill="{INK}">Today ({esc(today["date"])})</text>'
    )
    projects = today["projects"]
    if not projects:
        lines.append(
            f'<text x="{panel_x}" y="146" font-size="14" fill="{INK}">'
            "No commits today.</text>"
        )
    else:
        max_today = max(row["commits"] for row in projects)
        shown = projects[:6]
        for index, row in enumerate(shown):
            y = 142 + index * 30
            lines.append(
                f'<text x="{panel_x}" y="{y}" font-size="13" fill="{INK}">'
                f"{esc(clip(row['repo'], 22))}</text>"
            )
            bar_len = max(6, round(row["commits"] / max_today * 150))
            delay = 0.5 + index * 0.12
            lines.append(
                f'<rect x="{panel_x}" y="{y + 6}" width="{bar_len}" height="10"'
                f' rx="5" fill="{BLUE}">'
                f'<animate attributeName="width" from="0" to="{bar_len}"'
                f' begin="{delay:.2f}s" dur="0.45s" fill="freeze"'
                f' calcMode="spline" keySplines="0.2 0.8 0.2 1"/>'
                "</rect>"
            )
            lines.append(
                f'<text x="968" y="{y}" font-size="13" fill="{INK}"'
                f' text-anchor="end">{row["commits"]}</text>'
            )
        if len(projects) > len(shown):
            lines.append(
                f'<text x="{panel_x}" y="{142 + len(shown) * 30}" font-size="13"'
                f' fill="{INK}">+{len(projects) - len(shown)} more project(s)'
                "</text>"
            )

    lines.append("</g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def render_activity_svg_narrow(payload: dict) -> str:
    """The same activity chart stacked for a phone.

    A 1000px-wide chart scaled into a 390px column renders its labels at about
    five pixels, so the page serves this taller variant to small screens
    through a <picture><source media="(max-width: 640px)"> element. It carries
    the same numbers as the wide chart, only rearranged: chart on top, today's
    projects underneath instead of beside.
    """
    daily = payload["daily"]
    days = len(daily)
    total = sum(row["commits"] for row in daily)
    max_count = max((row["commits"] for row in daily), default=0)
    today = payload["today"]
    width, height = 560, 560
    lines = svg_open(width, height, f"Commits in the last {days} days: {total} total")

    lines.append(
        f'<text x="24" y="38" font-size="22" font-weight="600" fill="{INK}">'
        f"Commits in the last {days} days</text>"
    )
    lines.append(
        f'<text x="24" y="62" font-size="15" fill="{INK}">'
        f"{total} total, {today['commits']} today ({today['date']})</text>"
    )

    baseline = 268.0
    chart_top = 92.0
    chart_left = 24.0
    chart_right = 536.0
    slot = (chart_right - chart_left) / days
    bar_w = min(20.0, slot * 0.62)

    lines.append(
        f'<line x1="{chart_left:.1f}" y1="{baseline:.1f}"'
        f' x2="{chart_right:.1f}" y2="{baseline:.1f}" stroke="{INK}"'
        ' stroke-width="3" stroke-linecap="round"/>'
    )

    label_step = max(1, -(-days // 4))
    for index, row in enumerate(daily):
        x = chart_left + index * slot + (slot - bar_w) / 2
        count = row["commits"]
        is_today = index == days - 1
        if count == 0 or max_count == 0:
            bar_h, bar_y = 2.0, baseline - 2.0
        else:
            bar_h = max(6.0, round(count / max_count * (baseline - chart_top)))
            bar_y = baseline - bar_h
        rx = min(5.0, bar_w / 2)
        fill = ORANGE if is_today else BLUE
        animation = grow_animation(bar_y, bar_h, baseline, index * 0.06)
        lines.append(
            f'<rect x="{x:.1f}" y="{bar_y:.1f}" width="{bar_w:.1f}"'
            f' height="{bar_h:.1f}" rx="{rx:.1f}" fill="{fill}">{animation}</rect>'
        )
        if index % label_step == 0 or is_today:
            lines.append(
                f'<text x="{x + bar_w / 2:.1f}" y="{baseline + 22:.1f}"'
                f' font-size="12" fill="{INK}" text-anchor="middle">'
                f"{esc(row['date'][5:])}</text>"
            )

    lines.append(
        f'<line x1="24" y1="316" x2="536" y2="316" stroke="{INK}"'
        ' stroke-width="3" stroke-linecap="round" opacity="0.35"/>'
    )
    lines.append(
        f'<text x="24" y="350" font-size="18" font-weight="600" fill="{INK}">'
        f"Today ({esc(today['date'])})</text>"
    )

    projects = today["projects"]
    if not projects:
        lines.append(
            f'<text x="24" y="382" font-size="14" fill="{INK}">'
            "No commits today.</text>"
        )
    else:
        max_today = max(row["commits"] for row in projects)
        shown = projects[:6]
        for index, row in enumerate(shown):
            y = 378 + index * 30
            lines.append(
                f'<text x="24" y="{y}" font-size="13" fill="{INK}">'
                f"{esc(clip(row['repo'], 26))}</text>"
            )
            bar_len = max(6, round(row["commits"] / max_today * 300))
            lines.append(
                f'<rect x="240" y="{y - 11}" width="{bar_len}" height="12"'
                f' rx="6" fill="{BLUE}">'
                f'<animate attributeName="width" from="0" to="{bar_len}"'
                f' begin="{0.5 + index * 0.12:.2f}s" dur="0.45s" fill="freeze"'
                f' calcMode="spline" keySplines="0.2 0.8 0.2 1"/>'
                "</rect>"
            )
            lines.append(
                f'<text x="552" y="{y}" font-size="13" fill="{INK}"'
                f' text-anchor="end">{row["commits"]}</text>'
            )
        if len(projects) > len(shown):
            lines.append(
                f'<text x="24" y="{378 + len(shown) * 30}" font-size="13"'
                f' fill="{INK}">+{len(projects) - len(shown)} more project(s)'
                "</text>"
            )

    lines.append("</g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Block rendering (Markdown + HTML)
# --------------------------------------------------------------------------

def local_push_date(stamp: str, offset_hours: int) -> str:
    if not stamp:
        return "unknown"
    try:
        return local_date_of(stamp, offset_hours)
    except ValueError:
        return stamp[:10]




def summary_sentence(payload: dict, context: dict) -> str:
    today = payload["today"]
    if today["commits"] > 0:
        return (
            f"{today['date']}: {today['commits']} commit(s) "
            f"across {len(today['projects'])} project(s)."
        )
    recent = context["most_recent_day"]
    if recent:
        names = ", ".join(recent["repos"])
        return (
            f"{today['date']}: no commits today. The most recent day with "
            f"commits in the window was {recent['date']}, in {names}."
        )
    if context["newest_repo"]:
        return (
            f"{today['date']}: no commits today, and none in the tracking "
            f"window either; the newest repository is {context['newest_repo']}."
        )
    return f"{today['date']}: no commits today, and no repositories to track."




def current_line(payload: dict) -> str:
    current = payload["current_project"]
    if not current:
        return "no commits in the last 7 days, so nothing to feature"
    return (
        f"[{current['name']}]({current['html_url']}) with {current['commits']} "
        "commit(s) in the last 7 days"
    )


def current_text(payload: dict) -> str:
    current = payload["current_project"]
    if not current:
        return "no commits in the last 7 days, so nothing to feature"
    return (
        f"{current['name']} with {current['commits']} commit(s) in the last 7 days"
    )


def render_markdown_block(
    payload: dict, context: dict, offset_hours: int, raw_base: str
) -> list[str]:
    today = payload["today"]
    repos_url = f"https://github.com/{payload['owner']}?tab=repositories"

    lines = ["## What's fresh", "", summary_sentence(payload, context), ""]

    if today["commits"] > 0:
        lines += ["| Project | Last push |", "| --- | --- |"]
        for row in today["projects"]:
            lines.append(
                f"| [{row['repo']}]({row['html_url']}) | "
                f"{local_push_date(row['pushed_at'], offset_hours)} |"
            )
        lines.append("")

    lines += picture_block(
        raw_base, "activity.svg", "activity-narrow.svg", activity_alt(payload)
    )
    lines += [
        "",
        f"**Current project:** {current_line(payload)}.",
        "",
        f"[All repositories]({repos_url}).",
    ]
    return lines


def render_html_block(payload: dict, context: dict, offset_hours: int) -> list[str]:
    today = payload["today"]
    repos_url = f"https://github.com/{payload['owner']}?tab=repositories"

    lines = [
        "<h2>What's fresh</h2>",
        f"<p>{esc(summary_sentence(payload, context))}</p>",
    ]

    if today["commits"] > 0:
        lines += [
            "<table>",
            "<thead><tr><th>Project</th><th>Last push</th></tr></thead>",
            "<tbody>",
        ]
        for row in today["projects"]:
            lines.append(
                f'<tr><td><a href="{row["html_url"]}">{esc(row["repo"])}</a></td>'
                f"<td>{esc(local_push_date(row['pushed_at'], offset_hours))}</td></tr>"
            )
        lines += ["</tbody>", "</table>"]

    alt_a = activity_alt(payload)
    # The page defaults to dark and overrides to light, so the dark chart is the
    # fallback and the light ones are the media-matched overrides.
    lines += [
        '<figure class="wide-figure">',
        "<picture>",
        f'<source media="(prefers-color-scheme: light) and {PHONE_MEDIA}"'
        ' srcset="../assets/profile/generated/activity-narrow.svg">',
        '<source media="(prefers-color-scheme: light)"'
        ' srcset="../assets/profile/generated/activity.svg">',
        f'<source media="{PHONE_MEDIA}"'
        ' srcset="../assets/profile/generated/activity-narrow-dark.svg">',
        '<img src="../assets/profile/generated/activity-dark.svg"'
        f' alt="{esc(alt_a)}" width="100%">',
        "</picture>",
        f"<figcaption>{esc(alt_a)}</figcaption>",
        "</figure>",
    ]

    current = payload["current_project"]
    if current:
        lines.append(
            "<p>Current project: "
            f'<a href="{current["html_url"]}">{esc(current["name"])}</a>'
            f" with {current['commits']} commit(s) in the last 7 days.</p>"
        )
    else:
        lines.append(f"<p>Current project: {esc(current_text(payload))}.</p>")

    lines.append(f'<p><a href="{repos_url}">All repositories</a>.</p>')
    return lines


# --------------------------------------------------------------------------
# Block rewriting
# --------------------------------------------------------------------------

def marker_positions(text: str, source: Path) -> tuple[int, int]:
    """Return (index after START marker, index of END marker) or raise."""
    starts = [m.start() for m in re.finditer(re.escape(START_MARKER), text)]
    ends = [m.start() for m in re.finditer(re.escape(END_MARKER), text)]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        raise TrackerError(
            f"{source}: expected exactly one {START_MARKER} and one {END_MARKER} "
            f"in that order (found {len(starts)} start, {len(ends)} end)"
        )
    for pos in starts + ends:
        line_start = text.rfind("\n", 0, pos) + 1
        line_end = text.find("\n", pos)
        if line_end == -1:
            line_end = len(text)
        if text[line_start:line_end].strip() not in (START_MARKER, END_MARKER):
            raise TrackerError(
                f"{source}: tracking markers must sit on lines of their own"
            )
    return starts[0] + len(START_MARKER), ends[0]


def rewrite_block(
    text: str, source: Path, content_lines: list[str]
) -> str:
    insert_at, end_at = marker_positions(text, source)
    nl = "\r\n" if "\r\n" in text else "\n"
    body = nl.join(content_lines)
    return text[:insert_at] + nl + body + nl + text[end_at:]


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def build_outputs(
    root: Path, payload: dict, context: dict, offset_hours: int
) -> dict[Path, str]:
    """Compute every output string. Raises TrackerError before any write."""
    generated = root / "assets" / "profile" / "generated"
    raw_base = (
        f"{RAW_URL_ROOT}/{payload['owner']}/{root.name}/main"
        "/assets/profile/generated"
    )
    outputs: dict[Path, str] = {
        root / "profile" / "tracking.json": render_json(payload),
        generated / "activity.svg": render_activity_svg(payload),
        generated / "activity-narrow.svg": render_activity_svg_narrow(payload),
    }
    for light_name, dark_name in (
        ("activity.svg", "activity-dark.svg"),
        ("activity-narrow.svg", "activity-narrow-dark.svg"),
    ):
        outputs[generated / dark_name] = dark_svg(outputs[generated / light_name])
    manifest = with_chart_hashes(root, outputs)
    if manifest is not None:
        outputs[root / MANIFEST_PATH] = manifest
    targets = [
        (root / "profile" / "README.md", "md"),
        (root / "docs" / "index.html", "html"),
    ]
    for path, kind in targets:
        if not path.exists():
            continue
        with open(path, encoding="utf-8", newline="") as handle:
            text = handle.read()
        if kind == "md":
            content = render_markdown_block(payload, context, offset_hours, raw_base)
        else:
            content = render_html_block(payload, context, offset_hours)
        outputs[path] = rewrite_block(text, path, content)
    return outputs


def with_chart_hashes(root: Path, outputs: dict[Path, str]) -> str | None:
    """The manifest text with each generated chart's hash set from the SVG just drawn.

    The recorded hash has to come from the same string that is about to be
    written, or the two drift the moment the daily run fires. Returns None when
    the repository has no manifest, so the tracker still works in a checkout
    that has not adopted the content adapter.
    """
    path = root / MANIFEST_PATH
    if not path.is_file():
        return None
    manifest = json.loads(path.read_text(encoding="utf-8"))
    prefix = GENERATED_DIR.as_posix() + "/"
    for entry in manifest.get("assets", []):
        asset_path = entry.get("path", "")
        if not asset_path.startswith(prefix):
            continue
        content = outputs.get(root / asset_path)
        if content is None:
            continue
        entry["hash"] = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"

def summarize(
    payload: dict, outputs: dict[Path, str], dry_run: bool
) -> None:
    today = payload["today"]
    verb = "would write" if dry_run else "wrote"
    log("")
    log(f"date: {today['date']}")
    log(f"commits today: {today['commits']}")
    if today["projects"]:
        for row in today["projects"]:
            log(f"  {row['repo']}: {row['commits']}")
    else:
        log("  (no projects with commits today)")
    log(f"commits last 7 days: {payload['week']['commits']}")
    current = payload["current_project"]
    if current:
        log(
            f"current project: {current['name']} "
            f"({current['commits']} commit(s) this week, "
            f"pushed_at {current['pushed_at'] or 'unknown'}, "
            f"language {current['language'] or 'none'}, "
            f"stars {current['stars']})"
        )
    else:
        log("current project: none (no commits in the last 7 days)")
    log(
        f"stars total: {payload['stars']['total']} "
        f"across {len(payload['stars']['top'])} starred repo(s)"
    )
    log(f"repos tracked: {len(payload['repos'])}")
    log("")
    for path in sorted(outputs, key=str):
        digest = hashlib.sha256(outputs[path].encode("utf-8")).hexdigest()
        log(f"{verb} {path} (sha256 {digest})")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        token = resolve_token(args)
    except TrackerError as error:
        log(f"ERROR: {error}")
        return 1

    root = args.root.resolve()
    if not root.is_dir():
        log(f"ERROR: root does not exist: {root}")
        return 1

    try:
        data = collect(args.owner, token, args.tz_offset, args.days)
        payload, context = derive(data)
        outputs = build_outputs(root, payload, context, args.tz_offset)
    except TrackerError as error:
        log(f"ERROR: {error}")
        log("no files were written")
        return 1

    summarize(payload, outputs, args.dry_run)

    if args.dry_run:
        log("")
        log("dry run: nothing written")
        return 0

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(content.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
