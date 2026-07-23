#!/usr/bin/env python3
"""
Whisper Transcription -- Audio/Video to Text using faster-whisper.

faster-whisper uses CTranslate2 instead of PyTorch, giving 4x faster inference
and a much smaller install footprint (~100 MB vs ~3 GB for openai-whisper).

Features (always on):
  - VAD filtering          -- skip silence automatically via faster-whisper's built-in VAD
  - Audio normalization    -- ffmpeg -> 16kHz mono PCM16 for consistent input

Features (opt-in via flags):
  - Translation          (--translate)     -- translate speech to English/other languages
  - Word-level timestamps  (--word-timestamps)
  - Initial prompt         (--prompt)        -- inject names/acronyms for better accuracy
  - Speaker diarization    (--diarize)       -- requires pyannote.audio + HF_TOKEN

Usage:
    python whisper.py transcribe audio.mp3 --model medium
    python whisper.py transcribe audio.mp3 --diarize --num-speakers 2
    python whisper.py transcribe foreign.mp3 --translate --translate-to en
    python whisper.py transcribe podcast.mp3 --word-timestamps --format json
    python whisper.py batch ./recordings/ --format srt
"""

import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Optional

import click

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ===========================================================================
# Dependency checks
# ===========================================================================

def check_whisper():
    try:
        __import__("faster_whisper")
        return True
    except ImportError:
        return False


def check_ffmpeg():
    return shutil.which("ffmpeg") is not None


def check_diarization_deps():
    missing = []
    for mod in ("torch", "torchaudio", "pyannote.audio", "numpy", "pandas"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return missing


# ===========================================================================
# Device detection
# ===========================================================================

def get_device():
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda", "float16"
    except ImportError:
        pass
    return "cpu", "int8"


# ===========================================================================
# Audio normalization (always on)
# ===========================================================================

def normalize_audio(input_path: Path, work_dir: Path) -> Path:
    """Convert input to 16kHz mono PCM16 WAV via ffmpeg.

    Ensures consistent input format for Whisper regardless of source format.
    Returns path to the normalized WAV file and logs the duration.
    """
    wav_path = work_dir / "audio.wav"
    logger.info("Normalizing audio: 16kHz mono PCM16")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(input_path),
         "-map", "0:a:0", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
         str(wav_path)],
        check=True, capture_output=True,
    )
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(wav_path)],
        check=True, capture_output=True, text=True,
    )
    duration = float(result.stdout.strip())
    logger.info("Normalized: %.1fs, %s", duration, wav_path)
    return wav_path


# ===========================================================================
# Model loading
# ===========================================================================

MODEL_CHOICES = [
    "tiny", "tiny.en", "base", "base.en", "small", "small.en",
    "medium", "medium.en", "large-v3", "large-v3-turbo",
]


def get_model(model_name: str):
    """Load faster-whisper model."""
    from faster_whisper import WhisperModel

    device, compute_type = get_device()
    logger.info("Loading model '%s' (%s on %s)", model_name, compute_type, device)
    return WhisperModel(model_name, device=device, compute_type=compute_type)


# ===========================================================================
# Transcription (VAD always on; word_timestamps & prompt opt-in)
# ===========================================================================

