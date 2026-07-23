#!/usr/bin/env python3
"""
Subtitle to TXT converter — Convert VTT/SRT subtitle files to clean timestamped text.

Supports both VTT (WebVTT) and SRT (SubRip) formats. Auto-detects format by file
extension, falling back to content sniffing.

Parses subtitle cues, deduplicates overlapping text, and outputs a readable .txt
file with optional timestamps.

Usage:
    python subtitle_convert.py transcript.en.vtt
    python subtitle_convert.py transcript.en.srt -o output.txt
    python subtitle_convert.py transcript.en.vtt --no-timestamps
"""

import argparse
import re
import sys
from enum import Enum, auto
from pathlib import Path


class SubFormat(Enum):
    VTT = auto()
    SRT = auto()


# VTT timestamps: HH:MM:SS.mmm --> HH:MM:SS.mmm
# SRT timestamps: HH:MM:SS,mmm --> HH:MM:SS,mmm
TIMESTAMP_RE = re.compile(
    r"(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3})"
)

VTT_HEADER_PATTERNS = ("WEBVTT", "Kind:", "Language:")


def detect_format(file_path: Path) -> SubFormat:
    """Detect subtitle format: extension first, then content sniffing."""
    ext = file_path.suffix.lower()
    if ext == ".srt":
        return SubFormat.SRT
    if ext == ".vtt":
        return SubFormat.VTT

    # Fallback: sniff file content
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        head = f.read(512)
    if head.lstrip().startswith("WEBVTT"):
        return SubFormat.VTT
    # SRT starts with a number (cue index)
    if re.match(r"^\s*\d+\s*$", head.split("\n")[0]):
        return SubFormat.SRT
    # Default to VTT
    return SubFormat.VTT


def time_to_display(ts: str) -> str:
    """Convert SRT/VTT timestamp (HH:MM:SS,mmm or HH:MM:SS.mmm) to display format (HH:MM:SS)."""
    parts = ts.strip().split(":")
    h, m = parts[0], parts[1]
    # Split on either comma (SRT) or dot (VTT), keep only seconds
    s = re.split(r"[.,]", parts[2])[0]
    return f"{h}:{m}:{s}"


def is_blank_or_index(line: str, fmt: SubFormat) -> bool:
    """Check if a line is a blank line, or (for SRT) a cue index."""
    stripped = line.strip()
    if not stripped:
        return True
    if fmt == SubFormat.SRT and stripped.isdigit():
        return True
    return False


def is_header_line(line: str, fmt: SubFormat) -> bool:
    """Check if a line is a format-specific header."""
    if fmt == SubFormat.VTT:
        return any(line.startswith(p) for p in VTT_HEADER_PATTERNS)
    return False


def parse_cues(content: str, fmt: SubFormat) -> list[tuple[str, str]]:
    """Parse subtitle content into a list of (timestamp_line, text) tuples.

    Handles both VTT and SRT formats. Deduplicates by text content.
    """
    blocks = re.split(r"\n\s*\n", content.strip())
    cues: list[tuple[str, str]] = []
    seen: set[str] = set()

    for block in blocks:
        lines = block.strip().split("\n")
        if not lines:
            continue

        # Skip header blocks
        if is_header_line(lines[0], fmt):
            continue

        ts_line = None
        text_parts: list[str] = []

        for line in lines:
            # Skip blank/cue-index lines
            if is_blank_or_index(line, fmt):
                continue

            # Check for timestamp line
            m = TIMESTAMP_RE.search(line)
            if m:
                ts_line = line
                continue

            # Text line — strip HTML tags and decode entities
            clean = re.sub(r"<[^>]*>", "", line).strip()
            clean = clean.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
            if clean:
                text_parts.append(clean)

        if not ts_line or not text_parts:
            continue

        text = " ".join(text_parts)
        if text in seen:
            continue
        seen.add(text)
        cues.append((ts_line, text))

    return cues


def convert_to_txt(
    input_path: Path,
    output_path: Path | None = None,
    include_timestamps: bool = True,
) -> int:
    """Convert a subtitle file (VTT or SRT) to timestamped plain text.

    If output_path is None, writes to stdout.
    Returns the number of unique cues written.
    """
    fmt = detect_format(input_path)

    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    cues = parse_cues(content, fmt)

    if output_path is None:
        out = sys.stdout
    else:
        out = open(output_path, "w", encoding="utf-8")

    try:
        for i, (ts_line, text) in enumerate(cues):
            if i > 0:
                out.write("\n")

            if include_timestamps:
                m = TIMESTAMP_RE.search(ts_line)
                if m:
                    start = time_to_display(m.group(1))
                    end = time_to_display(m.group(2))
                    out.write("-------------------\n")
                    out.write(f"{start} - {end}\n")
            out.write(text + "\n")
    finally:
        if output_path is not None:
            out.close()

    return len(cues)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert VTT/SRT subtitle files to clean timestamped plain text.",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to the subtitle file (.vtt or .srt)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output .txt file path (default: print to stdout)",
    )
    parser.add_argument(
        "--no-timestamps",
        action="store_true",
        default=False,
        help="Omit timestamps, output plain text only",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else None
    fmt = detect_format(input_path)
    fmt_name = "VTT" if fmt == SubFormat.VTT else "SRT"
    include_timestamps = not args.no_timestamps

    count = convert_to_txt(input_path, output_path, include_timestamps)

    mode = "with timestamps" if include_timestamps else "plain text"
    if output_path:
        print(f"✓ Converted {count} unique cues from {fmt_name} ({mode})")
        print(f"  Input:  {input_path}")
        print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
