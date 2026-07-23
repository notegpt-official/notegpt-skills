# notegpt-skills

AI Agent Skills Collection — covering browser automation, audio/video transcription, and complete SEO workflows.

## Directory Structure

```
skills/
├── browser-automation/       # Browser Automation (Anti-Detection)
├── transcript/               # Audio/Video Transcription
└── seo/                      # SEO Automation Pipeline
    ├── seo-keyword-difficulty/   # Step 0: Keyword Difficulty Analysis
    ├── page-seo-generator/       # Step 1: English SEO Page Generation
    ├── page-seo-generator-i18n/  # Step 1: Multilingual SEO Page Generation
    ├── seo-image-generator/      # Step 2: SEO Image Generation
    └── page-seo-checker/         # Final Step: SEO Compliance Check
```

---

## Skill Overview

### 1. Browser Automation

Anti-detection browser automation powered by **CloakBrowser** (a pre-patched Chromium).

| Feature | Description |
|---------|-------------|
| **Anti-Detection** | C++ source-level fingerprint patching, bypassing reCAPTCHA v3, Cloudflare Turnstile, FingerprintJS |
| **Dual Language** | JavaScript (Playwright/Puppeteer) and Python APIs |
| **Human-Like** | Bézier curve mouse paths, per-character typing delays, natural scroll physics |
| **GeoIP** | Auto-matching timezone and locale based on proxy IP |
| **Persistence** | Persistent user profiles to maintain login sessions and cookies |

**Trigger words**: scrape XX page, automate filling XX, bypass captcha for XX

---

### 2. Transcript — Audio/Video to Text

A universal audio/video-to-text conversion tool.

| Source | Method | Output Formats |
|--------|--------|----------------|
| **YouTube URL** | yt-dlp subtitle extraction (manual captions → auto captions → Whisper fallback) | Plain text, SRT/VTT, JSON, timestamped segments |
| **Audio/Video Files** | faster-whisper (CTranslate2 accelerated, 4× inference speed) | Same as above |

**Trigger words**: transcribe, transcript, download subtitles, extract text from video, convert audio to text

---

### 3. SEO Automation Pipeline

#### Step 0: [seo-keyword-difficulty](skills/seo/seo-keyword-difficulty/SKILL.md) — Keyword Difficulty Analysis

Evaluate whether a keyword is worth pursuing **before any content production**.

- Retrieve real KD scores, search volume, and Top-10 competitor data via `seo-web-cafe` MCP
- Supports **Mode A** (single keyword deep analysis) and **Mode B** (multi-keyword comparison)
- Outputs a decision report: 🟢 Go / 🟡 Proceed with Caution / 🔴 Find Another Keyword
- Includes feasibility scoring formula: `(Volume/1000) × (1-KD/100) × TrendMultiplier × IntentMultiplier`

#### Step 1: [page-seo-generator](skills/seo/page-seo-generator/SKILL.md) — English SEO Page Generator

Generate a complete **11-column SEO landing page** from a single keyword input.

**4-Phase Workflow**:
1. **Keyword Research** — Semantic analysis, competitor intelligence, user persona, KD analysis
2. **Competitor TDK Analysis** — Scrape real competitor Titles & Descriptions via Playwright
3. **TDK Skeleton** — Generate 3 title options, character count verified with Python `len()`
4. **Full 11-Column Content** — Complete page content from Hero section to Schema markup

#### Step 1 (Multilingual): [page-seo-generator-i18n](skills/seo/page-seo-generator-i18n/SKILL.md) — Multilingual SEO Page Generator

Native-language SEO content generation for Japanese (ja) and Chinese (zh) markets.

- **Not machine translation**: Independently optimizes target-language expression while maintaining information consistency with the English source page
- Japanese: です・ます調, conclusion-first, bullet-point layout
- Chinese: Concise and direct, short sentences, pain-point focused

#### Step 2: [seo-image-generator](skills/seo/seo-image-generator/SKILL.md) — SEO Image Generator

Generate **4 types of visual assets** for SEO pages:

| Type | Ratio | Method | Brand Elements |
|------|-------|--------|----------------|
| Banner | 16:9 | Image-to-image (logo required) | ✅ Logo + URL |
| Product Intro | 1:1 | Text-to-image | ❌ No brand elements |
| Why Choose Us | 1:1 | Text-to-image | ❌ No brand elements |
| Pain Point Scenario | 1:1 | Text-to-image | ❌ No brand elements |

#### Final Step: [page-seo-checker](skills/seo/page-seo-checker/SKILL.md) — 12-Point SEO Compliance Check

A pre-publish **quality gate** performing a 12-point automated check on published pages:

| # | Check Item | Max Score |
|---|------------|-----------|
| 1 | Title Tag | 10 |
| 2 | Meta Description | 8 |
| 3 | Canonical Tag | 5 |
| 4 | H-Tag Structure | 8 |
| 5 | Body Content Word Count | 10 |
| 6 | User Review Authenticity | 5 |
| 7 | FAQ Structure & Schema | 8 |
| 8 | Image ALT Tags | 5 |
| 9 | Internal Links | 5 |
| 10 | Schema Structured Data | 10 |
| 11 | Hreflang Tags | 5 |
| 12 | Brand Name Count & Zero Articles | 5 |

**Scoring**: ≥80% 🟢 Ready to Publish / 60-79% 🟡 Fix Before Publishing / <60% 🔴 Not Ready

---

## SEO Workflow Overview

```
Keyword Input
    │
    ▼
┌─────────────────────────┐
│  seo-keyword-difficulty │  ← Step 0: Is this keyword viable?
└───────────┬─────────────┘
            │ 🟢/🟡 Passed
            ▼
┌─────────────────────────┐
│  page-seo-generator     │  ← Step 1: Generate English SEO page
│  page-seo-generator-i18n│  ← Step 1 (optional): Generate multilingual pages
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  seo-image-generator    │  ← Step 2: Generate visual assets
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  page-seo-checker       │  ← Final Step: Pre-publish quality check
└─────────────────────────┘
```

---

## Usage

These skills are designed to be used within an AI Agent environment that supports the Skill mechanism. Each skill's `SKILL.md` file defines complete trigger rules and workflow instructions.

Use this repository as your project directory, and the Agent will automatically discover and load all skills under the `skills/` directory.