def transcribe_file(model, file_path: str, *,
                    language: Optional[str] = None,
                    prompt: Optional[str] = None,
                    word_timestamps: bool = False,
                    task: str = "transcribe",
                    ) -> dict:
    """Run transcription and return a result dict.

    Returns:
        {text, segments, language}
        Each segment: {start, end, text, [words]}
        words (if word_timestamps=True): [{start, end, word, probability}]
    """
    from faster_whisper.vad import VadOptions

    options = {
        "language": language,
        "beam_size": 5,
        "vad_filter": True,
        "vad_parameters": VadOptions(
            max_speech_duration_s=model.feature_extractor.chunk_length,
            min_speech_duration_ms=100,
            speech_pad_ms=100,
            threshold=0.25,
            neg_threshold=0.2,
        ),
        "word_timestamps": word_timestamps,
        "initial_prompt": prompt,
        "task": task,
    }

    segments_iter, info = model.transcribe(file_path, **options)

    segments = []
    full_text_parts = []

    for seg in segments_iter:
        sd = {"start": seg.start, "end": seg.end, "text": seg.text}
        if word_timestamps and seg.words is not None:
            sd["words"] = [
                {"start": w.start, "end": w.end,
                 "word": w.word, "probability": w.probability}
                for w in seg.words
            ]
        segments.append(sd)
        full_text_parts.append(seg.text)

    return {
        "text": "".join(full_text_parts),
        "segments": segments,
        "language": info.language,
    }


# ===========================================================================
# Speaker diarization (opt-in via --diarize)
# ===========================================================================

def run_diarization(audio_wav: str, num_speakers: Optional[int] = None,
                    model_path: Optional[str] = None) -> list[dict]:
    """Run speaker diarization using pyannote.audio.

    Requires HF_TOKEN env var for HuggingFace model access.
    Returns list of {start, end, speaker} dicts.
    """
    import torch
    import torchaudio
    from pyannote.audio import Pipeline

    if model_path is None:
        model_path = "pyannote/speaker-diarization-3.1"

    token = os.environ.get("HF_TOKEN")
    logger.info("Loading diarization model: %s", model_path)
    pipeline = Pipeline.from_pretrained(model_path, use_auth_token=token)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipeline.to(device)

    waveform, sample_rate = torchaudio.load(audio_wav)
    diarization = pipeline(
        {"waveform": waveform, "sample_rate": sample_rate},
        num_speakers=num_speakers,
    )

    turns = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        turns.append({"start": turn.start, "end": turn.end, "speaker": speaker})

    logger.info("Diarization: %d turns, %d speakers",
                len(turns), len({t["speaker"] for t in turns}))
    return turns


def assign_speakers_to_segments(segments: list[dict],
                                diarization_turns: list[dict]) -> list[dict]:
    """Cross-reference each segment (and each word) with diarization turns.

    Each segment gets a 'speaker' field set to the dominant speaker
    during its time window.
    """
    import numpy as np
    import pandas as pd

    diarize_df = pd.DataFrame(diarization_turns)
    result = []

    for seg in segments:
        diarize_df["intersection"] = (
            np.minimum(diarize_df["end"], seg["end"])
            - np.maximum(diarize_df["start"], seg["start"])
        )
        overlap = diarize_df[diarize_df["intersection"] > 0]

        speaker = "UNKNOWN"
        if len(overlap) > 0:
            speaker = (
                overlap.groupby("speaker")["intersection"]
                .sum().sort_values(ascending=False).index[0]
            )

        words_with_speaker = []
        for w in seg.get("words", []):
            diarize_df["intersection"] = (
                np.minimum(diarize_df["end"], w["end"])
                - np.maximum(diarize_df["start"], w["start"])
            )
            w_overlap = diarize_df[diarize_df["intersection"] > 0]
            w_speaker = speaker
            if len(w_overlap) > 0:
                w_speaker = (
                    w_overlap.groupby("speaker")["intersection"]
                    .sum().sort_values(ascending=False).index[0]
                )
            w["speaker"] = w_speaker
            words_with_speaker.append(w)

        result.append({**seg, "speaker": speaker, "words": words_with_speaker})

    return result


