# Page SEO Content Rules

## TDK Rules

### Output Format (exact table)
```
| Type | Content (copy directly) |
| --- | --- |
| Title | ... |
| Description | ... |
| Keywords | ... |
| URL | ... |
| Above-the-fold Title (H1) | ... |
| Above-the-fold Description | ... |
| SEO Image Asset | (leave blank) |
| Model Used | (leave blank) |
```

- **Model Used**: always `(leave blank)` — user decides
- NO character count tails in any cell
- NO bold/italic formatting in content cells
- H1 = simple core keyword only (e.g. `AI Fat Filter`), NOT full Title

### Character Limits

| Field | Rule |
|-------|------|
| **Title** | 50-60 characters; English; **core keyword MUST be at the very beginning** — user searches X, first word is X; if core word lacks AI, use `[core word] with AI` or `[core word] – …+AI`; if core word already contains AI (e.g. `AI Clothes Changer`), AI at start is fine; format: `[primary keyword] – [functional long-tail supplement] + CTR word`; **NEVER** put Free/Best/brand word before the core keyword; **NEVER** include brand word in Title; CTR words: Free, No Sign Up, Online — not "Try it now" |
| **Description** | 150-160 characters; include brand word + core keyword + CTA hook |
| **Keywords** | Exactly 5 keywords, all lowercase; core keyword MUST be first |
| **URL** | digits + English lowercase + hyphens; e.g. `/ai-comic-generator` |
| **H1** | Simple core keyword only (e.g. `AI Fat Filter`), NOT the full Title with hooks |
| **Top-of-page description** | <114 characters; must include brand word; 🔴 **MUST be one natural English sentence** — no colons (:), em dashes (—), or other punctuation as connectors. Use "lets you", "helps you", "enables you to" to join ideas into a single flowing sentence |
| **Model Used** | Leave blank `(leave blank)` — user decides the model |

**Character counting tool:** https://uutool.cn/str-count/

**🔴 Character verification is MANDATORY via Python `len()` — never trust eyeball estimates.**

```bash
python3 -c "
print(f'Title: {len(\"<content>\")} chars')
"
```

Run this for every character-critical field before presenting output.

**🔴 Body text character count = visible text only, NOT markdown URLs.** URLs inside `[...](url)` are for browsers, invisible to readers. Strip them before counting:

```bash
python3 -c "
import re
text = '...'
visible = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
print(f'Visible: {len(visible)} chars')
"
```

This applies to Col 3/4/5 body, Col 6/7 intro, Reviews, FAQ — any field that may contain markdown links.

## Multi-Language TDK

| Language | Title Range | Description Range | Special |
|----------|-------------|-------------------|---------|
| English | 50-60 chars | 150-160 chars | Default |
| Japanese | 30-40 chars | 100-110 chars | Use katakana keywords; `No Sign-up` → `登録不要` |

Default to English unless user specifies otherwise.

## Output Language Constraint

🔴 **Output templates and content MUST match the user's input language.** All table headers (`Type`, `Content`, `Section`, `Site`, `Status`, etc.), field labels, and UI-facing text must be output in the same language the user communicates in. Examples:
- User writes in Chinese → output `| 类型 | 内容 |`, `| 站点 | 状态 |`, etc.
- User writes in Japanese → output `| 種類 | 内容 |`, `| サイト | ステータス |`, etc.
- User writes in English → output `| Type | Content |`, `| Site | Status |`, etc.

This rule applies to: TDK table headers, 11-column table headers, competitor analysis labels, failure markers, and all prompt questions directed at the user.

## 11-Column Page Structure

### Column 1: Hero + TDK
- Full-screen H100 visual area
- Output TDK table in this section: Title / Description / Keywords / URL / H1 / Top Description

### Column 2: H1 + Description + Button + Image
- Left-right layout: text left, image right
- Image: 1200×630 (social media size)
- H1 = Title

### Column 3: Product Introduction ("What Is ...?")
- H2: include **product noun** (e.g. "What Is AI Photo Glare Remover?")
- Body: 200-300 characters
- Embed core keyword (zero article)

### Column 4: Recommendation ("Why Choose ...?")
- H2: include core keyword
- Body: 200-300 characters

### Column 5: Pain Points
- H2: <100 characters
- Body: 200-300 characters
- MUST reflect real user pain points based on research

### Column 6: Feature Highlights
- H2: <100 characters
- P(Intro): 100-200 characters
- H3: <30 characters each
- Default: **3 highlights**
- P under each H3: **135-139 characters** (mobile precision limit)

