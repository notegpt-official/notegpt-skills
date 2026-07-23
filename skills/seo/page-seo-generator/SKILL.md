---
name: page-seo-generator
description: This skill should be used when the user wants to generate a complete 11-column SEO landing page for a website. It handles the full workflow: keyword research, TDK generation, and structured content output. Triggers include requests like "generate an SEO page", "create a landing page", "generate TDK", "SEO content", "landing page SEO", or providing a keyword with SEO intent.
agent_created: true
---

# Page SEO Content Generator

Generate complete 11-column SEO landing page content from a single keyword input.

> **Language constraint:** Output templates (section headers, table headers, user prompts, verification reports) MUST match the user's input language. If the user communicates in Chinese, output in Chinese. If in English, output in English. If in Japanese, output in Japanese. The templates below show English as the default; adapt to the user's language automatically.

> **Cross-platform tip:** Use `python` instead of `python3` on Windows. `~` is `%USERPROFILE%` on Windows.

## 🔴🔴🔴 COMPETITOR LINKS — READ FIRST, NEVER VIOLATE 🔴🔴🔴

**Every competitor name in the Phase 1 table MUST link to the exact feature/tool landing page URL — NOT the domain root.**

- ✅ CORRECT: `[canva.com/features/image-upscaler](https://www.canva.com/features/image-upscaler)` — goes directly to the upscaler tool
- ❌ WRONG: `[canva.com](https://www.canva.com)` — goes to homepage, user can't find the feature page
- ❌❌❌ NEVER use plain domain root as link target for competitors

**How to find the correct URL:**
1. API often only returns domain names — you MUST construct the feature page URL yourself
2. Search the web or infer the URL pattern: `https://<domain>/<tool-path>` for each competitor
3. Verify each link points to the tool/feature page for THIS keyword, not a homepage
4. **Before writing any output file, scan every `[...](url)` to confirm it opens a feature page**

This rule can never be skipped, bypassed, or "good-enoughed". Wrong links = wasted output.

---

## Required Inputs Summary

This skill will guide you to collect these inputs at the appropriate phase:

1. **Keyword** (Phase 1 start) — the target keyword for the page
2. **Brand Word** (Phase 1 end) — brand name to use throughout the content
3. **TDK Approval** (Phase 3) — user chooses one of 3 Title options before Phase 4

The skill has built-in prompts to collect each input at the right time. Do NOT proceed to the next phase until the required input is provided.

---

## Workflow (4 Phases, Sequential)

The workflow MUST follow this exact sequence. Do NOT skip phases.

### Phase 1: Keyword Research & Analysis

When the user provides a keyword, run a comprehensive analysis in this exact order:

1. **Load `seo-keyword-difficulty` skill** — call it with the keyword to get:
   - Keyword difficulty score, level, search volume, link budget
   - Top 10 competitor details (domain, DR, traffic, age, dedicated status)
   - Verdict: whether the keyword is worth doing

2. **Research the keyword independently:**
   - Meaning and search intent
   - Existing competitor tools and their offerings
   - Target user profiles and pain points

3. **Phase 1 output structure** (MUST follow this order):

   **📖 Keyword Meaning**
   - What the keyword means, what the tool does, use cases

   **🎯 Demand Positioning & Features**
   - Target positioning: who needs this, what gap does it fill, what makes it different
   - Include competitive landscape insight

   **👥 User Personas**
   - Table: Persona | Use Case | Search Intent
   - 3-4 user segments with clear motivation

   **📊 SEO Keyword Difficulty Analysis**
   - Summary table: score, level, volume, link budget
   - Top 10 competitor table with these columns: # | Page (🔴 Must Be Clickable Link) | DR | Monthly Traffic | Year | Dedicated Page | Notes
   - **🔴 Competitor Link Rule**: Every competitor name MUST be a clickable Markdown link. Use the `url` field from the API, format `[domain/path](full URL)`. NEVER use plain text domain names.
   - Google Trends explore URL
   - Final verdict with supporting reasons

   **❓ Brand word question** — ask user for brand word, do NOT assume. End Phase 1 here. Do NOT output use steps or highlights.

   **🔴 Phase 1 scope is STRICT**: only the 4 sections above. End Phase 1 with brand word question. Do NOT output use steps or highlights.

Once user provides brand word, proceed to Phase 1.5 before TDK.

### Phase 1.5: Competitor TDK Analysis (Playwright)

After Phase 1 and before Phase 2, automatically fetch real Title + meta description from top competitor ranking pages using Playwright (headless Chromium). This replaces the unreliable `WebFetch` approach which strips `<meta>` tags during HTML→markdown conversion.

**Workflow:**

1. Use the top competitor URLs from Phase 1's competitor table
2. For each competitor URL, use Playwright to:
   - Navigate to the page with `waitUntil: 'load'`
   - Wait 4-6s for JS rendering
   - Extract `document.title` and `<meta name="description" content="...">`
   - Fallback: try `<meta property="og:description">` if name="description" is missing