def group_consecutive_speakers(segments: list[dict]) -> list[dict]:
    """Merge consecutive segments from the same speaker.

    Merges when: same speaker, gap <= 1.0s, current group < 30s,
    and no sentence-ending punctuation at the boundary.
    """
    if not segments:
        return segments

    sentence_end = re.compile(r"[.!?]+$")
    grouped = []
    current = segments[0].copy()

    for seg in segments[1:]:
        gap = seg["start"] - current["end"]
        duration = current["end"] - current["start"]
        can_combine = (
            seg.get("speaker") == current.get("speaker")
            and gap <= 1.0
            and duration < 30.0
            and not sentence_end.search(current["text"].strip()[-1:])
        )
        if can_combine:
            current["end"] = seg["end"]
            current["text"] += " " + seg["text"]
            if "words" in current and "words" in seg:
                current["words"].extend(seg["words"])
            continue

        grouped.append(current)
        current = seg.copy()

    grouped.append(current)

    for seg in grouped:
        seg["text"] = re.sub(r"\s+", " ", seg["text"]).strip()
        seg["text"] = re.sub(r"\s+([.,!?])", r"\1", seg["text"])
        seg["duration"] = seg["end"] - seg["start"]

    return grouped


# ===========================================================================
# Timestamp formatting
# ===========================================================================

def format_timestamp(seconds: float) -> str:
    """SRT timestamp: HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def format_vtt_timestamp(seconds: float) -> str:
    """VTT timestamp: HH:MM:SS.mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


# ===========================================================================
# Output writers
# ===========================================================================

def write_txt(result: dict, output_path: Path, include_timestamps: bool = False):
    with open(output_path, "w", encoding="utf-8") as f:
        has_speakers = any(seg.get("speaker") for seg in result["segments"])
        for seg in result["segments"]:
            parts = []
            if include_timestamps:
                parts.append(f"[{format_timestamp(seg['start']).split(',')[0]}]")
            if has_speakers:
                parts.append(f"[{seg.get('speaker', 'UNKNOWN')}]")
            parts.append(seg["text"].strip())
            f.write(" ".join(parts) + "\n")


def write_srt(segments: list, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            speaker = f"[{seg['speaker']}] " if seg.get("speaker") else ""
            f.write(f"{i}\n{start} --> {end}\n{speaker}{seg['text'].strip()}\n\n")


def write_vtt(segments: list, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, 1):
            start = format_vtt_timestamp(seg["start"])
            end = format_vtt_timestamp(seg["end"])
            speaker = f"[{seg['speaker']}] " if seg.get("speaker") else ""
            f.write(f"{i}\n{start} --> {end}\n{speaker}{seg['text'].strip()}\n\n")


def write_output(result: dict, output_path: Path, output_format: str,
                 include_timestamps: bool = False):
    if output_format == "txt":
        write_txt(result, output_path, include_timestamps)
    elif output_format == "srt":
        write_srt(result["segments"], output_path)
    elif output_format == "vtt":
        write_vtt(result["segments"], output_path)
    elif output_format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    elif output_format == "tsv":
        with open(output_path, "w", encoding="utf-8") as f:
            has_speakers = any(seg.get("speaker") for seg in result["segments"])
            headers = "start\tend"
            if has_speakers:
                headers += "\tspeaker"
            headers += "\ttext\n"
            f.write(headers)
            for seg in result["segments"]:
                row = f"{seg['start']:.2f}\t{seg['end']:.2f}"
                if has_speakers:
                    row += f"\t{seg.get('speaker', '')}"
                row += f"\t{seg['text'].strip()}\n"
                f.write(row)


# ===========================================================================
# Core pipeline
# ===========================================================================

def run_pipeline(input_path: Path, *, model_name: str, output_format: str,
                 output_path: Optional[Path], language: Optional[str],
                 prompt: Optional[str], word_timestamps: bool,
                 include_timestamps: bool, diarize: bool,
                 num_speakers: Optional[int], diarization_model: str,
                 task: str = "transcribe"):
    """End-to-end: normalize -> transcribe -> [diarize] -> write."""

    if not check_ffmpeg():
        click.echo("Error: ffmpeg not found.")
        click.echo("  macOS:  brew install ffmpeg")
        click.echo("  Ubuntu: sudo apt install ffmpeg")
        raise SystemExit(1)

    t0 = time.time()

    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)

        click.echo("  [1/3] Normalizing audio (16kHz mono)...")
        wav_path = normalize_audio(input_path, work_dir)

        model = get_model(model_name)

        click.echo("  [2/3] Transcribing...")
        result = transcribe_file(
            model, str(wav_path),
            language=language, prompt=prompt,
            word_timestamps=word_timestamps, task=task,
        )

        if diarize:
            missing = check_diarization_deps()
            if missing:
                click.echo(f"Error: diarization requires: {', '.join(missing)}")
                click.echo("Run: pip install torch torchaudio pyannote-audio numpy pandas")
                raise SystemExit(1)
            if not os.environ.get("HF_TOKEN"):
                click.echo("Warning: HF_TOKEN not set -- diarization may fail.")
                click.echo("Get a token at https://hf.co/settings/tokens")

            click.echo("  [3/3] Speaker diarization...")
            turns = run_diarization(str(wav_path), num_speakers, diarization_model)
            result["segments"] = assign_speakers_to_segments(result["segments"], turns)
            result["num_speakers"] = len({t["speaker"] for t in turns})
            click.echo("  Grouping consecutive same-speaker segments...")
            result["segments"] = group_consecutive_speakers(result["segments"])
        else:
            click.echo("  [3/3] Done.")

    if output_path is None:
        output_path = input_path.with_suffix(f".{output_format}")
    else:
        output_path = Path(output_path)

    click.echo(f"  Writing: {output_path.name}")
    write_output(result, output_path, output_format, include_timestamps)

    elapsed = time.time() - t0
    click.echo(f"\n  {'-' * 40}")
    click.echo(f"  [OK] Done in {elapsed:.1f}s")
    click.echo(f"  Output:    {output_path}")
    click.echo(f"  Language:  {result.get('language', 'unknown')}")
    if result.get("num_speakers"):
        click.echo(f"  Speakers:  {result['num_speakers']}")
    click.echo(f"  Segments:  {len(result['segments'])}")

    preview = result["text"][:200].strip()
    click.echo(f"\n  Preview:\n  {preview}...")