### Column 7: How to Use / Tutorial
- H2: <32 characters
- 3 steps: Upload → Click Generate → Download
- Step H3: ≤30 characters each
- Step P: **135-139 characters** each

### Column 8: CTA
- H2: ~50 characters
- P: <200 characters
- Button text: ~20 characters

### Column 9: User Reviews
- Default: **6 reviews**
- Each review: **300-350 characters**
- Each MUST contain core keyword
- Format: full name + profession + review text
- 🔴 **H2 fixed template**: `What Users Say About [Core Keyword]` — always use "Users", never narrow to a specific group like "Swimwear Brands" or "Designers"

### Column 10: FAQ
- Default: **6 Q&A pairs**
- **MANDATORY: both Q and A must embed keywords**
- Answer: **300-350 characters** each
- 🔴 **Zero article in BOTH Q and A**: no a/an/the before tool keyword in question OR answer — "How does AI Jewelry Design Generator work?" and "AI Jewelry Design Generator processes..." NOT "How does an AI..." or "The AI Jewelry Design Generator processes..."
- 🔴 **No overlap with Col 3-8**: FAQ questions must NOT duplicate content already covered in earlier columns. Col 3 covers product definition, Col 4 covers recommendation, Col 5 covers pain points, Col 6 covers features, Col 7 covers tutorial, Col 8 covers CTA. FAQ should cover complementary topics these columns did not address: licensing/rights, privacy, output specs, compatibility, usage limits, batch generation, refunds, etc.

### Column 11: Schema Markup
- Type: `SoftwareApplication`
- Fields: name, url, description, offers (price 0 for free tools)
- aggregateRating: optional, only if available
- Brand word in Schema counts toward the 10 total

## Brand Word Rules

- **Ask the user** what the brand word is before generating content
- Brand word MUST appear exactly **10 times** across all content (including Schema code block)
- Count carefully and verify before output
- **Possessive form**: when brand word introduces a tool name, use `Brand's` not `Brand`. Example: `YourBrand's AI Tool Name` NOT `YourBrand AI Tool Name`. This applies throughout all columns and is grammatically correct for tool ownership.

## Anchor Text Links

Each English page must include **5 anchor text links**:

### Self-links (3 — Col 3/4/5 Body)

In Col 3, 4, 5 body text, the **first natural occurrence** of the core keyword becomes a clickable link to the current page.

```
[Core Keyword](https://your-domain.com/{path})
```

- 🔴 **Anchor text links must NOT be bolded** — use plain `[text](url)`, never `**[text](url)**`

### Cross-links (2 — End of Col 3 Body)

User provides 2 cross-feature links each time (feature name + URL). Naturally integrate into the end of Col 3 body as a functional extension, not a forced upsell. Freely adapt the connection based on how the features relate.

- User provides: English feature names + English URLs
- Link targets: `https://your-domain.com/{path}`

**Example (AI Mockup Generator + AI Product Photography / AI Background Changer)**:
```
…all from one tool. When you need real product shots or background swaps, pair it with [AI Product Photography](https://your-domain.com/ai-product-photography) and [AI Background Changer](https://your-domain.com/ai-background-changer) for a complete workflow.
```

## Keyword Usage Rules

### 🔴 Zero Article Principle
- 🔴 **ALL tool keywords — NOT just core keyword** — must NOT take articles (a / an / the) before them, anywhere in the entire page
- This applies to ALL 11 columns — H2, body, reviews, FAQ (Q & A both), CTA, every text field
- Example: ✅ "use AI Photo Editor" — ❌ "use an AI Photo Editor" — ❌ "use the AI Photo Editor"
- ✅ "AI Jewelry Design Generator creates..." — ❌ "The AI Jewelry Design Generator creates..."
- ✅ "with AI photo editing..." — ❌ "with an AI photo editing..."

### Keyword Independence
- Different pages on the same site MUST use strictly separated keywords
- Do NOT cross-contaminate keywords between pages

## Writing Style

1. Simple vocabulary, clear logic, no repetitive word stacking
2. **H2 titles**: use noun-form product name to build brand recognition
   - Body text: use action-verb keywords for SEO
3. Avoid absolute claims (e.g. "100%" → use "fully compliant")
4. Avoid cheap-sounding words (e.g. "remove blemishes" → use "perfect portraits")
5. Natural sentence structure: Verb + Noun + Free (e.g. "Make Passport Size Photo Free"), NOT "Free make..."
6. 🔴 **Pricing claims**: NEVER claim "completely free", "no subscription", or "no cost" unless confirmed. Use "offers free usage" / "provides free access" / "免费使用" / "無料で利用可能" instead — the tool may have usage limits or paid tiers.

## Image Recommendations

