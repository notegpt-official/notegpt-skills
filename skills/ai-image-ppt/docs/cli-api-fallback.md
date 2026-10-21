# CLI/API Fallback

Read this reference when no built-in image generation tool is available, before selecting the fallback backend. The main `SKILL.md` owns the backend decision rules; this document owns fallback commands, runtime setup, image-input limits, editing, transparency, and troubleshooting.

Let `{skill_root}` mean the directory containing `SKILL.md`.

## Runtime Setup

CLI/API fallback commands use the shared runtime environment. Before running `scripts/assemble_ppt.py` or fallback image commands, make sure the shared runtime exists. If `~/.image-ppt-skill/.venv/bin/python` is missing, or if importing script dependencies fails, create or refresh the environment:

```bash
python3 {skill_root}/scripts/image_ppt_runtime.py bootstrap
```

This is an internal setup step for the skill. Do not ask the user to run it unless dependency installation fails and user approval or troubleshooting is required.

The fallback CLI loads `~/.image-ppt-skill/.env` automatically for `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `IMAGE_PPT_IMAGE_MODEL`. Do not manually parse `.env`. Read `image-model-configuration.md` together with this file when no built-in image generation tool is available. Reading the configuration guide does not require inspecting secrets or asking for configuration unless needed.

## Generate One Slide

Generate candidates outside `origin_image/` (create `drafts/` when needed). Inspect the output, then copy the chosen image to its final `origin_image/slide_XX.png` path. A failed or rejected candidate must not create a final image. For an approved-sample revision, validate the replacement before overwriting the existing final image.

Basic generation command:

```bash
~/.image-ppt-skill/.venv/bin/python {skill_root}/scripts/image_gen.py generate \
  --model gpt-image-2.5-flare \
  --prompt-file {prompt_file} \
  --size 2560x1440 \
  --quality medium \
  --out {base_dir}/{deck_name}/drafts/slide_01_candidate.png
```

The fallback CLI defaults to `gpt-image-2.5-flare`. Select `--model gpt-image-2.5-sunburst` for Sunburst. It also accepts provider-prefixed names and older GPT Image models; verify provider support before using a model.

When generating from saved `prompts/slide_XX.json` files, use the job's `prompt` field only when the job does not require input images:

```bash
python3 -c 'import json, pathlib; print(json.loads(pathlib.Path("{base_dir}/{deck_name}/prompts/slide_01.json").read_text())["prompt"])' | \
~/.image-ppt-skill/.venv/bin/python {skill_root}/scripts/image_gen.py generate \
  --prompt-file - \
  --size 2560x1440 \
  --quality medium \
  --out {base_dir}/{deck_name}/drafts/slide_01_candidate.png
```

Before using this text-only `generate` path, inspect the assigned `prompts/slide_XX.json`. If `input_images` is non-empty or `requires_context_images` is true, this command is not sufficient because it does not attach those images. Use a selected backend/path that can pass the required images, such as the built-in image tool with the images visible in context or a CLI/API edit/image-input path that supplies every required source image. If no such path is available, stop and report the missing capability; select a compatible backend before production, or report a blocker if the backend was already fixed. Do not generate a text-only replacement for a strict input asset.

## Capabilities And Sizes

The fallback CLI supports:

- `generate`: create one or more images from a prompt.
- `edit`: edit one or more existing images, optionally with a mask.

The fallback CLI defaults to 2K 16:9 landscape output, `2560x1440`, with `medium` quality. GPT Image 2.5 also supports `xhigh` and `max`; older models retain their existing quality limits. For 4K landscape slides, use `--size 3840x2160 --quality high` only when the user asks for 4K, text-heavy slides need sharper output, or the default result is blurry. For portrait assets, use `--size 2160x3840` only if the user requests portrait output. For GPT Image 2.5, output above `2560x1440` pixels is experimental; inspect the actual size and visual quality.

## Editing Slides

If a slide is mostly correct but has a localized issue, use the selected backend's edit capability when available. In CLI/API fallback mode:

```bash
~/.image-ppt-skill/.venv/bin/python {skill_root}/scripts/image_gen.py edit \
  --image {slide_path} \
  --prompt {edit_prompt} \
  --out {new_slide_path}
```

Replace the final slide only after validating the edited output.

## Transparent Backgrounds

Transparent-background requests:

- GPT Image 2.5 Flare and Sunburst support `--background transparent --output-format png` (or `webp`) through compatible APIs. JPEG cannot preserve transparency. The current AtlasCloud adapter does not forward `background` and accepts only PNG/JPEG; do not promise native transparency through that adapter.
- `gpt-image-2` does not support native transparent backgrounds; GPT Image 1 / 1.5 do. Preserve the selected model unless a switch has been agreed.
- In built-in mode, use native transparency if the tool supports it; otherwise use a flat chroma-key background and `scripts/remove_chroma_key.py` when appropriate.

## Assembly And Doctor

`assemble_ppt.py` supports `16:9` (default), `4:3`, `1:1`, `3:4`, `9:16`, and `21:9`. Pass the deck specification's `aspect_ratio` to assembly and use the same ratio in prompts and image dimensions.

Run the API doctor only when troubleshooting fallback API access:

```bash
python3 {skill_root}/scripts/image_ppt_runtime.py doctor --check-api
```