# ===========================================================================
# CLI
# ===========================================================================

FORMAT_CHOICES = ["txt", "srt", "vtt", "json", "tsv"]


@click.group()
def cli():
    """Whisper Transcription -- Audio/Video to Text (faster-whisper).

    Always on: VAD filtering + audio normalization (16kHz mono).
    Optional:  --word-timestamps, --prompt, --diarize.

    Install:
      pip install faster-whisper click                 # base
      pip install torch torchaudio pyannote-audio \\   # for --diarize
                numpy pandas
    """
    if not check_whisper():
        click.echo("Error: faster-whisper not installed.")
        click.echo("Run: pip install faster-whisper")
        raise SystemExit(1)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--model", "-m", default="small", type=click.Choice(MODEL_CHOICES),
              help="Whisper model size (default: small)")
@click.option("--format", "-f", "output_format", default="txt",
              type=click.Choice(FORMAT_CHOICES), help="Output format")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--language", "-l", help="Language code (auto-detect if omitted)")
@click.option("--prompt", help="Initial prompt -- names, acronyms for better accuracy")
@click.option("--word-timestamps", is_flag=True,
              help="Include word-level timestamps in output")
@click.option("--timestamps", "include_timestamps", is_flag=True,
              help="Include segment timestamps in txt output")
@click.option("--diarize", is_flag=True,
              help="Enable speaker diarization (requires pyannote.audio + HF_TOKEN)")
@click.option("--num-speakers", type=int, default=None,
              help="Number of speakers (auto-detect if omitted)")
@click.option("--diarization-model", default="pyannote/speaker-diarization-3.1",
              help="Diarization model on HuggingFace")
@click.option("--translate", is_flag=True,
              help="Translate speech to English (task=translate)")
@click.option("--translate-to", default="en",
              help="Target language for translation (default: en)")
