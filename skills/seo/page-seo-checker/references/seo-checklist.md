# SEO Compliance Checklist — 12-Point Audit

## Pre-Check: Page Accessibility
- URL must return HTTP 200
- Page must have `<html>` and `<body>` tags
- If unreachable, stop immediately and report error

---

## Check 1: Title Tag (10 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| Title exists | Non-empty `<title>` tag | Missing or empty |
| Char count | 50-60 chars | <50 or >60 |
| Contains brand | Brand name (as specified by user) | No brand mention |
| No banned openings | No "is an AI-powered tool that..." etc. | Banned pattern found |
| Zero article | No "a/an/the AI [tool]" in Title | Article + tool name found |

## Check 2: Meta Description (8 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| Description exists | Non-empty `<meta name="description">` | Missing or empty |
| Char count | 150-160 chars | <150 or >160 |
| Contains keyword | At least 1 core keyword present | No keyword |
| No banned buzzwords | No "revolutionize/game-changer/cutting-edge" | Banned word found |

## Check 3: Canonical Tag (5 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| Canonical exists | `<link rel="canonical">` present | Missing |
| Self-referencing | URL matches current page | Points to different URL |
| HTTPS | Canonical URL uses HTTPS | Uses HTTP |

## Check 4: H-Tag Structure (8 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| Single H1 | Exactly 1 `<h1>` tag | 0 or >1 |
| H1 has brand | H1 contains product/brand name | No brand in H1 |
| H2 for sections | H2 for each of S1-S8 | Missing section H2 |
| No skipped levels | H1 → H2 → H3 sequence | H1 → H3 jump found |
| Sequential | No H3 where H2 needed | Wrong level used |

## Check 5: Body Content — Character Limits (10 pts)
| Section | Expected | Fail Condition |
|---------|----------|---------------|
| S1 What Is P | 200-300 chars | <200 or >300 |
| S2 Pain Point H2 | ≤60 chars | >60 |
| S2 Pain Point P | ≤200 chars | >200 |
| S3 Feature summary P | ≤100 chars | >100 |
| S3 Feature P (each) | ~100 chars | <<80 or >>120 |
| S4 User group P (each) | ≤150 chars | >150 |
| S5 Step P (each) | ~70 chars | <<50 or >>90 |
| S6 CTA P | ≤150 chars | >150 |
| S7 Review P (each) | ≥300 chars | <300 |
| S8 FAQ A (each) | 200-300 chars | <200 or >300 |

## Check 6: Testimonials (5 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| Review count | ≥6 distinct reviews | <6 |
| No banned openings | No "I've been using X for Y months..." | Banned pattern found |
| Arc variety | ≥4 different narrative arcs | <4 arcs |
| Review length | Each ≥300 chars | Any <300 |

## Check 7: FAQ (8 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| FAQ count | ≥10 FAQs | <10 |
| Q1 is overview | "What is [Product] and what makes it different?" | Different question |
| No banned openings | No "Absolutely!" / "Great question!" | Banned pattern found |
| Answer length | Each 200-300 chars | Any outside range |

## Check 8: Image ALT (5 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| All imgs have alt | Every `<img>` has alt attribute | Missing alt on any img |
| Alt non-empty | Alt text >0 chars | Empty alt string |
| Keyword in alt | At least 1 alt contains core keyword | No keyword in any alt |
| Descriptive alt | Alt describes content, not generic | "image" / "photo" as alt |

## Check 9: Internal Links (5 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| Link count | ≥3 internal links | <3 |
| Descriptive anchor | No "click here" / "learn more" anchors | Generic anchor found |
| Links to tool pages | Points to other site tool pages | Only homepage links |

## Check 10: Schema (10 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| JSON-LD exists | At least 1 `<script type="application/ld+json">` | No JSON-LD |
| FAQ schema | FAQPage with all 10 Q&A pairs | Missing or incomplete |
| Valid JSON | No syntax errors in JSON-LD | Parse error |
| Correct @type | Matches content type | Wrong schema type |

## Check 11: Hreflang (5 pts) — Skip for English-only
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| Hreflang exists | `<link rel="alternate" hreflang>` tags | Missing (for localized pages) |
| Includes en | `hreflang="en"` present | Missing English link |
| Includes x-default | `hreflang="x-default"` present | Missing default |
| All language variants | Links for each available language | Missing variant |
| HTTPS URLs | All hreflang URLs use HTTPS | HTTP URLs |

## Check 12: Brand Count & Zero-Article (5 pts)
| Sub-check | Expected | Fail Condition |
|-----------|----------|---------------|
| Brand count | Exactly 10 brand name occurrences (as specified by user) | Not 10 |
| Zero article | No "a/an/the" before tool name | Article violation found |

---

## Scoring Summary
| Category | Threshold | Action |
|----------|-----------|--------|
| ≥80% | Green | Ready to publish |
| 60-79% | Yellow | Fix critical items before publishing |
| <60% | Red | Do NOT publish |
