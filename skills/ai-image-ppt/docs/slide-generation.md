# Main-Agent Slide Generation

Read this before full-deck image generation, preparing slide jobs, saving final images, or handling blockers.

## Final Slide Image Generation

Generate one image per slide with the selected image backend. Every final `slide_XX.png` must be produced by the built-in image tool or by `scripts/image_gen.py`; programmatic rendering or hybrid text overlay is not acceptable for slide image creation.

After the outline, visual-style, and sample gates are satisfied (approval, explicit user waiver, or verified reference-image match for the sample gate) and the image backend is automatically selected and fixed, create final downstream artifacts if they do not already exist:

- `deck_spec.json`
- `prompts/slide_XX.json`
- `speech.md`

Do not create these final downstream artifacts before outline approval. If the user explicitly asks for pre-approval planning files, use `.draft.` filenames and synchronize them after approval.

`deck_spec.json` must include `sample_generation_method` copied from the approved sample before `prepare_slide_prompts.py` is run. The helper copies that method into each `prompts/slide_XX.json`, so the main agent can retain the selected backend and visual settings used for the sample. Choose generation or editing mode according to required input images and repair needs; the recorded sample mode is provenance, not a mandatory mode for later calls.

Before full production, create structured per-slide image jobs. Prefer the bundled deterministic helper:

```bash
~/.image-ppt-skill/.venv/bin/python {skill_root}/scripts/prepare_slide_prompts.py \
  --spec {base_dir}/{deck_name}/deck_spec.json \
  --out-dir {base_dir}/{deck_name} \
  --selected-backend "<selected backend label>"
```

The helper writes `prompts/slide_XX.json` for every slide and creates `origin_image/` if needed. It does not generate images or maintain task-state files.

If a spec example is needed, run `~/.image-ppt-skill/.venv/bin/python {skill_root}/scripts/prepare_slide_prompts.py --write-template /existing/scratch/directory/deck_spec.example.json`. This writes an example only; replace its example values before use.

Each `prompts/slide_XX.json` is a self-contained slide job. It includes the slide number, title, output filename, input image list, whether context images are required, and the full prompt text. Use these JSON job files for built-in image generation, CLI/API fallback coordination, and main-agent execution. Do not create a separate task-state manifest.

Save all necessary context in each job so it remains reproducible without implicit conversation references.

For any slide that depends on cross-slide or source-wide meaning, write the necessary background directly into `deck_spec.json` before preparing prompts:

- Use deck-level `deck_context` for canonical concepts that multiple slides may need, such as the source summary, core claim, term list, taxonomy, characters, definitions, chronology, or required naming.
- Use slide-level `local_context` for page-specific facts that must be visible to that page, such as "summarize these six traits", "compare these two methods", "continue this three-step framework", or "use this exact quote".
- Expand references like "the six traits", "the above framework", "the previous conclusion", or "these examples" into explicit lists or definitions inside `deck_context` or `local_context`. Avoid leaving them as implicit pointers.


`deck_spec.json` may express `required_images` either as structured objects or as Markdown image reference strings. The helper extracts the image path from strings such as `strict input asset\n\n![Result 01](assets/figures/result_01.png)` and carries the surrounding text / alt text into the image role.

Use a structured visual brief for each slide. Image generation works best when the prompt separates canvas, style, layout, text, visual elements, and constraints instead of relying only on a long style paragraph.

Keep the deck visually coherent but vary slide layouts according to page semantics. Treat style references and `layout_blueprints` as candidate patterns, not fixed templates. Across a normal deck, deliberately mix suitable page types such as:

- cover / section divider
- context or problem framing
- process or timeline
- comparison or tradeoff
- data / evidence / KPI
- architecture or workflow diagram
- summary / conclusion / next steps

Avoid generating every slide as the same three-card layout. For each slide, choose a layout that fits its content and explain that choice in the `layout.intent` field.

