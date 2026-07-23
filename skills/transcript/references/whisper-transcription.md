# Whisper Transcription — Reference (via faster-whisper)

> faster-whisper uses CTranslate2 instead of PyTorch for the Whisper engine itself, giving 4x faster inference. Uses PyTorch only for optional speaker diarization.

## When to Use

- **Podcast repurposing** — Convert episodes to blog posts, show notes, social snippets
- **Video subtitles** — Generate VTT/SRT files for YouTube, social media
- **Interview extraction** — Pull quotes and insights from recorded calls
- **Content audit** — Make audio/video libraries searchable
- **Translation** — Transcribe and translate foreign language content

## Dependencies

```bash
pip install -r scripts/requirements.txt
# Also requires ffmpeg installed on system
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

## Subtitle Format Strategy

Whisper generates **VTT as the canonical output format** — the single source of truth. All other subtitle formats (SRT, JSON, TSV, TXT) are derived by converting the VTT file via `python scripts/subtitle_convert.py`.

**Why VTT?**
- Native web standard (WebVTT) — supported by all browsers
- Millisecond precision timestamps (`.` separator, unlike SRT's `,`)
- Richer cue formatting and metadata support
- Single canonical format → convert to anything else without re-running Whisper

## Commands

### Transcribe Single File (output: VTT)

```bash
python scripts/whisper.py transcribe audio.mp3 --model small
# Output: audio.vtt (VTT format, the canonical output)

python scripts/whisper.py transcribe video.mp4 --output subtitles
# Output: subtitles.vtt
```

### Transcribe with Translation

```bash
python scripts/whisper.py transcribe foreign-audio.mp3 --translate
# Output: foreign-audio.vtt (translated to English)

python scripts/whisper.py transcribe foreign-audio.mp3 --translate --translate-to fr
# Output: foreign-audio.vtt (translated to French)
```

### Transcribe with Word-level Timestamps

```bash
python scripts/whisper.py transcribe podcast.mp3 --word-timestamps --output podcast
# Output: podcast.vtt (word-level timestamps embedded in VTT)
```

### Transcribe with Speaker Diarization

```bash
HF_TOKEN=hf_xxx python scripts/whisper.py transcribe interview.mp3 --diarize --num-speakers 2
# Output: interview.vtt with [SPEAKER_00] / [SPEAKER_01] labels
```

### Convert VTT to Other Formats

```bash
# VTT → SRT (YouTube upload)
python scripts/subtitle_convert.py audio.vtt -f srt -o audio.srt

# VTT → JSON (programmatic access)
python scripts/subtitle_convert.py audio.vtt -f json -o audio.json

# VTT → TSV (spreadsheet analysis)
python scripts/subtitle_convert.py audio.vtt -f tsv -o audio.tsv

# VTT → TXT (reading, blog posts)
python scripts/subtitle_convert.py audio.vtt -o audio.txt

# VTT → plain text (no timestamps)
python scripts/subtitle_convert.py audio.vtt --no-timestamps -o audio.txt
```

### Batch Transcription

```bash
python scripts/whisper.py batch ./recordings/ --output ./transcripts/
# Output: ./transcripts/*.vtt (one VTT per audio file)

