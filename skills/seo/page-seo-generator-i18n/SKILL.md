---
name: page-seo-generator-i18n
description: This skill should be used when the user wants to generate native-language SEO landing page content for non-English markets (Japanese, Chinese, and other languages). Unlike page-seo-generator which requires keyword research and TDK generation for English pages, this skill assumes TDK (Title, Description, Keywords) is already provided by the user. The focus is on generating culturally-native SEO content in the target language — never machine-translated from English. Use this skill when the user provides TDK for a non-English SEO page or requests native-language SEO content generation.
agent_created: true
---

# Page SEO Content Generator — i18n (Multilingual SEO Content Generation)

Generate native-language 11-column SEO landing page content. Unlike the English-focused `page-seo-generator`, this skill **assumes TDK is already provided** and focuses on localizing content from an English source page — keeping product facts consistent while adapting expression to the target language culture. The output reads as if written by a native speaker, never as a machine translation.

## Workflow (2 Phases, Sequential)

### Phase 1: Input Collection

Before generating content, collect ALL of the following from the user:

| Required | Field | Notes |
|----------|-------|-------|
| ✅ | **Language** | `ja` (Japanese) or `zh` (Chinese). Other languages supported by asking |
| ✅ | **Core Keyword** | The target keyword for the page (in target language) |
| ✅ | **Title** | Provided TDK Title (in target language) |
| ✅ | **Description** | Provided TDK Description (in target language) |
| ✅ | **Keywords** | Provided TDK Keywords (in target language) |
| ✅ | **URL Path** | User provides English URL (e.g. `/ai-mockup`). Auto-prefix with language code: zh → `/zh-CN/...`, ja → `/ja/...`. Full URL: `https://your-domain.com/{lang}/{path}` |
| ✅ | **Brand Word** | Brand name as it should appear in content |

**If any field is missing, ask the user before proceeding.** Do NOT assume or generate TDK.

Once all fields are collected, present a confirmation summary in the same language as the user's input:

```
📋 Confirmation:
- Language: Japanese (ja) / Chinese (zh)
- Core Keyword: XXX
- Title: XXX
- Description: XXX
- Keywords: XXX
- URL: XXX
- Brand Word: XXX
```

Then proceed to Phase 2 immediately — no user confirmation needed.

### Phase 2: 11-Column Content Generation

Load `references/rules.md` for per-language character limits, writing conventions, and structural rules before generating content.

Generate all 10 columns in the `| Section | Content |` table format. Each column must be independently usable.

🔴 **Output Language Constraint**: All column headers, labels, and UI-facing template text in the output file must be rendered in the target language matching the user's input. The English labels and templates shown in this skill file are for structural reference only. When generating content for Chinese pages (zh), output Chinese headers; for Japanese pages (ja), output Japanese headers. Match the language the user used in their request.

#### Column Structure Overview

1. **Column 1: Hero + TDK** — TDK summary table (in target language)
2. **Column 2: H1 + Description + Button + Image** — Left-right layout, text left, image right (1200×630)
3. **Column 3: Product Introduction** — H2 introducing the tool, body paragraph
4. **Column 4: Recommendation** — H2 with core keyword, body paragraph
5. **Column 5: Pain Points** — H2, body paragraph reflecting real user pain points
6. **Column 6: Feature Highlights** — 3 highlights with H3 + P each
7. **Column 7: Tutorial** — 3 steps with H3 + P each
8. **Column 8: CTA** — H2, P, button text
9. **Column 9: User Reviews** — 6 reviews
10. **Column 10: FAQ** — 6 Q&A pairs

#### Core Philosophy: One Information Source, Multiple Expressions

🔴 **CRITICAL**: Use English content as the **information source and page structure reference**, but **do NOT translate sentence by sentence**. Localize content according to the target language users' reading habits, search habits, and SEO conventions — keeping core information consistent while making the page read as if written by a native author.

Per hreflang SEO requirements: Google expects hreflang-tagged pages to share **equivalent product facts**. Feature points, technical specifications, and core selling points must match the English page; but sentence structure, tone, case-study angles, and CTA style should be independently optimized for the target market.

This means:

- **Information layer consistency**: Product features, technical specifications, and brand core selling points must align with the English page — do not arbitrarily add, remove, or fabricate
- **Expression layer localization**: Sentence structures, tone, pain-point angles, use-case selection, and CTA style should be independently crafted per target language culture
- **Cultural adaptation**: Writing style, sentence structure, and logical flow differ completely by language
  - **Japanese (ja)**: Use desu/masu form (です・ます調) throughout; logical flow: conclusion → reason → specific examples; use bullet points (箇条書き) liberally to reduce reading fatigue; polite, professional but not overly salesy tone; gentle CTA guidance
  - **Chinese (zh)**: Concise and direct, hitting pain points head-on; prefer short sentences (15–25 characters), parallel structures, affirmative statements; natural and compelling like a friend recommending a tool
- **Structure preservation**: Keep the overall page structure (H1, H2, FAQ, CTA) consistent to facilitate multilingual version maintenance
- **Search-engine-friendly + human-readable**: Satisfy local search engine ranking preferences while keeping the reading experience smooth and natural for real users

For detailed per-language writing rules, load `references/rules.md`.

#### Localization Writing Rules

1. **Preserve page structure**
   - Keep the overall structure of H1, H2, FAQ, CTA, etc. consistent to facilitate multilingual version maintenance.

2. **Do not translate sentence by sentence**
   - You may adjust word order, sentence patterns, and paragraph flow as long as core information remains unchanged.

3. **Localize keywords**
   - Use search terms more common in the target language instead of copying English keywords directly.
   - Distribute keywords naturally; avoid keyword stuffing; align with local user search habits.

4. **Write like a native speaker**
   - Use wording, tone, and expressions natural to local users, making content read like original writing, not a translation.
   - Avoid preserving English sentence patterns and expression logic.

5. **Adapt examples and CTAs appropriately**
   - CTAs, case studies, and feature descriptions may be optimized for target language expression conventions, but must not alter product features or factual information.

6. **Keep brand information consistent**
   - Product names, brand names, feature details, data points, and core selling points must remain consistent — do not arbitrarily add, remove, or fabricate content.

7. **Overall principle**
   - The final output should read like an SEO page written specifically for the target language market, not a translated version of an English page. Ensure content is natural, fluent, aligned with local search habits, and possesses good SEO readability and originality.

#### Output Rules

1. **Write ALL content to a single `.md` file** — do NOT output inline in chat
2. File naming: `SEO-[keyword]-[brand]-[lang].md` (e.g. `SEO-ai-image-enhancer-YourBrand-ja.md`)
3. All 10 columns use `| Section | Content |` table format (headers in target language per the Output Language Constraint above)
4. Save to the current workspace directory
5. **Output file contains only the 10 content columns** — do NOT include Schema Markup or verification report

#### Verification

Verify character counts internally with Python `len()` before writing the output file. Do NOT include the verification report in the output.

#### Brand Word Rules

- Brand word appears exactly **10 times** across all content
- Verify with Python `count()` internally before finalizing