```json
{
  "type": "16:9 full-slide PowerPoint image",
  "language": "Chinese",
  "canvas": {
    "aspect_ratio": "16:9",
    "use_full_canvas": true,
    "slide_number": "do not render a slide number"
  },
  "style": {
    "name": "{confirmed style name}",
    "visual_direction": "{same final style description for every slide}",
    "color_palette": "{main colors and accent colors}",
    "typography": "{font personality, hierarchy, weight, text alignment}",
    "texture_and_finish": "{flat, paper, dashboard, editorial, whiteboard, etc.}",
    "deck_consistency": "same palette, typography, icon language, texture, and mood across all slides"
  },
  "deck_context": {
    "source_summary": "{brief source-wide summary}",
    "core_claim": "{the deck's central thesis}",
    "canonical_terms": ["{term 1}", "{term 2}", "{term 3}"]
  },
  "layout": {
    "role": "{cover, agenda, section divider, concept, process, comparison, timeline, data evidence, architecture, case study, summary, Q&A, etc.}",
    "intent": "{why this page uses this layout: cover, comparison, timeline, data evidence, workflow, summary, etc.}",
    "composition": "{specific layout for this slide}",
    "content_zones": "{title zone, body zone, visual zone, footer or callout zones}",
    "variation_rule": "same style identity as the deck, but vary composition by slide role; do not repeat the same blueprint on adjacent slides unless the content is part of a deliberate repeated sequence",
    "relationship_to_previous_slide": "{new layout, continuation layout, mirrored layout, or deliberate repeated sequence}",
    "spacing": "clear hierarchy, coherent alignment, no overlapping elements"
  },
  "text": {
    "title": "{slide title}",
    "key_points": ["{point 1}", "{point 2}", "{point 3}"],
    "text_quality": "render all Chinese text exactly, clearly, and without garbled characters"
  },
  "local_context": {
    "required_background": "{facts, lists, definitions, comparisons, or prior-slide references this slide needs to be self-contained}"
  },
  "visual_elements": {
    "main_visual": "{icons, diagram, chart, illustration, dashboard cards, collage, or other content-specific visual idea}",
    "supporting_elements": "{arrows, cards, callouts, decorative elements, labels}"
  },
  "constraints": [
    "The final image itself must contain the title and key points.",
    "All text must be readable and correctly spelled.",
    "Keep the confirmed style consistent with the rest of the deck.",
    "No watermark, no unrelated logo, no extra slide number."
  ]
}
```

If preparing prompts manually instead of using `prepare_slide_prompts.py`, still save each full slide job under `{base_dir}/{deck_name}/prompts/slide_XX.json` before generation. The saved job must include `prompt`, `out`, and `input_images`, including any deck-level approved sample slide style reference and all slide-level source images with explicit role labels.

## Batched Main-Agent Generation

After sample approval, derive expected image filenames from the slide numbers in `deck_spec.json`. An expected `origin_image/slide_XX.png` file existing means that page was generated successfully; absence means it still needs generation. There are no other task states or state files.

1. Skip existing final images, including the approved sample, unless the user requests a revision or QA identifies a problem.
2. Select up to 6 missing pages per batch. Read their prompt jobs and inspect required local images. Attach the approved sample for style only and required source assets as strict inputs.
3. Call the selected image backend directly in the main agent, one page per call, with at most 6 concurrent calls. Use smaller batches or serial calls when parallel execution is unavailable. Generation/editing mode may vary with image inputs and repair needs.
4. Inspect candidates, then save or copy the selected images to their exact final paths. Keep drafts, failed outputs, and references outside `origin_image/`. Do not create placeholder final files.
5. Wait for all calls and image saving in the current batch before starting the next. Retry failed pages by checking for missing final images; no status reset or result-recording command is needed. Report failures and reasons directly to the user.

For revisions, generate and inspect a replacement outside `origin_image/`, then replace the existing final image only after validation. Image existence determines generation success; visual QA is a separate check, not another task status.

## Pre-Assembly Check

Check each expected filename, not just the image count. Every expected image must exist, and no unexpected final slide images should remain in `origin_image/`. Use zero-padded slide numbers such as `slide_01.png`; file order does not depend on generation completion order.

Use deck-level `aspect_ratio` (default `16:9`) consistently in prompts, image dimensions, style canvas rules, and assembly. For Chinese decks, require accurate readable Chinese text.

Each job's `out` is a filename relative to the project's `origin_image/` directory, not relative to `prompts/`. Read the job's `prompt` field for the image model; do not send the entire job JSON as prompt text.
