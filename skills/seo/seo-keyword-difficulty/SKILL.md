---
name: seo-keyword-difficulty
description: SEO keyword difficulty assessment and competitor analysis Skill. Given a target keyword, automatically queries search volume, difficulty score, Top-10 competitor page TDK, Google Trends data, and outputs a comprehensive recommendation report to decide which keywords to target for traffic. Trigger words: keyword difficulty, keyword research, SEO keyword analysis, keyword selection, KD analysis, competitor TDK. This Skill applies to all SEO content projects, not limited to any specific website.
agent_created: true
---

# SEO Keyword Difficulty & Competitor Analysis

Given a target keyword (or a list of candidates), this Skill runs an automated research pipeline that produces a **Keyword Decision Report**: search volume, difficulty score, Top-10 competitor TDK breakdown, trend direction, and a final recommendation on whether to write for this keyword or pivot to a better variant.

**This is Step 0 of the SEO automation pipeline** — before any page or blog content is written, you must know whether the keyword is worth targeting.

---

## MCP Dependency

**seo-web-cafe** (Keyword Difficulty Estimation MCP) is the **primary data source** for this Skill. It provides real KD scores, search volume, Top-10 competitor analysis, link budgets, and trend signals — far more accurate than WebSearch estimates.

**MCP endpoint**: `mcp__seo-web-cafe__estimate_keyword_difficulty`
- Parameters: `{keyword: string (required), gl: string (optional, default "us"), hl: string (optional, default "en"), force: string (optional, "1" to skip cache)}`
- Returns: score, level, keywordType, keywordVolume, keywordTrend, linkBudget, details (Top-10), reasons
- Rate limit: 10 calls/minute, ≥6 second interval between calls
- Auth: via URL token (`?token=wc_mcp_...`) embedded in MCP config

**If MCP is not connected**: Fall back to WebSearch for KD/Volume estimates. This is less accurate but still usable. Clearly label all fallback data with source ("WebSearch estimate" vs "seo-web-cafe MCP").

**To enable**: Add `seo-web-cafe` MCP to your agent with URL `https://seo.web.cafe/kd/mcp?token=wc_mcp_your_token_here`. 

---

## Trigger

Activate when the user asks to:
- Research keyword difficulty / search volume / competition
- Decide which keyword to target for a new SEO page
- Analyze competitor TDK for a given keyword
- Check Google Trends for a topic
- Run "keyword research" or "keyword selection" before content production

---

## Two Modes

### Mode A: Single Keyword Deep Dive

User provides **one keyword**. You produce a full report for that keyword and suggest 2-3 alternative long-tail variants if the primary keyword looks too competitive.

### Mode B: Keyword Comparison Batch

User provides **3-5 candidate keywords**. You produce a side-by-side comparison table, ranking them by viability (volume × difficulty × trend), and recommend the best one to target first.

If the user doesn't specify a mode, default to **Mode A** (single keyword deep dive).

---

## Phase 0: Collect Inputs

Ask the user in a single message:

1. **Target keyword(s)** — the primary keyword, or a list of 3-5 candidates for Mode B
2. **Language/market** — which Google domain to analyze (google.com for English, google.co.jp for Japanese, etc.). Default: `google.com` (English, global)
3. **Product/brand name** — so we can check whether the brand already ranks for this keyword
4. **Content type** — Page (tool landing page) or Blog (comparison/review article). This affects the competitor analysis lens: Page competitors are other tool pages; Blog competitors are review/comparison articles.

If any field is omitted, mark as "unspecified" and proceed with defaults.

---

## Phase 1: Automated Research Pipeline

Execute the following steps **in sequence**. Each step uses specific tools — do not skip any step.

### Step 1: Search Volume & Difficulty Score

