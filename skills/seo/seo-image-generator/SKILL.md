---
name: seo-image-generator
description: "Generate visual asset prompts for SEO landing pages — banner (16:9, image-to-image with logo), product introduction (1:1), why choose (1:1), and pain points (1:1). Then optionally execute batch generation via image generation service. This skill should be used after page-seo-generator produces the 11-column SEO content, to create matching visual materials for the page."
agent_created: true
---

# SEO Page Image Generator

Generate 4 types of visual assets for SEO landing pages — prompt writing and optional batch execution. Think of it as the visual counterpart to page-seo-generator: that skill produces the words, this one produces the pictures.

## When to Use

- A new SEO page has been generated (via page-seo-generator or page-seo-generator-i18n) and needs visual materials
- User asks for "SEO images", "page images", "banner image", or similar
- User wants to supplement an existing page with Before/After demo images

## Image Types (4 Kinds)

| # | Type | Ratio | Method | Must-Have Elements | Brand Elements |
|---|------|-------|--------|--------------------|----------------|
| 1 | Banner | 16:9 | **Image-to-image** | Logo, URL, feature name, core effect demo | ✅ Logo + URL + brand name |
| 2 | Product Intro | 1:1 | Text-to-image | Input → Output flow, what it does | ❌ No logo/brand/URL |
| 3 | Why Choose | 1:1 | Text-to-image | Traditional vs AI comparison, value props | ❌ No logo/brand/URL |
| 4 | Pain Points | 1:1 | Text-to-image | Problem → Solution, emotional resonance | ❌ No logo/brand/URL |

**Brand rule**: Only Banner includes brand elements (logo, URL, brand name). Types 2-4 should be minimal, low information density, focused on one clear core value per image — no logo, no brand name, no URL.

The key distinction between #3 and #4:
- **Why Choose**: Rational. Traditional way (slow, expensive) vs AI way (fast, affordable). Uses icons, process diagrams, cost comparisons. Think "logical persuasion."
- **Pain Points**: Emotional. The user's real frustration (tedious manual work, missed deadlines) → the relief AI provides. Think "emotional connection."

## Overall Visual Direction

- **Language**: All text on every image must be in **English**. Audience is English-speaking (US/Europe). The BEFORE/input side may show its original content in any language. AFTER side and ALL UI elements, badges, labels, and descriptions must be in English.
- **Tone**: Light, clean, modern — like a high-end AI SaaS landing page (think Stripe, Linear, Vercel)
- **Background**: White, light gray, light beige, or soft gradients. No dark or over-saturated backgrounds.
- **Brand accent**: Use brand color sparingly — UI highlights, small accents, icon fills. Not as dominant background.
- **Content priority**: Show the product working. Before/After, input/output, real scenarios. Not abstract AI concept art. Not generic stock photos. Not text-heavy slides.
- **One-glance comprehension**: Someone scrolling fast should understand what this AI tool does without reading a word.

## Core Feature Demonstration Principles (All Types)

**Every image must use the product's core feature Before/After as its visual foundation, then layer the message points on top.**

In other words: whether it's product introduction, why choose us, or pain points, **the actual effect demonstration of the core feature never disappears**. Before/After is the main visual subject; everything else is just seasoning:

- To express **speed** → add a small clock icon next to the Before/After
- To express **low cost** → add a price tag or savings badge
- To express **scale** → show multiple images being processed simultaneously
- To express **pain points** → first show the result after the feature solves the problem, then use expression/mood changes to convey the before/after emotional shift

**Wrong approach**: Pure abstract comparison (e.g., a clock on the left and a clock on the right), where you can't see what the product actually does.

**Right approach**: A product image translated into multiple languages (feature demonstration), with a small "5 sec" badge floating on top (expressing speed).

## ⚠️ Required Inputs (Collect First)

**Before starting any image generation**, you MUST collect the following information from the user:

1. **Brand Name** — the product/company brand name (e.g. "YourBrand")
2. **Website URL** — the main domain URL that will appear on Banner images (e.g. `https://your-domain.com/`)
3. **Logo Image** — Banner generation requires the logo as reference image (will be uploaded to image generation service)

