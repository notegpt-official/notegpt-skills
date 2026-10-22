# Outline, Style, And Sample

Read this first to confirm presentation settings, and before writing or updating `outline.md`, using files from `references/`, or generating/approving the sample slide.

Apply the mandatory-confirmation, explicit-waiver, and verified-reference sample exception rules in `workflow-gates-and-progress.md` to every approval below.

## First Confirm Style, Audience, Scenario, Tone, And Slide Count

Before source preparation or outlining, resolve these settings together:

- Visual style: a built-in direction or user-provided visual reference.
- Audience: for example, students, teachers, or colleagues; include age or expertise when relevant.
- Scenario: for example, teaching slides, a picture book, a work summary, or a business report.
- Tone: for example, neutral, friendly, professional, educational, technical, or academic.
- Slide count: total slides, including the cover and closing; suggest a suitable count when unspecified and confirm it with the other unresolved settings. Keep the outline and final deck at that count unless the user approves a change.

Reuse explicitly specified values and settings clearly inferable from the user's request without asking again. Briefly state inferred settings without claiming user approval; ask only about missing or ambiguous values in one grouped question, preferably using an available built-in question tool, suggesting a suitable combination rather than separate confirmation rounds. Wait for the user's choices unless confirmation is explicitly waived; when waived, choose suitable defaults and state the assumptions. If all settings are explicit or clearly inferable, briefly restate them and continue without waiting. Record the resolved settings in `outline.md` once the project exists; use them to guide content depth, vocabulary, examples, layouts, and speaker notes. Carry audience, scenario, and tone into `deck_spec.json` under `deck_context` for slide-job generation.

If the user has already specified a style, provided a style image, or provided a PDF/PPT/PPTX to use as style reference, do not force a 2-3 option style selection. Extract and briefly restate its rules. References resolve style only: do not infer audience, scenario, tone, or slide count from reference content, appearance, or image/page count. Resolve those settings from the user's written instructions or ask about them before source preparation and outlining; a visual reference does not skip the initial settings gate.

For PDF/PPT/PPTX style references, do not infer the visual system from document structure, outline text, XML, file metadata, or slide object hierarchy alone. First render or export representative pages/slides into real page images, inspect those rendered images, and derive the style from what is actually visible on the pages. If the file has multiple visual sections, inspect enough representative pages to capture the shared style and any section-specific variations.

When extracting style from reference material, separate content reuse from style reuse. Unless the user explicitly asks to reuse the source content, treat the provided image/PDF/PPT/PPTX as a style reference only.

If the user has not provided a clear style, prefer a multiple-choice question: offer 2-3 concrete style directions and mark one as your recommendation. Each style option should briefly specify:

- Color palette
- Layout system
- Typography direction
- Illustration or image treatment
- Decorative elements
- Density and whitespace rules

After the user chooses a style, create one final style direction and keep the visual identity consistent across all slide prompts. Keep color palette, typography, texture, icon/illustration language, and overall mood stable. Do not reuse the same layout on every page.

Reusable style references come only from the skill's built-in `references/` directory, listed below. User-provided visual directions and images/PDF/PPT/PPTX may be used as references for the current deck.

Use style references as inspiration, not as rigid templates. Adapt the style to the topic and audience.

Important: a deck should have one coherent visual identity, not one repeated composition. Treat each reference as a style system: stable palette, typography, icon language, texture, and visual mood; variable page layout chosen from the slide's content role. `layout_blueprints` are candidate starting points only. Do not apply the same blueprint to every slide.

Available built-in references:

- `references/clean-professional.md`
- `references/creative-magazine.md`
- `references/e-ink-magazine.md`
- `references/data-dashboard.md`
- `references/research-defense.md`
- `references/retro-flat-illustration.md`
- `references/hand-drawn-technical-explainer.md`
- `references/hand-drawn-whiteboard.md`
- `references/warm-handcrafted.md`
- `references/mckinsey-style.md`
- `references/government-red.md`
- `references/teaching-courseware.md`


Example combined confirmation (adapt to the request and omit questions already answered):

```text
I recommend a clean, professional work summary for colleagues, using light backgrounds, blue-green accents, and clear structure; please confirm or adjust the settings below, or provide another combination or visual reference.

- Style: Clean Professional (recommended), Creative Magazine, or Data Dashboard?
- Audience: students, teachers, or colleagues? Suggested: colleagues.
- Scenario: teaching slides, picture book, work summary, or business report? Suggested: work summary.
- Tone: neutral, friendly, professional, educational, technical, or academic? Suggested: professional.
- Slide count: 8, 12, 16, or another total? Suggested: 12 slides including cover and closing.
```

## Plan The Deck Outline

After the initial settings gate, create a concise `outline.md` draft using the confirmed style, audience, scenario, tone, and slide count. Record those settings at the top. For each slide, define:

- Slide number
- Slide title
- 3-5 key points
- Optional visual idea
- Layout role and intent, such as cover, agenda, section divider, concept explanation, process, comparison, timeline, data evidence, architecture, case study, summary, or Q&A
- Required source images, if any, including the image path or attachment name, its role on the slide, and whether it is a strict input asset or only a style/layout reference

Save the draft to `{base_dir}/{deck_name}/outline.md` once the project directory is known. If the output directory is not known yet, show the outline in chat first and write it to `outline.md` immediately after creating the project directory.