| Type | Size | Notes |
|------|------|-------|
| Social media / hero | 1200×630 | Column 2 |
| Feature illustration | 400×400 | Screenshot or diagram |
| General content | 500×420 | With background color |

## Format Cleanliness (Mandatory)

- **NO character count tails**: NEVER include `(57)`, `（152）`, or any character count annotations in output
- **NO extra symbols**: no stray pipes `|`, brackets, or markup artifacts
- Output clean, plain content suitable for direct use

## Output Delivery Rules

### 🔴 Phase Gate
- **NEVER output Phase 4 content before TDK is confirmed** by the user
- Before TDK approval: only show Phase 1 analysis + Phase 2 TDK table + verification
- After TDK approval: compile ALL content into a single `.md` file

### 🔴 File Output
- **After TDK confirmation, write everything to a `.md` file** — do NOT output inline in chat
- File naming: `SEO-[keyword]-[brand].md`
- File includes: Phase 1 analysis + Phase 2 TDK + Phase 4 11-column content + verification report
- All 11 columns use `| Section | Content |` table format

### 🔴 Competitor Link Enforcement
- Every competitor name MUST be a clickable Markdown link going to the **exact feature landing page**
- NOT just domain root — must open the actual tool/feature page on the competitor's site
- Use the actual ranking page URL from the API `url` field
- Verify all links are clickable before writing the output file

## Phase 1.5: Competitor TDK Analysis

After Phase 1 and user provides brand word, run Playwright-based real-browser TDK fetching.

### Why Playwright (not WebFetch/curl)
- `WebFetch` converts HTML→markdown, stripping `<meta name="description">` tags → false "not set" reports
- `curl` only gets static HTML; JS-rendered SPAs (Canva, Adobe, etc.) return empty `<head>`
- Playwright executes JavaScript, reads final DOM — equivalent to AITDK browser extension

### Script
- Use `references/competitor-tdk-fetcher.mjs`
- Copy to workspace, populate `COMPETITORS` array with URLs from Phase 1 table
- Run with managed Node.js

### Output Table Format
```
| # | Site | Title | Description | Status |
|---|------|-------|-------------|------|
| 1 | Fotor | AI Image Upscaler... (68c) | Upscale images online... (149c) | ✅ |
| 2 | Canva | — | — | ⚠️ Manual check needed (Cloudflare) |
| 3 | Adobe | — | — | ❌ Page unavailable |
```

### Failure Markers
| Marker | Meaning | Action |
|--------|---------|--------|
| ✅ | TDK captured | Use as reference |
| ⚠️ Manual check needed (Cloudflare) | Anti-bot wall | User checks with AITDK |
| ⚠️ JS-rendered, Meta may be incomplete | SPA returned partial data | Note in analysis |
| ❌ Page unavailable | 404/HTTP error | Skip this competitor |

### Notes
- This phase is **informational only** — no user confirmation needed, proceed to Phase 2 immediately
- Results inform TDK writing (see what top-ranking titles/descriptions look like)
- Locale set to `en-US` for consistent English results

### Common Pattern Analysis

After the competitor TDK table, output analysis of common patterns:

**Title Commonalities:**
| Dimension | Method |
|------|------|
| Structure Pattern | "Keyword – Hook + CTR" vs other patterns |
| High-frequency CTR Words | Count: Free, Online, No Sign Up, etc. |
| Keyword Position | Head (first), middle, or tail |
| Length Range | Min-Max chars |

**Description Commonalities:**
| Dimension | Method |
|------|------|
| Opening Pattern | Action verb or benefit-first |
| High-frequency Elements | Common phrases, value props |
| Length Range | Min-Max chars |

**TDK Insights**: 2-4 actionable bullets for writing our TDK

### 3-Title Output (Phase 2)

Based on competitor analysis, output the three best Title options:
- Each 50-60 chars, verified with Python `len()`
- All follow user rules: core keyword at the very beginning, no Free/Best before keyword, no brand word
- Three options differ in CTR word or functional long-tail angle
- Format in TDK table:
  ```
  | Title | **A:** [title_a] (XXc)<br>**B:** [title_b] (XXc)<br>**C:** [title_c] (XXc) |
  ```
- After presenting, ask "Which Title? A / B / C"

## User Input Requirements

| Required | Provided by |
|----------|-------------|
| Core keyword | User |
| Keyword meaning / intent | User OR AI research |
| Brand word | User (AI MUST ask) |
| Semrush/Ahrefs screenshots | User |
| Use steps (3) | AI generates |
| Feature highlights (3/4/6) | AI generates |
| Target user / value proposition | AI generates |

