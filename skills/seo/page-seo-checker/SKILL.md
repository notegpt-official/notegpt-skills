---
name: page-seo-checker
description: "Check SEO compliance of any domain page based on internal SEO standards and page launch checklist, generating a visual HTML report. Automatically extracts domain from URL, supports production and test environments. Trigger keywords: check SEO, SEO check, check page SEO, page SEO compliance, SEO report. Activate when user provides a page URL and requests SEO compliance check."
agent_created: true
---

# Page SEO Checker — 12-Point Automated Audit

Given a live page URL (production or test environment), this Skill runs a **12-point automated SEO compliance check** and produces a visual HTML report. It verifies that every page meets all hard constraints before going live.

**This is the final step of the SEO automation pipeline** — after content is written, images generated, and localization applied, run this check as the quality gate before publishing.

---

## MCP Dependency

**seo-web-cafe** MCP can optionally be used in this Skill to validate keyword difficulty assumptions. If the page's target keyword was analyzed using seo-keyword-difficulty (Step 0), the checker can cross-reference: did the page actually target a 🟢/🟡 keyword, or was it written for a 🔴 keyword that should be pivoted?

**MCP endpoint**: `mcp__seo-web-cafe__estimate_keyword_difficulty`
- Not required for the core 12-point audit, but available for keyword validation if needed
- If connected, use it to verify the page's primary keyword KD level matches the original decision report

---

## Trigger

Activate when the user asks to:
- Check SEO compliance of a page
- Run an SEO audit on a URL
- Verify page SEO before publishing
- Generate an SEO report

The user must provide a **live URL** (http/https) — this Skill checks real published pages, not draft Markdown.

---

## Required Inputs (Collect First)

**Before starting the audit**, collect the following from the user:

1. **Page URL** — the live page to check (production or test environment)
2. **Brand Name** — the brand name that should appear in the page (needed for Check 1 and Check 12)

Ask in one message:
> "To run the SEO audit, I need:
> 1. The page URL to check
> 2. Your brand name (for brand mention verification)
>
> Please provide these before I start."

Once collected, proceed to Phase 0 below.

---

## Phase 0: Identify Target

1. **URL** — the page to check (provided by the user)
2. **Environment** — auto-detect from URL:
   - Production: domain matches `your-domain.com`, etc.
   - Test/Staging: domain contains `test`, `staging`, `dev`, `localhost`, or non-production subdomains
3. **Language** — auto-detect from URL path prefix (`/ja/`, `/zh/`, `/ko/`, or default English)

If the URL is unreachable (404/5xx), report the error immediately and stop — there's nothing to check.

---

## Phase 1: 12-Point Automated Audit

For each check point, use **WebFetch** to read the live page, then verify the specific constraint. Each point produces a **Pass ✓** or **Fail ✗** result with details.

### Check 1: Title Tag

- **Requirement**: Title exists, contains brand name, 50-60 characters, no banned phrases
- **Method**: Extract `<title>` from page HTML
- **Verify**:
  1. Title tag exists and is non-empty ✓/✗
  2. Character count within 50-60 ✓/✗ (report actual count)
  3. Contains brand name (as specified by user) ✓/✗
  4. Does NOT contain banned openings: "is an AI-powered tool that..." / "is the ultimate solution..." ✓/✗
  5. No articles (a/an/the) before tool name in Title ✓/✗

### Check 2: Meta Description

- **Requirement**: Description exists, 150-160 characters, contains core keyword, no banned phrases
- **Method**: Extract `<meta name="description">` from page HTML
- **Verify**:
  1. Description tag exists and is non-empty ✓/✗
  2. Character count within 150-160 ✓/✗ (report actual count)
  3. Contains at least 1 core keyword ✓/✗
  4. Does NOT contain banned buzzwords ("revolutionize", "game-changer", etc.) ✓/✗

### Check 3: Canonical Tag

- **Requirement**: `<link rel="canonical">` exists and points to the correct self-referencing URL
- **Method**: Extract canonical link from page HTML
- **Verify**:
  1. Canonical tag exists ✓/✗
  2. Canonical URL matches the current page URL (ignoring query params/trailing slashes) ✓/✗
  3. Canonical URL uses HTTPS ✓/✗

### Check 4: H-Tag Structure

- **Requirement**: Proper hierarchy — exactly 1 H1, H2s for each section, no skipped levels
- **Method**: Extract all `<h1>` through `<h6>` tags from page HTML
- **Verify**:
  1. Exactly 1 H1 tag on the page ✓/✗ (report count)
  2. H1 contains brand/product name ✓/✗
  3. H2 tags present for all 8 sections (S1-S8) ✓/✗
  4. No H3 used where H2 should be, no H4 used where H3 should be ✓/✗
  5. H-tag hierarchy is sequential (H1 → H2 → H3, no H1 → H3 skips) ✓/✗