# Batch convert all VTT files to SRT
for f in ./transcripts/*.vtt; do
    python scripts/subtitle_convert.py "$f" -f srt -o "${f%.vtt}.srt"
done
```

## Common Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--model` / `-m` | Model size | `small` |
| `--format` / `-f` | Output format (`vtt`/`txt`/`srt`/`json`/`tsv`) | `vtt` |
| `--output` / `-o` | Output file path | auto (input stem + extension) |
| `--language` / `-l` | Language code (auto-detect if omitted) | auto |
| `--translate` | Translate speech to target language | off |
| `--translate-to` | Target language for `--translate` | `en` |
| `--prompt` | Initial prompt — names, acronyms for better accuracy | none |
| `--word-timestamps` | Include per-word timestamps in output | off |
| `--timestamps` | Include segment timestamps in txt output | off |
| `--diarize` | Enable speaker diarization | off |
| `--num-speakers` | Number of speakers (auto-detect if omitted) | auto |
| `--diarization-model` | HuggingFace diarization model | `pyannote/speaker-diarization-3.1` |

> **Speaker diarization** requires `HF_TOKEN` environment variable set to a valid HuggingFace access token.
>
> **Format strategy:** Default is `vtt`. For non-VTT formats, prefer converting the VTT output via `subtitle_convert.py` (avoids re-running Whisper). Use `--format` directly only when you need a one-shot output from Whisper without keeping the VTT source.

### subtitle_convert.py Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-f` / `--format` | Output format (`txt`/`srt`/`json`/`tsv`) | `txt` |
| `-o` / `--output` | Output file path | auto (input stem + new extension) |
| `--no-timestamps` | Omit timestamps (txt output only) | off |

## Examples

### Example 1: Podcast to Blog Post
```bash
# Step 1: Transcribe to VTT
python scripts/whisper.py transcribe episode-42.mp3 --model medium
# Output: episode-42.vtt

# Step 2: Convert VTT to clean text
python scripts/subtitle_convert.py episode-42.vtt -o episode-42.txt

# Processing time: ~1 min for 1 hour audio with GPU
```

### Example 2: YouTube Subtitles
```bash
# Step 1: Transcribe to VTT
python scripts/whisper.py transcribe marketing-video.mp4
# Output: marketing-video.vtt

# Step 2: Convert VTT to SRT for YouTube upload
python scripts/subtitle_convert.py marketing-video.vtt -f srt -o marketing-video.srt
# Output: marketing-video.srt — upload directly to YouTube/Vimeo
```

### Example 3: Interview with Diarization
```bash
# Step 1: Transcribe with speaker labels to VTT
HF_TOKEN=hf_xxx python scripts/whisper.py transcribe interview.mp3 --diarize --num-speakers 2
# Output: interview.vtt with [SPEAKER_00] / [SPEAKER_01] labels

# Step 2: Convert to SRT for video player
python scripts/subtitle_convert.py interview.vtt -f srt -o interview.srt
```

### Example 4: Batch Process Interview Library
```bash
# Step 1: Batch transcribe to VTT
python scripts/whisper.py batch ./customer-interviews/ --model small
# Output: ./customer-interviews/*.vtt (one per audio file)

# Step 2: Batch convert to text for analysis
for f in ./customer-interviews/*.vtt; do
    python scripts/subtitle_convert.py "$f" -o "${f%.vtt}.txt"
done
```

## Model Selection Guide

| Model | Speed | Accuracy | VRAM | Best For |
|-------|-------|----------|------|----------|
| `tiny` / `tiny.en` | Fastest | ~70% | 1 GB | Quick drafts, short clips |
| `base` / `base.en` | Fast | ~80% | 1 GB | Social media clips, YouTube fallback |
| `small` / `small.en` | Medium | ~85% | 2 GB | **Podcasts, interviews (recommended default)** |
| `medium` / `medium.en` | Slow | ~90% | 5 GB | Professional transcripts |
| `large-v3` | Slower | ~95% | 10 GB | Critical accuracy |
| `large-v3-turbo` | Medium | ~94% | 6 GB | Best accuracy/speed trade-off |

- `.en` variants are English-only, slightly faster and more accurate for English content
- All models auto-detect language unless `--language` is specified

**Recommendation:** Use `small` for most tasks, `medium` for client deliverables, `large-v3-turbo` for best quality.

## Output Formats

| Format | Extension | Source | Use Case |
|--------|-----------|--------|----------|
| `vtt` | .vtt | **Whisper (default)** | Web video subtitles, canonical source |
| `srt` | .srt | Whisper or `subtitle_convert.py` (VTT → SRT) | Video subtitles (YouTube, Vimeo) |
| `json` | .json | Whisper or `subtitle_convert.py` (VTT → JSON) | Programmatic access, timestamps |
| `tsv` | .tsv | Whisper or `subtitle_convert.py` (VTT → TSV) | Spreadsheet analysis |
| `txt` | .txt | Whisper or `subtitle_convert.py` (VTT → TXT) | Reading, blog posts, analysis |

> **Recommended workflow:** Whisper outputs `.vtt` (default). Use `subtitle_convert.py` to derive any other format without re-running Whisper.

## Pipeline (Always On)

1. **Audio normalization** — ffmpeg converts input to 16kHz mono PCM16 WAV regardless of source format
2. **VAD filtering** — faster-whisper's built-in VAD skips silence automatically

## Performance Tips

1. **GPU acceleration** — Auto-detects CUDA (float16) or CPU (int8 quantized). No config needed.
2. **4x faster than openai-whisper** — CTranslate2 engine with int8 CPU / float16 GPU inference
3. **Language detection** — Automatic, or specify with `--language`