**Primary tool**: `seo-web-cafe` MCP — call `mcp__seo-web-cafe__estimate_keyword_difficulty` with parameters `{keyword: "[keyword]", gl: "[gl code]"}`. This returns:
- `score`: KD 0–100 (for brand keywords, represents "derivative content entry difficulty")
- `level`: Very Easy / Easy / Moderate / Hard / Extremely Hard
- `keywordType`: `generic` general keyword / `brand` brand keyword (auto-detected)
- `keywordVolume`: Monthly search volume (12-month average)
- `keywordTrend`: Rising phase signal `{domain, volume, estimatedValue, ratio}`, ratio ≥ 1 = rapidly rising
- `linkBudget`: Link budget to enter Top-10 (referring domain count: low/mid/high)
- `details`: Top-10 competitor row-by-row breakdown (position, domain, pageType, dr, visits, dedicated, titleHit, kwHit, kwHitTraffic, searchShare, sitelinks, eng, strength, contribution)
- `reasons`: Judgment reasons, with detailed breakdown of signal weight contributions per signal

**MCP call frequency limit**: 10 calls/minute, ≥6 second interval between calls for batch queries. Repeated queries for the same keyword within 7 days hit the cache (instant return but still counted toward quota).

**Fallback**: If `seo-web-cafe` MCP is not connected or returns errors, use WebSearch to find publicly available estimates from Ahrefs/Ubersuggest/Semrush-style sources. Report the source of each metric.

**Additional data**: If Google Search Console MCP is connected AND the brand's site is verified in GSC, use `mcp__google-search-console__search_analytics` to pull the brand's existing performance data for this keyword (impressions, clicks, position, CTR). This supplements the MCP data with real ranking data.

For each keyword, collect:
- **Monthly search volume** — from `keywordVolume` field (MCP) or WebSearch estimate
- **Keyword Difficulty (KD) score** — from `score` field (MCP) or WebSearch estimate
- **KD level** — from `level` field (MCP): Very Easy (≤20) / Easy (21-40) / Moderate (41-60) / Hard (61-80) / Extremely Hard (81-100)
- **Keyword type** — from `keywordType` field (MCP): `generic` or `brand`
- **Link budget** — from `linkBudget.quality.mid` (MCP): median referring domains needed to enter Top-10
- **CPC** (if available from other sources — indicates commercial intent)
- **GSC data** (if available): impressions, clicks, avg position for this keyword on the brand's site

**Output format for each keyword:**

```
| Keyword | Volume | KD (0-100) | KD Level | Type | Link Budget (mid) | CPC | Source |
|---------|--------|-------------|----------|------|--------------------|-----|--------|
| ai background remover | 18,000 | 45 | Moderate | generic | 45 refs | $1.20 | seo-web-cafe MCP |
```

**Mode B batch processing**: For 3-5 keywords, call MCP for each keyword sequentially with ≥6 second intervals. Summarize all results in a single comparison table.

### Step 2: Top-10 Competitor TDK Analysis

**Primary data**: If Step 1 MCP call returned `details` array, it already contains Top-10 competitor data (position, domain, pageType, dr, visits, dedicated, titleHit, kwHit, kwHitTraffic, searchShare, sitelinks, strength, contribution). Use this as the **baseline** and enrich with TDK data.

**TDK enrichment**: Use WebSearch the target keyword on the specified Google domain. Then use WebFetch to read each of the Top-10 organic results, extracting their:

- **Title tag** (full text + character count)
- **Meta description** (full text + character count)
- **H1 tag** (if visible in the fetched content)
- **URL structure** (slug pattern)
- **Content type** (tool page, blog post, comparison, video, etc.)

**Merge MCP + WebFetch data**: Combine MCP `details` (DR, visits, dedicated, strength) with WebFetch TDK data into a single enriched table. If a competitor is in both data sources, merge all fields. If only in one, note which fields are missing.

For each competitor, note:
- Does their Title follow a pattern (e.g., "Free AI [Tool] — [Brand]" vs "Best [Tool] in 2025")?
- Does their Description include pricing/free claims?
- Is their H1 identical to the Title, or different?
- From MCP data: is the domain `dedicated` (dedicated to this keyword)? Does it have `sitelinks` (strong brand signal)? What's its `strength` score?

