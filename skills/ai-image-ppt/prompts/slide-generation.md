# Main-Agent Slide Generation Checklist

- Compare slide numbers in `deck_spec.json` with `origin_image/slide_XX.png`. Existing final image means generated successfully; missing image means generate it. No task-state files are used.
- Reuse existing images, especially the approved sample, unless revision is requested or QA requires repair.
- Read up to 6 missing-page prompt jobs per batch. Follow the selected backend and approved visual settings; inspect and attach required input images.
- Call the image tool directly, one slide per call, with at most 6 concurrent calls including retries and repairs. Do not delegate.
- Inspect candidates, then save or copy selected images into their exact final paths. Keep drafts and failed outputs elsewhere.
- Finish the current batch before starting another. Report failures and retry missing images after resolving the cause; no state-reset command is needed.
- For revisions, validate the replacement before overwriting the final image. Before assembly, check that every expected filename exists and no unexpected slides remain.
