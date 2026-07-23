#!/usr/bin/env python3
"""
Subtitle format converter — Convert between VTT, SRT, JSON, TSV, and TXT formats.

Primary workflow:
  1. Whisper generates a VTT file (the canonical format)
  2. This script converts VTT to any other needed format

Supports:
  - VTT → SRT    (YouTube upload, video players)
  - VTT → JSON   (programmatic access, timestamps)
  - VTT → TSV    (spreadsheet analysis)
  - VTT → TXT    (reading, blog posts, with optional timestamps)
  - SRT → TXT    (clean timestamped text from existing SRT files)

Usage:
    python subtitle_convert.py transcript.en.vtt -f srt -o transcript.srt
    python subtitle_convert.py transcript.en.vtt -f json -o transcript.json
    python subtitle_convert.py transcript.en.vtt -f tsv -o transcript.tsv
    python subtitle_convert.py transcript.en.vtt -o transcript.txt        # default: txt
    python subtitle_convert.py transcript.en.vtt --no-timestamps           # plain text
    python subtitle_convert.py transcript.en.srt -o transcript.txt         # SRT → TXT
"""

import argparse
import json
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

OUTPUT_FORMATS = ["txt", "srt", "json", "tsv"]


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


def vtt_to_srt_timestamp(ts: str) -> str:
    """Convert VTT timestamp (HH:MM:SS.mmm) to SRT timestamp (HH:MM:SS,mmm)."""
    return ts.replace(".", ",", 2)  # Replace only the last dot (before milliseconds)


def srt_to_vtt_timestamp(ts: str) -> str:
    """Convert SRT timestamp (HH:MM:SS,mmm) to VTT timestamp (HH:MM:SS.mmm)."""
    return ts.replace(",", ".", 2)  # Replace only the last comma (before milliseconds)


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


def parse_cues(content: str, fmt: SubFormat) -> list[dict]:
    """Parse subtitle content into a list of cue dicts.

    Each cue: {index, start, end, start_display, end_display, text}
    Handles both VTT and SRT formats. Deduplicates by text content.
    """
    blocks = re.split(r"\n\s*\n", content.strip())
    cues: list[dict] = []
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

        m = TIMESTAMP_RE.search(ts_line)
        cues.append({
            "start_raw": m.group(1),
            "end_raw": m.group(2),
            "start_display": time_to_display(m.group(1)),
            "end_display": time_to_display(m.group(2)),
            "text": text,
        })

    return cues


# ===========================================================================
# Format writers
# ===========================================================================

def write_txt(cues: list[dict], output_path: Path | None,
              include_timestamps: bool) -> int:
    """Write cues as plain text with optional timestamps."""
    if output_path is None:
        out = sys.stdout
    else:
        out = open(output_path, "w", encoding="utf-8")

    try:
        for i, cue in enumerate(cues):
            if i > 0:
                out.write("\n")
            if include_timestamps:
                out.write(f"{cue['start_display']} - {cue['end_display']}\n")
            out.write(cue["text"] + "\n")
    finally:
        if output_path is not None:
            out.close()

    return len(cues)


def write_srt(cues: list[dict], output_path: Path) -> int:
    """Write cues as SRT (SubRip) format."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, cue in enumerate(cues, 1):
            start = vtt_to_srt_timestamp(cue["start_raw"])
            end = vtt_to_srt_timestamp(cue["end_raw"])
            f.write(f"{i}\n{start} --> {end}\n{cue['text']}\n\n")
    return len(cues)


def write_json(cues: list[dict], output_path: Path) -> int:
    """Write cues as JSON array."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cues, f, indent=2, ensure_ascii=False)
    return len(cues)


def write_tsv(cues: list[dict], output_path: Path) -> int:
    """Write cues as TSV (tab-separated values)."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("start\tend\ttext\n")
        for cue in cues:
            f.write(f"{cue['start_raw']}\t{cue['end_raw']}\t{cue['text']}\n")
    return len(cues)


# ===========================================================================
# Main conversion entry point
# ===========================================================================

def convert(
    input_path: Path,
    output_path: Path | None = None,
    output_format: str = "txt",
    include_timestamps: bool = True,
) -> int:
    """Convert a subtitle file between formats.

    If output_path is None, writes to stdout (txt format only).
    Returns the number of unique cues written.
    """
    fmt = detect_format(input_path)

    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    cues = parse_cues(content, fmt)

    if output_format == "txt":
        return write_txt(cues, output_path, include_timestamps)
    elif output_format == "srt":
        if output_path is None:
            output_path = input_path.with_suffix(".srt")
        return write_srt(cues, output_path)
    elif output_format == "json":
        if output_path is None:
            output_path = input_path.with_suffix(".json")
        return write_json(cues, output_path)
    elif output_format == "tsv":
        if output_path is None:
            output_path = input_path.with_suffix(".tsv")
        return write_tsv(cues, output_path)
    else:
        print(f"Error: unknown output format: {output_format}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert subtitle files between VTT, SRT, JSON, TSV, and TXT formats.",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to the subtitle file (.vtt or .srt)",
    )
    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=OUTPUT_FORMATS,
        default="txt",
        help="Output format (default: txt)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file path (auto-generated if omitted; stdout for txt)",
    )
    parser.add_argument(
        "--no-timestamps",
        action="store_true",
        default=False,
        help="Omit timestamps (txt output only)",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else None
    src_fmt = detect_format(input_path)
    src_name = "VTT" if src_fmt == SubFormat.VTT else "SRT"
    include_timestamps = not args.no_timestamps

    count = convert(input_path, output_path, args.format, include_timestamps)

    if output_path:
        mode = "with timestamps" if include_timestamps else "plain text"
        print(f"✓ Converted {count} unique cues: {src_name} → {args.format.upper()} ({mode})")
        print(f"  Input:  {input_path}")
        print(f"  Output: {output_path}")
    elif args.format != "txt":
        out_path = input_path.with_suffix(f".{args.format}")
        print(f"✓ Converted {count} unique cues: {src_name} → {args.format.upper()}")
        print(f"  Input:  {input_path}")
        print(f"  Output: {out_path}")


if __name__ == "__main__":
    main()
