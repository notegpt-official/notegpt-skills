# Whisper Transcription — Reference (via faster-whisper)

> faster-whisper uses CTranslate2 instead of PyTorch for the Whisper engine itself, giving 4x faster inference. Uses PyTorch only for optional speaker diarization.

## When to Use

- **Podcast repurposing** — Convert episodes to blog posts, show notes, social snippets
- **Video subtitles** — Generate SRT/VTT files for YouTube, social media
- **Interview extraction** — Pull quotes and insights from recorded calls
- **Content audit** — Make audio/video libraries searchable
- **Translation** — Transcribe and translate foreign language content

## Dependencies

```bash
pip install -r requirements.txt
# Also requires ffmpeg installed on system
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

## Commands

### Transcribe Single File

```bash
python scripts/whisper.py transcribe audio.mp3 --model small
python scripts/whisper.py transcribe video.mp4 --format srt --output subtitles.srt
```

### Transcribe with Translation

```bash
python scripts/whisper.py transcribe foreign-audio.mp3 --translate
python scripts/whisper.py transcribe foreign-audio.mp3 --translate --translate-to fr
```

### Transcribe with Word-level Timestamps

```bash
python scripts/whisper.py transcribe podcast.mp3 --word-timestamps --format json
```

### Transcribe with Speaker Diarization

```bash
python scripts/whisper.py transcribe interview.mp3 --diarize --num-speakers 2
```

### Batch Transcription

```bash
python scripts/whisper.py batch ./recordings/ --format txt --output ./transcripts/
```

## Common Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--model` / `-m` | Model size | `small` |
| `--format` / `-f` | Output format (`txt`/`srt`/`vtt`/`json`/`tsv`) | `txt` |
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

## Examples

### Example 1: Podcast to Blog Post
```bash
python scripts/whisper.py transcribe episode-42.mp3 --model medium

# Output: episode-42.txt (full transcript)
# Processing time: ~1 min for 1 hour audio with GPU
```

### Example 2: YouTube Subtitles
```bash
python scripts/whisper.py transcribe marketing-video.mp4 --format srt

# Output: marketing-video.srt — upload directly to YouTube/Vimeo
```

### Example 3: Interview with Diarization
```bash
HF_TOKEN=hf_xxx python scripts/whisper.py transcribe interview.mp3 --diarize --num-speakers 2 --format srt

# Output: interview.srt with [SPEAKER_00] / [SPEAKER_01] labels
```

### Example 4: Batch Process Interview Library
```bash
python scripts/whisper.py batch ./customer-interviews/ --model small --format txt

# Output: ./customer-interviews/*.txt (one per audio file)
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

| Format | Extension | Use Case |
|--------|-----------|----------|
| `txt` | .txt | Reading, blog posts, analysis |
| `srt` | .srt | Video subtitles (YouTube) |
| `vtt` | .vtt | Web video subtitles |
| `json` | .json | Programmatic access, timestamps |
| `tsv` | .tsv | Spreadsheet analysis |

## Pipeline (Always On)

1. **Audio normalization** — ffmpeg converts input to 16kHz mono PCM16 WAV regardless of source format
2. **VAD filtering** — faster-whisper's built-in VAD skips silence automatically

## Performance Tips

1. **GPU acceleration** — Auto-detects CUDA (float16) or CPU (int8 quantized). No config needed.
2. **4x faster than openai-whisper** — CTranslate2 engine with int8 CPU / float16 GPU inference
3. **Language detection** — Automatic, or specify with `--language`