3. For `window.chrome.runtime` injection to suppress `navigator.webdriver` detection

**Script:** Use `references/competitor-tdk-fetcher.mjs` — copy it to the workspace, then run:

**macOS / Linux:**
```bash
node competitor-tdk-fetcher.mjs
```

**Windows (PowerShell):**
```powershell
node competitor-tdk-fetcher.mjs
```

Pass in the competitor URLs as arguments.

**Output — Competitor TDK table:**

```
| # | Site | Title (Length) | Description (Length) | Notes |
|---|------|---------------|---------------------|-------|
| 1 | Site A | ... (XXc) | ... (XXc) | ✅ |
| 2 | Site B | ... (XXc) | ... (XXc) | ✅ |
| 3 | Canva | — | — | ⚠️ Manual Check Needed (Cloudflare) |
```

**Handling failures:**
- Cloudflare/anti-bot (e.g. Canva): Mark `⚠️ Manual Check Needed (Cloudflare)` — user checks with AITDK browser extension
- JS-rendered SPA with no SSR: May return generic title — mark `⚠️ JS Rendering, Meta May Be Incomplete`
- HTTP errors / 404: Mark `❌ Page Unavailable`
- Target: ≥70% of competitors successfully fetched

After outputting the TDK table, immediately output a **Common Pattern Analysis**, then proceed to Phase 2. Do NOT wait for user confirmation.

#### Common Pattern Analysis

Analyze what all successfully-fetched competitors have in common:

**Title Commonalities:**
- Structure Pattern: what pattern dominates (e.g. "Keyword – Hook + CTR", "Brand | Keyword – Benefit")
- High-Frequency CTR Words: which CTR words appear most across competitors
- Keyword Position: where is the core keyword (head/middle/tail)
- Length Range: min-max chars among fetched titles

**Description Commonalities:**
- Opening Pattern: action verb or benefit-first?
- High-Frequency Elements: common value props, phrases
- Length Range: min-max chars among fetched descriptions

**TDK Insights:**
- 2-4 actionable bullets for writing our Title and Description

### Phase 2: TDK Skeleton

Load `references/rules.md` for detailed specifications.

**🔴 Title: Output 3 options (A / B / C) — learn from competitors and provide the three best titles.**

Generate 3 title options, each informed by competitor learnings from Phase 1.5:
- Learn from competitor structure patterns, high-frequency CTR words, and keyword positioning
- Each option follows user rules: core keyword (noun-form tool definition word) at the beginning; no prefixing with "Free" or "Best"; no brand word
- Three options should differ in CTR words or functional long-tail, giving the user different angles to choose from

Output TDK table with Title row containing all 3 options:

```
| Type | Content (Copy from Right) |
| --- | --- |
| Title | **A:** ... (XXc)<br>**B:** ... (XXc)<br>**C:** ... (XXc) |
| Description | ... |
| Keywords | ... |
| URL | ... |
| Above-the-Fold Title (H1) | ... |
| Above-the-Fold Description | ... |
| SEO Image Assets | (Leave blank) |
| Model Used | (Leave blank) |
```

After presenting, ask "Which Title? A / B / C" — wait for user choice before Phase 4.

**Character count limits:**

| Field | Limit | Verification |
|-------|-------|-------------|
| Title (each) | 50-60 chars | `len(title)` × 3 |
| Description | 150-160 chars | `len(desc)` |
| Keywords | Exactly 5, all lowercase | count + case check |
| H1 | core keyword only (e.g. `AI Fat Filter`) | `len(h1)` |
| Above-the-Fold Desc | <114 chars | `len(top)` |

**🔴 MANDATORY: Python `len()` verification before presenting TDK.**

After writing TDK content, run a Python one-liner to verify every character count:

```bash
python3 -c "
print(f'Title A: {len(\"<title_a>\")} chars')
print(f'Title B: {len(\"<title_b>\")} chars')
print(f'Title C: {len(\"<title_c>\")} chars')
print(f'Description: {len(\"<desc>\")} chars')
print(f'H1: {len(\"<h1>\")} chars')
print(f'Above-the-Fold Desc: {len(\"<top>\")} chars')
"
```

Only present TDK when ALL values are verified within range. If any field is out of range, regenerate it and re-verify.

**Character count report** must be included below the TDK table as:

```
📊 Python len() Verification:
- Title A: XX chars ✅/❌ (50-60)
- Title B: XX chars ✅/❌ (50-60)
- Title C: XX chars ✅/❌ (50-60)
- Description: XX chars ✅/❌ (150-160)
- Above-the-Fold Desc: XX chars ✅/❌ (<114)
```

Use English by default. For Japanese, Title 30-40 chars, Description 100-110 chars, use katakana keywords.

Custom rule: **Ask the user for the brand word before outputting TDK.** If not yet received, ask again before Phase 2.

