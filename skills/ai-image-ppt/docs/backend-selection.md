# Backend Selection

Read this together with `cli-api-fallback.md` and `image-model-configuration.md` only when no built-in image generation tool is available. Otherwise select the built-in tool directly without reading these files.

This skill supports two image backends:

1. Built-in image tool, preferred when available. Example tool names: `image_gen`; OpenClaw `image_generate`.
2. Local API/CLI fallback, using `scripts/image_gen.py`.

## Decision Rules

- Before recommending CLI/API fallback, actively check whether the built-in image generation tool is callable in the current environment. Do not infer availability only from the agent name or subscription context.
- Prefer the built-in image tool when available. In environments exposing `image_gen`, use the built-in `image_gen` tool. In OpenClaw, this may be `image_generate`. Resolution, quality, aspect ratio, or slide-edit requests alone do not require CLI/API fallback. Check which parameters the current tool actually exposes.
- Do not identify the built-in tool as a specific GPT Image model unless the environment provides evidence. If exact model, size, or quality selection is required but the tool does not expose it, explain the limitation rather than silently changing backend. Successful image generation alone does not verify the actual model or requested parameters.
- Select CLI/API fallback directly without a separate approval gate, only when no built-in image generation tool is available.
- Do not recommend CLI/API fallback merely because it provides direct `--out` file paths, easier local file management, local config reuse, batch generation convenience, or simpler automation.
- Before generating the first image, tell the user which tool availability you checked, which backend you plan to use, why fallback is or is not needed, and proceed without asking for backend confirmation. Do not treat being in a specific agent environment as proof that the built-in image tool is available.
- CLI/API fallback loads `~/.image-ppt-skill/.env` automatically. Run the CLI normally; do not manually parse `.env` or ask for configuration before an error.
- Ask for `OPENAI_API_KEY` configuration only after you have intentionally selected CLI/API fallback and that fallback reports missing config, after authentication/base URL/model errors, or when the user explicitly wants to change API settings. Do not mention missing `OPENAI_API_KEY` while the built-in image tool is available. Configure provided values with `scripts/image_ppt_runtime.py config --api-key`.

If CLI/API fallback is selected, read `cli-api-fallback.md` before generating images. Read `image-model-configuration.md` as part of the no-built-in-tool path to understand API key, base URL, model, and `.env` configuration.

Once automatically selected, keep the backend fixed. Choose generation or editing mode according to required input images and repair needs. If the fixed backend lacks a required capability, report a blocker instead of switching backends.

## Report The Selection

Briefly state the selected backend and the reason when helpful, then continue. Do not ask the user to approve the backend. Outline, visual-style, and sample-slide approval requirements remain unchanged.
