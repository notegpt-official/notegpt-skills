# SEO Page Image Prompt Templates

Templates are loose guidelines — adapt freely to the specific product and scenario. The goal is clear communication, not rigid formatting.

---

## Common Style Rules (apply to all types)

- **Language**: All text must be English. Audience is English-speaking (US/Europe). Only the BEFORE/input side may show its original content in any language — everything else (AFTER content, badges, UI labels, descriptions, selling points) must be in English.
- Light, clean, modern AI SaaS website aesthetic
- Background: white, light gray, light beige, or soft gradients — never dark or highly saturated
- Brand color used as accent (UI elements, highlights, icons), not as dominant background
- Realistic product photography and functional demos, not abstract AI concept art
- No heavy text walls — let the visuals do the talking

---

## 1. Banner (Hero Image)

**Dimensions**: 16:9
**Method**: Image-to-image (use logo as reference/base)
**Must contain**: Logo, website URL (main domain, e.g. `https://your-domain.com/`), feature name, core effect showcase

**Preferred layout** — left/right split:

```
┌─────────────────────────────────────────────────────┐
│  [Logo] Brand Name                                  │
│                                                     │
│  Feature Name (large headline)                      │
│  Short description (1-2 lines)                      │
│  Core value proposition (1 line)                    │
│                                                     │
│  [icon] Selling point 1    [icon] Selling point 2   │
│  [icon] Selling point 3                             │
│                                                     │
│  [URL bar] https://your-domain.com/                   │
├─────────────────────────────────────────────────────┤
│  [BEFORE badge]      →      [AFTER badge]           │
│  [Product image      arrow  [Product image           │
│   in source language]  →    in target language]     │
│  [Product card details]     [Product card details]   │
└─────────────────────────────────────────────────────┘
```

- **Left column**: Logo at top → feature name as headline → short description → 2-3 selling points with icons → URL bar at bottom
- **Right column**: Before/After product images (e.g. product card with original language → same card with translated language), connected by an arrow
- Use rounded card shadows for the product images, dashed arc arrow for the Before→After flow
- Selling point icons in soft brand-color circles
- White or very light background with subtle gradient

**Prompt direction**:

```
A 16:9 hero banner for an AI SaaS website, split left-right layout.

LEFT COLUMN (text and branding):
- Top: [Brand Logo] + brand name
- Large headline: "[FEATURE NAME]" (bold, dark text with brand-color accent on key word)
- 1-2 line description: "[SHORT DESCRIPTION]"
- Value proposition: "[VALUE PROP]"
- 2-3 selling point icons in soft brand-color circles with short labels
- Bottom: rounded URL bar showing [MAIN DOMAIN URL]

RIGHT COLUMN (product demo):
- Two product cards side by side with rounded corners and soft shadows
- Left card: "BEFORE" badge + [ORIGINAL PRODUCT IMAGE in source language]
- Right card: "AFTER" badge + [SAME PRODUCT IMAGE translated to target language]
- Dashed arc arrow connecting Before to After

Overall style: light, minimal, premium AI SaaS aesthetic. White/very light background with subtle gradient. Professional, clean typography.
```

**Before/After on right side**: Show a real product card (e.g. e-commerce listing) in original language, arrow pointing to the same card with text translated. Use "BEFORE"/"AFTER" badges.

---

## 2. Product Introduction (What Is It)

**Dimensions**: 1:1
**Method**: Text-to-image
**Goal**: Explain what the product is and how it works.
**No brand elements**: No logo, no brand name, no URL — keep it purely about the function.
**Style**: Minimal, low information density. One clear visual message per image.

**Prompt direction**:

```
A clean 1:1 image showing [INPUT] → [OUTPUT] transformation.
Minimal composition: just the two states side by side with a subtle arrow.
No logos, no brand text, no extra UI elements — only the core transformation.
Light background, soft shadows, generous whitespace.
Simple, elegant, instantly understandable at a glance.
```


---

## 3. Why Choose (Recommendation)

**Dimensions**: 1:1
**Method**: Text-to-image
**Goal**: Show why users prefer this tool over alternatives.
**No brand elements**: No logo, no brand name, no URL.
**Style**: Minimal, low information density. One core comparison per image (e.g. speed OR cost OR quality — not all at once).

**Prompt direction**:

```
A clean 1:1 comparison image: traditional way vs AI way for [TASK].
Pick ONE key differentiator to highlight (e.g. time saved, cost reduced, or quality improved).
Simple side-by-side or before/after layout with minimal text labels.
No logos, no brand elements — just the clear contrast.
Light background, soft colors, generous whitespace.
The viewer should understand the advantage in one second.
```


---

## 4. Pain Points (Problem → Solution)

**Dimensions**: 1:1
**Method**: Text-to-image
**Goal**: Show user frustrations before the product, then the AI solution after.
**No brand elements**: No logo, no brand name, no URL.
**Style**: Minimal, low information density. One pain point per image, one clear solution.

**Prompt direction**:

```
A clean 1:1 problem-to-solution image for [TARGET USER].
Before: one specific frustration (e.g. spending hours on repetitive manual work that the AI tool solves).
After: the same task done effortlessly by AI.
Keep it simple — one pain point, one solution, minimal text.
No logos, no brand elements. Light background, soft muted tones on the "before" side, subtle accent on the "after" side.
Emotionally relatable — the viewer should think "that's exactly my problem."
```