For the user-facing outline, group content by slide number in a clear format suited to the content, showing each slide's title and all text intended to appear in the PPT, including subtitles, body text, labels, captions, chart/table text, and footers where applicable. Keep the presentation concise through formatting, not by summarizing or omitting slide text. Speaker notes and internal layout or generation instructions are excluded.

Show the outline and request confirmation, preferably using an available built-in question tool, then wait for approval before image generation, unless the user explicitly asked you to skip confirmation. If any slide lists required source images, explicitly ask the user to verify that each image is assigned to the correct slide and role before generation. If the user requests changes, update `outline.md` and ask for confirmation again.

Unless the user explicitly waived outline confirmation, stop after writing the outline draft. At this point, report the `outline.md` path, slide count, required source images and their slide mapping, and that no slide images or PPTX have been generated yet. Do not proceed to backend selection or sample generation until the outline gate is satisfied. Final `deck_spec.json`, `speech.md`, and full-deck prompt preparation must also wait for the sample gate.

If the user approved a sample slide, record that approved `slide_XX.png` path as the deck-level style reference. Later slide prompts and main-agent generation calls should include it as a style-only reference so each page keeps the same palette, typography mood, density, texture, and visual identity without copying the sample's exact layout.

Recommended structure:

```text
Slide 1: Cover
Slide 2: Context / problem
Slide 3-7: Main argument or sections
Slide 8: Summary / recommendation / closing
```

For slides that use source images, add lines like:

```markdown
Slide 5: Experiment Results
- Key points: ...
- Required images:
  - Main evidence figure; strict input asset; preserve data, axes, labels, legends, colors, and values

    ![Result 01](assets/figures/result_01.png)

  - Supporting model architecture; strict input asset; preserve labels and arrows

    ![Model Architecture](assets/figures/model_architecture.png)
```

Use Markdown image syntax inside the `Required images` list whenever the asset is local and renderable in the outline. This lets the user visually verify the exact asset mapping during outline review. Keep the descriptive text next to each image so `prepare_slide_prompts.py` can convert the same asset into structured prompt input later.

## Generate One Sample Slide For Approval

After the outline and style are approved and the image backend is selected, generate exactly one sample slide image before full production.

Compose its prompt directly from the confirmed outline, style, and required references. Do not create full-deck jobs or run `prepare_slide_prompts.py` for the sample; prepare those jobs only after the sample gate is satisfied and its actual generation method and style reference are recorded.

Sample slide requirements:

- Use the confirmed style description.
- Prefer a representative content slide over the cover when possible.
- Demonstrate the intended deck rhythm: the sample should show how the chosen style adapts to a real content page, not just a generic fixed template.
- Save it directly as the intended final slide filename, such as `{base_dir}/{deck_name}/origin_image/slide_08.png`. In CLI/API mode, generate a candidate outside `origin_image/`, inspect it, then copy the chosen sample to that exact path.
- Show the sample inline using Markdown image syntax, such as `![Sample slide](image_path_or_url)`, with a user-accessible image path or URL; do not substitute a plain Markdown link. Show it even when sample confirmation is waived or the verified-reference exception applies.
- Compare the sample visually with any user-provided style reference image: check palette, typography hierarchy, density and whitespace, texture, and illustration/icon treatment. Match the visual identity while allowing a layout appropriate to the sample content. Also perform normal text, content, and required-asset QA. If the style matches and QA passes, show the sample, briefly report the match, record the reference path and comparison result in `outline.md`, and continue without asking for sample confirmation. A reference image existing or appearing in the prompt is insufficient evidence. If the match is uncertain or inconsistent, ask the user to confirm or adjust the visual style, typography, layout density, and text quality.

When sample confirmation is required, prefer an available built-in question tool after displaying the image. Do not generate the full deck until the user approves the sample slide or explicitly waives sample confirmation, or the verified-reference exception above is satisfied. Even with confirmation skipped, generate and inspect the sample first. If the user requests changes, revise the style description and regenerate that same `slide_XX.png` file first. Once approved, keep that file as the final slide for its page. Do not create `sample_slide.png` in `origin_image/`, because the assembly step is designed around final `slide_XX` filenames.

After the sample slide is approved, record the sample generation method in `deck_spec.json` before preparing full-deck jobs. This records provenance and the backend/visual settings to reuse. Generation and editing modes may differ when required by reference images or repairs. Include at least:

- `backend_used`: the selected backend label, such as `built-in image tool` or `scripts/image_gen.py`.
- `tool_name`: the actual tool or command used, such as `image_gen`, `image_generate`, or `scripts/image_gen.py`.
- `mode`: `generate` or `edit`.
- `prompt_source`: where the approved sample prompt came from.
- `size`, `quality`, and model/config details when the backend exposes them.
- `approved_sample_path`: the approved `origin_image/slide_XX.png` path.
- `input_context_preparation`: how local source/style images were made available, such as `view_image` for built-in mode.
- `execution_rule`: the main agent must retain the selected backend and visual settings, selecting generation or editing as needed; report a blocker if the required capability is unavailable.

Before preparing jobs, set `approved_style_reference` to an object with the approved sample `path` and a style-only role. Verify its final image exists; subsequent generation skips that page based on image existence.

A sample image existing means it was generated, not that the user approved it. Wait for sample approval before preparing full-deck jobs or launching batches, unless the sample has passed inspection and either confirmation was explicitly waived or the verified-reference exception above is satisfied. Image-based task completion does not replace this approval gate.