def transcribe(file: str, model: str, output_format: str, output: Optional[str],
               language: Optional[str], prompt: Optional[str],
               word_timestamps: bool, include_timestamps: bool,
               diarize: bool, num_speakers: Optional[int],
               diarization_model: str,
               translate: bool, translate_to: str):
    """Transcribe an audio/video file to text."""
    input_path = Path(file)
    task = "translate" if translate else "transcribe"

    click.echo(f"\n  Whisper Transcription (faster-whisper)")
    click.echo(f"  {'=' * 40}")
    click.echo(f"  Input:  {input_path.name}")
    click.echo(f"  Model:  {model}")
    click.echo(f"  Format: {output_format}")
    if translate:
        click.echo(f"  Mode:   translate -> {translate_to}")
    if prompt:
        click.echo(f"  Prompt: {prompt[:60]}...")
    if word_timestamps:
        click.echo(f"  Word timestamps: on")
    if diarize:
        click.echo(f"  Diarization: on")

    run_pipeline(
        input_path,
        model_name=model, output_format=output_format, output_path=output,
        language=language, prompt=prompt, word_timestamps=word_timestamps,
        include_timestamps=include_timestamps, diarize=diarize,
        num_speakers=num_speakers, diarization_model=diarization_model,
        task=task,
    )


@cli.command()
@click.argument("folder", type=click.Path(exists=True))
@click.option("--model", "-m", default="small", type=click.Choice(MODEL_CHOICES),
              help="Whisper model size (default: small)")
@click.option("--format", "-f", "output_format", default="txt",
              type=click.Choice(FORMAT_CHOICES), help="Output format")
@click.option("--output", "-o", type=click.Path(), help="Output directory")
@click.option("--language", "-l", help="Language code (auto-detect if omitted)")
@click.option("--prompt", help="Initial prompt -- names, acronyms for better accuracy")
@click.option("--word-timestamps", is_flag=True,
              help="Include word-level timestamps in output")
@click.option("--timestamps", "include_timestamps", is_flag=True,
              help="Include segment timestamps in txt output")
@click.option("--diarize", is_flag=True,
              help="Enable speaker diarization (requires pyannote.audio + HF_TOKEN)")
@click.option("--num-speakers", type=int, default=None,
              help="Number of speakers (auto-detect if omitted)")
@click.option("--diarization-model", default="pyannote/speaker-diarization-3.1",
              help="Diarization model on HuggingFace")
def batch(folder: str, model: str, output_format: str, output: Optional[str],
          language: Optional[str], prompt: Optional[str],
          word_timestamps: bool, include_timestamps: bool,
          diarize: bool, num_speakers: Optional[int],
          diarization_model: str):
    """Batch transcribe all audio/video files in a folder."""
    input_dir = Path(folder)
    output_dir = Path(output) if output else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    extensions = {".mp3", ".wav", ".m4a", ".mp4", ".mkv", ".webm", ".ogg", ".flac"}
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in extensions]

    if not files:
        click.echo(f"No audio/video files found in {folder}")
        return

    click.echo(f"\n  Batch Transcription -- {len(files)} files")
    click.echo(f"  {'=' * 40}")

    for i, fp in enumerate(files, 1):
        click.echo(f"\n-- [{i}/{len(files)}] {fp.name} --")
        out_path = output_dir / fp.with_suffix(f".{output_format}").name
        try:
            run_pipeline(
                fp,
                model_name=model, output_format=output_format, output_path=out_path,
                language=language, prompt=prompt, word_timestamps=word_timestamps,
                include_timestamps=include_timestamps, diarize=diarize,
                num_speakers=num_speakers, diarization_model=diarization_model,
            )
        except Exception as e:
            logger.error("Failed: %s -- %s", fp.name, e)
            continue

    click.echo(f"\n  [OK] Batch complete: {len(files)} files")


if __name__ == "__main__":
    cli()