**Output format:**

```
| # | URL | Title (chars) | Desc (chars) | H1 | Type | Pattern | DR | Visits | Dedicated | Strength |
|---|-----|---------------|-------------|-----|------|---------|-----|--------|-----------|----------|
| 1 | remove.bg/... | Free Background Remover... (58) | Remove backgrounds from... (152) | Background Remover | Tool page | Free + Brand | 91 | 50M | Yes | 0.82 |
| 2 | canva.com/... | AI Background Remover... (52) | ... (160) | ... | Tool page | AI + Feature | 93 | 800M | No | 0.75 |
```

### Step 3: Google Trends Direction

**Primary data**: If Step 1 MCP call returned `keywordTrend`, it already contains trend signals: `{domain, volume, estimatedValue, ratio}`. `ratio ≥ 1` indicates the keyword is in a **rapid rising phase**. Use this as the primary trend indicator.

**Enrichment**: Use WebSearch for `"Google Trends [keyword]"` or use WebFetch on trends.google.com if accessible. Cross-validate with MCP trend data.

For each keyword, determine:
- **Trend direction** over the past 12 months: ↗ Rising / ↘ Falling / → Stable / ↕ Seasonal
- **Trend ratio** (from MCP): ratio value, if ≥ 1 = rapidly rising
- **Peak month** (if seasonal)
- **Relative interest** (0-100 scale from Trends data)

If Trends data is not directly accessible, infer direction from MCP `keywordTrend.ratio`, recent search volume changes, news coverage frequency, and whether the topic is tied to a technology that's still growing vs. declining.

### Step 4: SERP Feature Audit

**Tool**: WebSearch the keyword and note what SERP features appear:

- Featured snippet? (Yes/No — and who holds it)
- People Also Ask? (Yes/No — list top 4 questions)
- Knowledge panel? (Yes/No)
- Image pack? (Yes/No)
- Video results? (Yes/No — count)
- Sitelinks? (Yes/No — for which domains)

These features tell you what content format Google prefers for this keyword: if there's a featured snippet, a concise "What is" answer can win it; if there's a video pack, you may need video content too.

---

## Phase 2: Synthesize — Keyword Decision Report

After collecting all data, synthesize into a final decision report. **This is the most important output — the user needs a clear yes/no/pivot recommendation, not just raw data.**

### Viability Score Formula

Calculate a simple viability score for each keyword:

```
Viability = (Volume / 1000) × (1 - KD/100) × TrendMultiplier × IntentMultiplier

Where:
- TrendMultiplier: ↗ = 1.2, → = 1.0, ↘ = 0.7, ↕ = 0.5
- IntentMultiplier: CPC > $0.50 = 1.3 (commercial intent), CPC < $0.50 = 1.0, CPC = $0 = 0.7 (informational, lower conversion)
```

Higher viability = better keyword to target.

**Additional consideration — Link Budget feasibility**: If MCP returned `linkBudget.quality.mid`, compare it against the brand's current DR and referring domain count. If the brand's current referring domains < `linkBudget.quality.low`, the keyword is likely unattainable even if KD looks moderate. Flag this as a **link budget warning** in the report.

### Decision Categories

Based on viability score, KD, and link budget:

| Category | Criteria | Action |
|----------|----------|--------|
| 🟢 **Green — Go** | KD ≤ 40 AND Volume ≥ 5,000 AND Trend ↗/→ AND brand DR ≥ linkBudget.low | Write the page/blog. This keyword is attainable. |
| 🟡 **Yellow — Consider** | KD 41-60 OR Volume 1,000-5,000 OR brand DR < linkBudget.mid but ≥ linkBudget.low | Write, but also target a long-tail variant simultaneously for safety. |
| 🔴 **Red — Pivot** | KD > 60 OR Volume < 1,000 OR Trend ↘ OR brand DR < linkBudget.low | Do NOT target directly. Pivot to a long-tail variant (add qualifiers like "free", "online", "for [use case]"). |
| ⚪ **No Data** | Insufficient data for evaluation | Manual review needed. Gather more data before deciding. |