### Phase 3: TDK Approval

Present TDK table with 3 Title options (A/B/C). Wait for user to choose one Title. **🔴 STRICT GATE: Do NOT output Phase 4 content before user explicitly picks a Title.** Only output TDK table + verification + "Which Title? A / B / C" in this phase.

Once user picks a Title, that Title locks in for all subsequent content.

### Phase 4: Full 11-Column Content

**🔴 OUTPUT FORMAT: Write all content to a single .md file. Do NOT output inline in chat.**

After the user confirms TDK, compile EVERYTHING into one `.md` file containing:
- Phase 1 analysis (Keyword Meaning, Demand Positioning & Features, User Personas, Keyword Difficulty Analysis)
- Phase 2 TDK table + verification
- Phase 4: All 11 columns in `| Column | Content |` table format
- Phase 4 verification report

The file name should be: `SEO-[keyword]-[brand].md` (e.g. `SEO-AI-Photo-Enhancer-YourBrand.md`)

Save to the current workspace directory.

Load `references/rules.md` for all specifications before generating content.

Generate all 11 columns using the `| Column | Content |` table format for each column (each independently copyable):

1. **Column 1: Feature Area + TDK (Fullscreen H100)** — Full TDK summary table
2. **Column 2: H1 + Description + Button + Image** — Split layout, text + button on left, image 1200×630 on right
3. **Column 3: Product Introduction** — H2: "What Is ...?" with product noun, body 200-300 chars
4. **Column 4: Recommendation** — H2: "Why Choose ...?" with keyword, body 200-300 chars
5. **Column 5: Pain Points** — H2 <100 chars, body 200-300 chars
6. **Column 6: Highlights** — 3 highlights: H3 <30 chars, P exact 135-139 chars each
7. **Column 7: How to Use** — 3 steps: H3 ≤30 chars, P exact 135-139 chars
8. **Column 8: CTA** — H2 uses long-tail keyword, P <200 chars, button ~20 chars
9. **Column 9: User Reviews** — 6 reviews, 300-350 chars each, keyword in each
10. **Column 10: FAQs** — 6 Q&A, keyword in BOTH Q and A, answer 300-350 chars each
11. **Column 11: Schema Markup** — SoftwareApplication type

**🔴 MANDATORY: Python `len()` verification for ALL character-critical fields.**

Before presenting Phase 5 output, run Python verification on:
- All H2, H3, P fields (especially Columns 5/6/7 which have strict 135-139 limits)
- All 6 Review texts
- All 6 FAQ answers
- Brand word count exactly 10
- All 6 FAQ lines (6 Q + 6 A)

**Brand word count**: run `count()` or `.split().count()` to verify exactly 10 occurrences (including Schema).

Present verification summary below the content:

```
📊 Python len() Verification Report:
- Column 6 P(1-3): XX/XX/XX ✅
- Column 7 P(1-3): XX/XX/XX ✅  
- Reviews (1-6): XX/XX/XX/XX/XX/XX ✅
- FAQ Answers (1-6): XX/XX/XX/XX/XX/XX ✅
- Brand Word: XX occurrences ✅ (Target: 10)
```

## Critical Rules (Must Follow)

### Phase 1 Competitor Links
- **🔴 EVERY competitor name MUST be a clickable Markdown link** — no plain text domains
- **🔴 Links MUST go directly to the feature landing page** (the actual ranking URL), NOT just the domain root
- **🔴 Verify: clicking the link in the output file should open the exact competitor tool/feature page**
- Use the actual ranking page URL from the API `url` field; if the API only returns domain, construct the full feature page URL
- Format: `[domain.com/page-path](https://www.domain.com/page-path)` — clickable, goes to the exact ranking page
- Example: `[flair.ai](https://flair.ai/)` or `[sellerpic.ai/tools/product-in-hand](https://www.sellerpic.ai/tools/product-in-hand)`
- **Verify before output**: check that every competitor in the table has a clickable link going to the correct feature landing page

### Before Output
- **Brand word**: MUST be confirmed with user; appears exactly 10 times total (count includes Schema)
- **🔴 Zero article**: ALL tool keywords (core keyword + any tool-related terms) MUST NOT take a / an / the — applies to ALL columns (H2, body, reviews, FAQ Q & A, CTA)
- **Keyword isolation**: different pages on same site use strictly separated keywords

### During Output
- **Clean format**: no `(57)` or `（152）` character count tails; no stray `|` or artifacts
- **H2 naming**: use noun-form product name; body uses action-verb keywords
- **Writing style**: simple vocabulary, natural English, no cheap-sounding words, no absolute claims

### After Output
- **🔴 Run Python `len()` verification** on ALL character-critical fields — never guess or eyeball
- **🔴 Run Python `count()` verification** on brand word = exactly 10 (including Schema)
- Verify no format artifacts remain (no `(57)`, no `|` tails)