**Do NOT proceed with prompt writing or image generation until all 3 items are collected.**

Ask in one message:
> "To generate SEO images for your page, I need:
> 1. Your brand name
> 2. Your website URL (main domain)
> 3. Your logo image (for Banner)
>
> Please provide these before I start."

Once collected, proceed to the Workflow below.

## Workflow

**Language rule for user-facing questions**: All guide questions in the steps below should be asked in the same language the user is communicating in. If the user writes in Chinese, ask in Chinese; if in English, ask in English. The example prompts below are in English for reference — adapt accordingly.

### Step 1: Gather Context

Pull from the surrounding conversation or the page-seo-generator output:

- Feature name (e.g. "AI Image Translator")
- Industry / scenario (e.g. "e-commerce, Amazon sellers")
- Target user (e.g. "cross-border e-commerce sellers")
- Brand name (e.g. YourBrand)
- What the tool does (input → output transformation)

If any of these are missing, ask briefly — don't interrogate.

### Step 2: Ask for Visual Direction

Ask the user: "What kind of application scenario should the images lean toward?"

The answer can be as broad as "e-commerce" or as specific as needed. Once you have the scenario direction (e.g. "e-commerce"), freely choose varied product scenes within that domain — skincare, electronics, food packaging, fashion, home goods, etc. Don't make the user specify further. Just use their answer as the scene anchor and populate details yourself.

### Step 3: Ask for Logo and Website URL

Banner is image-to-image — it needs the logo as a reference image. Banner also must display the website URL.

Ask both in one go: "Please share your logo image — the Banner needs it. Which website URL should we use?"

- **Logo**: Accept any format. Once received, upload it to the image generation service via the batch generation workflow and use the returned path as `input_urls` for the banner task.
- **URL**: Always ask — do NOT assume. The URL should be the **main domain** (e.g. `https://your-domain.com/`), not a feature-specific path. Banner shows the main brand domain.

### Step 4: Ask for Quantities

Ask for each type separately (or all at once if the user prefers):

"How many images per type?"

| Type | Suggested default |
|------|-------------------|
| Banner | 1 (one hero image per page) |
| Product Intro | 1-2 |
| Why Choose | 1-2 |
| Pain Points | 1-2 |

User can override freely. No hard rules.

### Step 5: Write Prompts

Write prompts following the loose templates in `references/prompt-templates.md`. These are starting points, not rigid rules — adapt based on the actual product, audience, and scenario.

Key principles when adapting:
- Be specific about what the AI tool does (the transformation, not just a vague "AI improves X")
- Describe what the user sees — left/right split, top/bottom, specific UI elements
- Include visual cues that make the value obvious (e.g. a clock showing "hours → seconds")
- Keep prompts in English for best model compatibility

### Step 6: Execute Image Generation

You can use any image generation tool or skill to generate the images based on the prompts you've written:

- **Banner** (16:9): Requires logo as input for image-to-image generation
- **Other 3 types** (1:1): Pure text-to-image generation
- **Quantity**: Use the quantities specified by the user in Step 4

Generate all image types according to the prompts and specifications defined above.

**Fallback: If no image generation tool or skill is available:**
- Explain to the user that image generation capability is not currently available
- Provide all the image generation prompts you've written, organized by type (Banner, Product Intro, Why Choose, Pain Points)
- Include the technical specifications for each type (dimensions, method, quantity)
- The user can then use these prompts with their preferred external image generation service

### Step 7: Present Results

Output the generated image URLs or files grouped by type (Banner, Product Intro, Why Choose, Pain Points).

## Notes

- Banner is the only image-to-image type. The other three are pure text-to-image.
- Logo upload only needs to happen once per session — reuse for subsequent runs.
- The templates in `references/prompt-templates.md` are suggestions. Feel free to deviate when the product or scenario calls for a different approach.
- This skill focuses on prompt writing. The actual image generation can be done using any image generation tool or service you prefer.