**Special case — Brand keyword**: If MCP returned `keywordType = "brand"`, the `score` represents "difficulty for third-party derivative content to enter this SERP". The brand itself can rank easily for its own brand keyword. Flag this clearly: "This is a brand keyword — the brand itself can rank, but third-party content targeting this word faces [KD score] difficulty."

### Report Structure

Output the report in this exact format:

```markdown
# Keyword Decision Report: [keyword]

## 1. Core Metrics
| Keyword | Volume | KD | KD Level | Type | Link Budget (mid) | CPC | Trend | Trend Ratio | Viability |
|---------|--------|----|----------|------|--------------------|-----|-------|-------------|-----------|
| [primary] | [V] | [KD] | [level] | [generic/brand] | [refs] | [$] | [↗/→/↘] | [ratio] | [score] |
| [variant 1] | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| [variant 2] | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Link budget feasibility**: [brand current DR = X, link budget low/mid/high = Y1/Y2/Y3 refs → 🟢 feasible / 🟡 borderline / 🔴 unattainable]

## 2. Decision
**[🟢 Green / 🟡 Yellow / 🔴 Red]: [recommendation sentence]**

Example: "🟢 Green — 'ai background remover' is attainable with KD 45 and 18K monthly volume. Write the tool page."

## 3. Competitor TDK Summary
[Enriched Top-10 table with MCP DR/Visits/Dedicated/Strength + WebFetch TDK]

**Pattern insights**: [2-3 sentences about what patterns dominate the SERP — e.g., "6 of 10 competitors use 'Free' in Title; only 2 use 'Best'."]

**SERP strength analysis**: [From MCP data: how many Top-10 results are `dedicated` (dedicated to this keyword)? How many have `sitelinks` (strong brand signal)? Average `strength` score of Top-10? This tells you how "locked" the SERP is.]

**Opportunity gaps**: [1-2 sentences about what no competitor is doing — e.g., "None of the Top-10 include a year (2025/2026) in Title — adding one could differentiate."]

## 4. SERP Features
| Feature | Present | Holder/Notes |
|---------|---------|-------------|
| Featured snippet | Yes/No | ... |
| People Also Ask | Yes/No | [top 4 questions] |
| Image pack | Yes/No | ... |
| Video results | Yes/No | [count] |

**Content format recommendation**: [e.g., "Featured snippet exists → ensure S1 What Is has a concise 40-60 char answer eligible for snippet capture."]

## 5. Recommended Long-Tail Variants (if Red/Yellow)
| Variant | Volume | KD | Why |
|---------|--------|----|-----|
| [variant 1] | ... | ... | [reason] |
| [variant 2] | ... | ... | [reason] |

## 6. Next Step
Based on the decision, the next action is:
- 🟡 → Run page-writer for primary keyword + blog-writing for a long-tail variant
- 🔴 → Re-run this Skill with suggested long-tail variants before writing anything
```

---

## Quality Checklist

Before delivering the report, verify:

1. **All 4 research steps completed**: Volume/KD ✓, Competitor TDK ✓, Trends ✓, SERP Features ✓
2. **Competitor count**: At least 8 of Top-10 competitors analyzed (2 may be inaccessible — note which ones failed)
3. **Viability score calculated**: Formula applied correctly, all multipliers accounted for
4. **Decision category assigned**: Green/Yellow/Red/No Data, with clear action recommendation
5. **Pattern insights present**: At least 2 observations about Title/Description patterns in the SERP
6. **Opportunity gaps identified**: At least 1 gap that no competitor is exploiting
7. **Long-tail variants provided**: If Red/Yellow, at least 2 alternatives with their own metrics
8. **Next step specified**: Clear handoff to the next Skill in the pipeline

---

## Resources

### references/

- `references/kd-scoring-guide.md` — Detailed explanation of the viability formula, KD interpretation thresholds, and when to trust vs. distrust third-party KD estimates.
