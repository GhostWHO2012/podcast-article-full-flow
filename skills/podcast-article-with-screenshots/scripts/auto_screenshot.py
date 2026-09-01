#!/usr/bin/env python3
"""Extract candidate screenshots from a video using subtitle timing cues.

This helper intentionally stays simple: it parses SRT timestamps, scores cues by
optional keywords and text density, then calls ffmpeg for a small set of frames.
Human review is still required for final image quality and article placement.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
from dataclasses import dataclass


TIME_RE = re.compile(
    r"(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2}),(?P<ms>\d{3})\s+-->\s+"
    r"(?P<h2>\d{2}):(?P<m2>\d{2}):(?P<s2>\d{2}),(?P<ms2>\d{3})"
)


@dataclass
class Cue:
    start: float
    end: float
    text: str
    score: int


def parse_time(match: re.Match[str], suffix: str = "") -> float:
    return (
        int(match.group(f"h{suffix}")) * 3600
        + int(match.group(f"m{suffix}")) * 60
        + int(match.group(f"s{suffix}"))
        + int(match.group(f"ms{suffix}")) / 1000
    )


def read_srt(path: pathlib.Path, keywords: list[str]) -> list[Cue]:
    raw = path.read_text(encoding="utf-8-sig", errors="ignore")
    blocks = re.split(r"\n\s*\n", raw.replace("\r\n", "\n"))
    cues: list[Cue] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        time_line_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if time_line_index is None:
            continue
        match = TIME_RE.search(lines[time_line_index])
        if not match:
            continue
        text = " ".join(lines[time_line_index + 1 :])
        if not text:
            continue
        score = len(text)
        for kw in keywords:
            if kw and kw.lower() in text.lower():
                score += 100
        if re.search(r"\d|%|美元|AI|产品|演示|图表|案例|公司|创始人|模型|机器人", text, re.I):
            score += 30
        cues.append(Cue(parse_time(match), parse_time(match, "2"), text, score))
    return cues


def fmt_timestamp(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}-{m:02d}-{s:02d}"


def extract_frame(video: pathlib.Path, out_file: pathlib.Path, timestamp: float) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{timestamp:.3f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(out_file),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=pathlib.Path)
    parser.add_argument("--srt", required=True, type=pathlib.Path)
    parser.add_argument("--out", required=True, type=pathlib.Path)
    parser.add_argument("--keywords", default="")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument(
        "--bucket-seconds",
        type=int,
        default=90,
        help="Minimum time spacing bucket for candidates. Larger values reduce repeated scenes.",
    )
    args = parser.parse_args()

    keywords = [kw.strip() for kw in re.split(r"[,，]", args.keywords) if kw.strip()]
    cues = read_srt(args.srt, keywords)
    if not cues:
        raise SystemExit("No subtitle cues found.")

    # Keep candidates spread through the video. These are candidates, not final picks:
    # article assembly should still remove repeated talking-head frames.
    selected: list[Cue] = []
    used_buckets: set[int] = set()
    for cue in sorted(cues, key=lambda c: c.score, reverse=True):
        bucket = int(cue.start // max(1, args.bucket_seconds))
        if bucket in used_buckets:
            continue
        selected.append(cue)
        used_buckets.add(bucket)
        if len(selected) >= args.count:
            break

    args.out.mkdir(parents=True, exist_ok=True)
    manifest_lines = [
        "# Screenshot Candidates",
        "",
        "These are candidates only. Select fewer final images when frames repeat the same interview setup.",
        "",
    ]
    for idx, cue in enumerate(sorted(selected, key=lambda c: c.start), 1):
        shot_time = cue.start + min(1.0, max(0.0, (cue.end - cue.start) / 2))
        filename = f"img{idx:02d}_{fmt_timestamp(shot_time)}.png"
        out_file = args.out / filename
        extract_frame(args.video, out_file, shot_time)
        manifest_lines.extend(
            [
                f"## {filename}",
                "",
                f"- Timestamp: {shot_time:.3f}s",
                f"- Cue: {cue.text[:220]}",
                f"- Score: {cue.score}",
                "",
            ]
        )

    (args.out / "screenshot_candidates.md").write_text(
        "\n".join(manifest_lines), encoding="utf-8"
    )
    print(f"Extracted {len(selected)} screenshots to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
