# KD Scoring Guide

## Viability Formula Explained

```
Viability = (Volume / 1000) × (1 - KD/100) × TrendMultiplier × IntentMultiplier
```

### Why This Formula Works

- **Volume / 1000**: Normalizes search volume to a manageable scale. 18,000 volume → 18.0; 500 volume → 0.5.
- **(1 - KD/100)**: Inverts the difficulty score. KD 45 → 0.55 (55% attainable); KD 80 → 0.20 (only 20% attainable). Higher KD heavily penalizes viability.
- **TrendMultiplier**: Rewards growing topics (1.2×), penalizes declining ones (0.7×). A rising keyword with moderate KD can beat a stable keyword with low KD.
- **IntentMultiplier**: Commercial intent (high CPC) means users are ready to convert, so it gets a 1.3× boost. Pure informational queries (CPC = $0) are harder to monetize.

### Example Calculation

```
Keyword: "ai background remover"
Volume: 18,000 → 18.0
KD: 45 → (1 - 0.45) = 0.55
Trend: ↗ Rising → 1.2
CPC: $1.20 → Commercial intent → 1.3

Viability = 18.0 × 0.55 × 1.2 × 1.3 = 15.6
```

```
Keyword: "remove background from photo"
Volume: 5,000 → 5.0
KD: 35 → (1 - 0.35) = 0.65
Trend: → Stable → 1.0
CPC: $0.80 → Commercial intent → 1.3

Viability = 5.0 × 0.65 × 1.0 × 1.3 = 4.2
```

The first keyword has higher viability despite higher KD, because its volume is 3.6× larger and it's trending upward.

## KD Interpretation Thresholds

| KD Range | Interpretation | What It Means |
|----------|---------------|---------------|
| 0-20 | Very Easy | New sites can rank within weeks. Top-10 has weak content. |
| 21-40 | Easy | Reasonable chance with good content + basic SEO. |
| 41-60 | Moderate | Need strong content + backlinks. Achievable in 2-6 months. |
| 61-80 | Hard | Established brands dominate. Requires sustained effort. |
| 81-100 | Extremely Hard | Don't target directly. Use long-tail variants instead. |

## When to Trust vs. Distrust KD Estimates

### MCP Data (seo-web-cafe) — Most Trustworthy

The `seo-web-cafe` MCP provides KD scores calculated from a multi-signal model that includes:
- **Site strength** = 0.6×DR + 0.4×traffic score (log-normalized)
- **Signal system**: weak sites/weak homepages, dedicated-site density, strong homepage density, homepage crowding, Top-3 blockade, primary keyword density, volume prior, rising-phase trend, SERP experience fragility, new domain signals, domain migration detection
- **Brand keyword auto-switching**: excludes the brand's own site and platform ecosystem pages, scoring only contested positions
- **Link budget**: interpolated from the Ahrefs official KD→referring-domain curve using the final difficulty score

**Advantages over WebSearch estimates**:
- Real `details` data for each Top-10 competitor (DR, visits, dedicated, strength, contribution)
- `linkBudget` field tells you exactly how many referring domains you need to enter Top-10
- `keywordType` auto-detects brand keywords and switches scoring methodology
- `keywordTrend` with `ratio` gives precise rising phase signal

**Limitations**:
- MCP rate limit: 10 calls/minute, ≥6s interval
- Daily quota: 100 calls (login user), 500 (VIP)
- 7-day cache: repeated queries return cached results (use `force=1` to skip)
- Some keywords may return `keywordVolume: null` if data is sparse

### WebSearch Estimates — Fallback, Less Trustworthy

KD scores from tools (Ahrefs, Semrush, Ubersuggest) found via WebSearch are estimates based on backlink profiles. They can be misleading in these cases:

1. **Low-volume keywords with high KD**: Sometimes KD is high because 1-2 authoritative pages rank, but they're not actually optimized for the keyword. A well-targeted page can still rank.
2. **New trending topics**: KD may show as "easy" because few pages exist yet, but competition will increase rapidly. Check trend direction to validate.
3. **Forum/QA-dominated SERPs**: If Top-10 includes Reddit, Quora, Stack Overflow threads, KD may be low but the intent is informational — hard to convert.
4. **Brand-dominated SERPs**: If the brand itself already ranks #1-3, KD for that keyword may show high, but the brand can strengthen its position with a dedicated page.

**Rule of thumb**: Always cross-reference KD with actual SERP quality. If the Top-10 pages look weak (thin content, poor UX, no clear answer), even KD 50 is achievable. If they look strong (comprehensive guides, strong brands), even KD 30 may be harder than the number suggests.

## Long-Tail Variant Strategy

When the primary keyword is Red (KD > 60 or Volume < 1000), pivot strategies:

1. **Add qualifier words**: "free" / "online" / "for [use case]" / "without [problem]"
   - `ai background remover` (KD 45) → `free ai background remover online` (KD ~25)
2. **Shift from tool name to use case**: 
   - `ai image generator` (KD 70) → `ai image generator for social media` (KD ~35)
3. **Shift from generic to comparison**:
   - `background remover` (KD 55) → `remove.bg vs canva background remover` (KD ~15)
4. **Year-based freshness**:
   - `best ai tools` (KD 85) → `best ai tools 2026` (KD ~40, drops every year as old content expires)

Each variant should be run through the same research pipeline (Volume + KD + Trend + Intent) before committing.
