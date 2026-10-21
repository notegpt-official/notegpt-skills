# Workflow Gates And Progress

Read this before creating downstream artifacts, advancing between phases, or reporting progress.

## Mandatory Phase Gates

Confirmation is mandatory by default. Only an explicit user request to skip a specific gate or all confirmations waives confirmation; silence or a general deck-creation request is not a waiver. A clearly specified visual style needs no separate style-selection confirmation. Record waivers in `outline.md` without claiming user approval. A waiver skips waiting, not the underlying work: still generate and inspect one representative sample before full production. Sample-only exception: when the user supplies a style reference image and visual comparison verifies the sample matches its visual identity and passes normal sample QA, continue without asking for sample confirmation. If the match is uncertain or inconsistent, request confirmation. Record the reference path and comparison result in `outline.md`, without claiming user approval. Throughout this skill, a gate is satisfied by user approval, an explicit waiver covering that gate, or this verified-reference exception for the sample; references to approval below follow this rule. Retain the inspected sample method and style reference in the existing specification fields even when confirmation is waived.

User approval is required for the outline, visual style (unless already specified), and sample slide, unless explicitly waived or the sample meets the verified-reference exception above. Source preparation, backend selection, and execution steps do not require separate approval.

Phase order:

1. Source reading and asset extraction
2. Outline confirmation
3. Visual style confirmation
4. Automatic image backend selection (prefer built-in; no user confirmation)
5. One sample slide approval
6. Full slide generation
7. QA, speaker notes finalization, and PPT assembly

Hard rules:

- If a built-in image generation tool is available, select it directly without reading `backend-selection.md`, `cli-api-fallback.md`, or `image-model-configuration.md`. Otherwise read all three, then select the backend. No user confirmation is required.

- Before outline approval, do not create final `deck_spec.json`, `speech.md`, prompt job files, slide images, or `.pptx` files.
- If you need an internal planning artifact before approval, name it with `.draft.` such as `deck_spec.draft.json` or `speech.draft.md`, and clearly report that it is not final.
- Downstream artifacts (`deck_spec.json`, `prompts/`, `speech.md`, final slide images, and `.pptx`) should be created only after the relevant gates have been approved.
- If the deck uses required source images, stop at outline confirmation and ask the user to verify the slide-to-image mapping before style selection or image generation.

## Visible Progress Plan

For non-trivial decks, keep a user-visible checklist with one active step:

1. Prepare source, outline, style, and backend decisions.
2. Generate and approve one sample slide.
3. Prepare slide prompts.
4. Generate images in batches in the main agent (up to 6 concurrent calls).
5. Save generated slide images.
6. QA, repair, notes, and PPT assembly.

Completion evidence:

- `Prepare source, outline, style, and backend decisions`: `outline.md` is approved and image backend is selected.
- `Generate and approve one sample slide`: one final `origin_image/slide_XX.png` has passed inspection and user approval, or inspection with an explicit sample-confirmation waiver or verified reference-image match recorded in `outline.md`. File existence alone does not satisfy this gate.
- `Prepare slide prompts`: `prompts/slide_XX.json` exists for each expected slide.
- `Generate images in batches in the main agent (up to 6 concurrent calls)`: the main agent directly executes batches of at most 6 concurrent image calls, with one slide per call and no subagent dispatch. Each batch is checked and saved before the next begins.
- `Save generated slide images`: each selected generated image exists at its expected `origin_image/slide_XX.png` path. File existence is the only per-slide task-state criterion.
- `QA, repair, notes, and PPT assembly`: every expected final image exists, QA is complete, `speech.md` is final, and `{deck_name}.pptx` exists.

Do not mark a step complete just because the chat says it is complete; use real output files.