### Check 5: Body Content — Character Limits

- **Requirement**: Each section's content meets the character limits defined in page-writer
- **Method**: Parse section content by `<!-- S1-S8 -->` HTML comments, or by H2 boundaries
- **Verify**:
  1. S1 What Is: 200-300 chars ✓/✗ (report count)
  2. S2 Pain Point: P ≤ 200 chars ✓/✗ (report count)
  3. S3 Feature summary: ≤ 100 chars ✓/✗ (report count)
  4. S3 Each feature description: ~100 chars ✓/✗ (report count)
  5. S4 Each user group: ≤ 150 chars ✓/✗ (report count)
  6. S5 Each step: ~70 chars ✓/✗ (report count)
  7. S6 CTA: ≤ 150 chars ✓/✗ (report count)
  8. S7 Each review: ≥ 300 chars ✓/✗ (report count)
  9. S8 Each FAQ answer: 200-300 chars ✓/✗ (report count)

### Check 6: Testimonials — Realism & Variety

- **Requirement**: 6 reviews with at least 4 different narrative arcs, no banned patterns
- **Method**: Extract review block content from S7
- **Verify**:
  1. At least 6 distinct reviews present ✓/✗ (report count)
  2. No "I've been using X for Y months and it's amazing!" openings ✓/✗
  3. At least 4 different narrative arcs identifiable ✓/✗ (list arcs found)
  4. Each review ≥ 300 chars ✓/✗

### Check 7: FAQ — Structure & Banned Patterns

- **Requirement**: 10 FAQs, Q1 is "What is [Product]", no banned openings
- **Method**: Extract FAQ block from S8
- **Verify**:
  1. At least 10 FAQs present ✓/✗ (report count)
  2. Q1 asks "What is [Product] and what makes it different?" ✓/✗
  3. No "Absolutely!" or "Great question!" answer openings ✓/✗
  4. Each answer 200-300 chars ✓/✗ (report min/max)

### Check 8: Image ALT Tags

- **Requirement**: All `<img>` tags have non-empty, descriptive alt text containing keyword
- **Method**: Extract all `<img>` tags and their `alt` attributes from page HTML
- **Verify**:
  1. Every `<img>` has an `alt` attribute ✓/✗ (report count of missing alt)
  2. Alt text is non-empty (not just "") ✓/✗
  3. At least 1 image alt contains the core keyword ✓/✗
  4. Alt text describes content, not just "image" or "photo" ✓/✗

### Check 9: Internal Links

- **Requirement**: At least 3 internal links to other site pages, using keyword-rich anchor text
- **Method**: Extract all `<a>` tags with href pointing to the same domain
- **Verify**:
  1. At least 3 internal links present ✓/✗ (report count)
  2. Anchor text is descriptive (not "click here" or "learn more") ✓/✗
  3. Links point to other tool/content pages (not just homepage) ✓/✗

### Check 10: Schema / Structured Data

- **Requirement**: FAQ Schema (FAQPage) and/or Product Schema present in JSON-LD
- **Method**: Extract `<script type="application/ld+json">` blocks from page HTML
- **Verify**:
  1. At least 1 JSON-LD block exists ✓/✗
  2. If FAQ section exists: FAQPage schema with all 10 Q&A pairs ✓/✗
  3. Schema is valid JSON (no syntax errors) ✓/✗
  4. Schema `@type` matches content (FAQPage for FAQ, Product/SoftwareApplication for tool pages) ✓/✗

### Check 11: Hreflang Tags (if localized page)

- **Requirement**: If the page is a localized version (ja/zh/ko path), hreflang tags must link back to all language variants including the English original
- **Method**: Extract all `<link rel="alternate" hreflang="...">` tags
- **Verify**:
  1. Hreflang tags exist ✓/✗ (skip check if English-only page)
  2. Includes `hreflang="en"` pointing to original English page ✓/✗
  3. Includes `hreflang="x-default"` ✓/✗
  4. Includes hreflang for each available language variant ✓/✗
  5. All hreflang URLs are valid HTTPS ✓/✗

### Check 12: Brand Name Count & Zero-Article Compliance

- **Requirement**: Brand name appears exactly 10 times; no articles before tool names
- **Method**: Search body content for the brand name (as specified by user) occurrences; also search for `[a/an/the] [tool name]` patterns
- **Verify**:
  1. Brand name count = 10 ✓/✗ (report actual count and per-section distribution)
  2. No instances of "an AI [tool]", "the AI [tool]", "a [tool name]" where tool name is the site's specific product ✓/✗ (report any violations found)

---

## Phase 2: Score Calculation

### Scoring

Each check point is worth points based on its SEO impact:

| # | Check | Points | Weight |
|---|-------|--------|--------|
| 1 | Title Tag | 10 | High — Title is the #1 SEO signal |
| 2 | Meta Description | 8 | High — CTR driver |
| 3 | Canonical | 5 | Medium — Prevents duplication |
| 4 | H-Tag Structure | 8 | High — Content hierarchy signal |
| 5 | Body Content Limits | 10 | High — Readability + quality |
| 6 | Testimonials | 5 | Medium — Trust signals |
| 7 | FAQ | 8 | High — FAQ Schema eligibility |
| 8 | Image ALT | 5 | Medium — Accessibility + image SEO |
| 9 | Internal Links | 5 | Medium — Crawlability + authority flow |
| 10 | Schema | 10 | High — Rich results eligibility |
| 11 | Hreflang | 5 | Medium — International SEO (skip if N/A) |
| 12 | Brand Count & Zero-Article | 5 | Medium — Brand consistency |
| **Total** | | **86** | |

- If Check 11 is skipped (English-only page), total becomes **81**. Scale score proportionally.
- **Pass ≥ 80%** = Green (ready to publish)
- **Pass 60-79%** = Yellow (fix critical items before publishing)
- **Pass < 60%** = Red (do NOT publish — major issues need fixing first)

---

## Phase 3: Generate HTML Report

Produce a standalone HTML file with the following sections:

### Report Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SEO Audit Report — [URL]</title>
  <style>
    /* Clean, professional styling */
    /* Green ✓ / Red ✗ indicators */
    /* Collapsible details for each check */
    /* Summary score banner at top */
  </style>
</head>
<body>
  <header>
    <h1>SEO Audit Report</h1>
    <div class="meta">URL: [url] | Date: [date] | Env: [prod/test] | Lang: [en/ja/zh/ko]</div>
    <div class="score-banner">
      <span class="score">[X]/[total]</span>
      <span class="badge [green/yellow/red]">[Green/Yellow/Red]</span>
    </div>
  </header>

  <section class="checks">
    <!-- For each of the 12 checks -->
    <div class="check [pass/fail]">
      <h3>Check [N]: [Name]</h3>
      <span class="result">[✓ Pass / ✗ Fail]</span>
      <details>
        <summary>Details</summary>
        <table>
          <tr><td>Sub-check</td><td>Result</td><td>Value</td></tr>
          <!-- Each sub-verification item -->
        </table>
      </details>
      <div class="fix-if-fail">[If ✗: specific fix instruction]</div>
    </div>
  </section>

  <section class="summary">
    <h2>Summary & Action Items</h2>
    <ul>
      <!-- List all ✗ items with fix instructions -->
    </ul>
    <h2>Recommendation</h2>
    <p>[Green: Ready to publish / Yellow: Fix [N] items / Red: Do not publish]</p>
  </section>
</body>
</html>
```

Save the report as `seo-audit-[domain]-[date].html` in the current working directory.

---

## Phase 4: Fix Recommendations

For each ✗ item, provide a **specific, actionable fix**:

| Check | Typical Fix |
|-------|------------|
| Title too long/short | "Shorten Title to 50-60 chars: suggested rewrite: `[new title]`" |
| Missing canonical | "Add `<link rel=\"canonical\" href=\"[url]\">` to `<head>`" |
| H-tag skip | "Change H3 to H2 on `[section]`, or add missing H2 before the H3 block" |
| Missing FAQ schema | "Add JSON-LD block with FAQPage schema containing all 10 Q&A pairs" |
| Brand count off | "Add/remove [N] brand mentions. Suggested positions: [list]" |
| Zero-article violation | "Replace `an AI background remover` → `AI background remover` in [location]" |

Do not just say "fix it" — give the exact correction.

---

## Quality Checklist

Before delivering the report, verify:

1. **All 12 checks executed**: None skipped (except Check 11 for English-only pages)
2. **URL was reachable**: Page successfully fetched — if not, report error and stop
3. **Score calculated correctly**: Total points match, percentage correct
4. **HTML report generated**: File saved, visually clean and complete
5. **Fix recommendations provided**: Every ✗ has a specific correction
6. **Decision category assigned**: Green/Yellow/Red with clear publish/don't-publish recommendation

---

## Resources

### references/

- `references/seo-checklist.md` — The full SEO checklist with all 12 points, sub-verification items, and expected values. Load this at the start of each audit to ensure completeness.
- `references/report-template.html` — Starter HTML template for the audit report. Customize with actual data each run.
