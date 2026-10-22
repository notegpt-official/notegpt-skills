# Research Defense

**Use Cases:**
- Research project proposal defenses
- Grant applications and major research program reports
- Midterm reviews and final project evaluations
- Thesis proposals, preliminary defenses, and final defenses
- Work-package breakdowns, technical roadmaps, research foundations, risk analysis, and expected outcomes
- Formal reports for universities, research institutes, laboratories, and industry-academia projects

**GPT-Image-2 Style Brief:**
```json
{
  "type": "16:9 full-slide PowerPoint image",
  "style_name": "Research Defense",
  "best_for": "Formal academic settings such as research proposals, grant defenses, midterm reviews, final project evaluations, thesis defenses, and laboratory progress reports",
  "visual_direction": "formal Chinese academic research defense deck, authoritative but adaptable project presentation, evidence-driven layout, structured scientific diagrams, concise conclusions, and disciplined visual hierarchy",
  "canvas": {
    "aspect_ratio": "16:9",
    "background": "clean white #FFFFFF with subtle light gray #F5F7FA content background",
    "composition": "structured academic slide with title area, evidence area, explanatory diagrams, tables, callouts, or conclusion area chosen according to slide content",
    "density": "medium-high to high information density, suitable for serious academic defense, while keeping clear reading order and alignment"
  },
  "color_palette": {
    "primary": "deep academic blue #003F8F or #004A9F",
    "secondary": "research blue #0B5CAD and pale blue #EAF2FF",
    "accent": "formal red #B5121B or #C00000 used sparingly for key conclusions, risks, breakthroughs, and emphasized phrases",
    "neutral": "black #111111, dark gray #333333, light border gray #D8DEE8, pale table fill #F3F6FA",
    "optional": "muted gold #F3DFA2 only for cover or major title emphasis",
    "rule": "prefer blue for structure and red for critical arguments, but adapt emphasis to the topic and source material; avoid colorful decorative palettes, heavy gradients, playful icons, and casual illustration styles"
  },
  "typography": {
    "title": "bold Chinese sans-serif, large, formal, report-like, left aligned",
    "section_labels": "white bold Chinese text on deep blue blocks or arrow labels",
    "body": "dense but readable Chinese sans-serif, mostly black, key phrases in red bold",
    "tables": "compact academic table typography with clear header rows and restrained category emphasis",
    "text_quality": "Chinese text must be exact, readable, non-garbled, and suitable for formal research defense"
  },
  "page_system": {
    "header": "usually use a clear title area with optional section number and optional project/institution mark; cover pages and divider pages may use a different composition",
    "divider": "optional thin horizontal rule, blue segment, or subtle academic separator when it helps hierarchy",
    "body": "structured content area with light borders, module labels, evidence cards, diagrams, or tables as needed",
    "footer": "optional one-sentence takeaway strip or conclusion line when the slide needs a strong final claim",
    "logo_rule": "use only user-provided logos or a neutral text placeholder such as Project Identifier; do not invent real institution logos or unrelated brand names"
  },
  "layout_patterns": [
    "research background with literature timeline, policy/report evidence, and problem statement",
    "research status with left-side evidence collage and right-side challenge comparison",
    "topic decomposition with multi-column task chain and right-side vertical research path",
    "research content page with three evidence cards and supporting mechanism images",
    "core objective page with arrow label, large target sentence, technical route, and mechanism diagram",
    "platform support page with equipment photos, prior achievements, certificates, and bullet evidence",
    "risk analysis four-quadrant grid with risk type, risk judgment, mitigation evidence, and bottom conclusion",
    "expected outcomes table with category, measurable indicators, and assessment method"
  ],
  "layout_usage_rule": "Use these patterns as flexible starting points, not mandatory templates. Keep the deck's academic tone, disciplined hierarchy, restrained palette, and evidence-first logic, while adapting the body layout to each slide's role and source material.",
  "layout_blueprints": [
    {
      "name": "Research Background / Current State of Research",
      "sections": [
        {"position": "top", "count": 1, "labels": ["one-sentence problem or status statement with optional emphasized phrases"]},
        {"position": "left large area", "count": 1, "labels": ["literature timeline / technical evolution / evidence collage"]},
        {"position": "right column", "count": 1, "labels": ["report evidence / industry challenge / application pain point"]},
        {"position": "bottom", "count": 1, "labels": ["optional takeaway conclusion"]}
      ]
    },
    {
      "name": "Work-Package Breakdown / Technical Roadmap",
      "sections": [
        {"position": "top", "count": 1, "labels": ["project objective sentence"]},
        {"position": "middle", "count": 3, "labels": ["Work Package 1", "Work Package 2", "Work Package 3"]},
        {"position": "left side", "count": 2, "labels": ["Application-Oriented Basic Research", "Core Content of Key Tasks"]},
        {"position": "right side", "count": 4, "labels": ["Performance Research", "Application Validation", "In-Depth Exploration", "Relationship Analysis"]},
        {"position": "bottom", "count": 1, "labels": ["chain-summary sentence"]}
      ]
    },
    {
      "name": "Core Objectives / Research Objectives",
      "sections": [
        {"position": "top-left", "count": 1, "labels": ["blue arrow label: Core Objectives or Research Objectives"]},
        {"position": "top-right", "count": 1, "labels": ["target sentence with key phrases"]},
        {"position": "middle", "count": 2, "labels": ["content detail box 1", "content detail box 2"]},
        {"position": "bottom", "count": 3, "labels": ["method diagram", "mechanism image", "application validation image"]},
        {"position": "bottom-center", "count": 1, "labels": ["technical route statement"]}
      ]
    },
    {
      "name": "Research Content / Evidence Presentation",
      "sections": [
        {"position": "top", "count": 1, "labels": ["research content sentence with key variables"]},
        {"position": "middle", "count": 3, "labels": ["Research Area 1", "Research Area 2", "Research Area 3"]},
        {"position": "inside each card", "count": 3, "labels": ["blue title bar", "scientific figure or chart", "short evidence caption"]},
        {"position": "bottom", "count": 1, "labels": ["integrated conclusion or mechanism statement"]}
      ]
    },
    {
      "name": "Risk Analysis",
      "sections": [
        {"position": "top", "count": 1, "labels": ["risk control thesis statement"]},
        {"position": "middle grid", "count": 4, "labels": ["Technical Risk", "Safety Risk", "Performance Risk", "Management Risk"]},
        {"position": "bottom", "count": 1, "labels": ["supporting scientific images and final conclusion"]}
      ]
    },
    {
      "name": "Expected Outcomes / Evaluation Metrics",
      "sections": [
        {"position": "top", "count": 3, "labels": ["High Value", "Full Coverage", "Measurable"]},
        {"position": "middle", "count": 1, "labels": ["large table: Category / Specific Metric / Evaluation Method"]},
        {"position": "left table column", "count": 4, "labels": ["Theoretical Innovation and Intellectual Property", "Technical Breakthroughs and Materials Development", "Talent Development and Academic Impact", "Long-Term Development Potential"]}
      ]
    }
  ],
  "visual_elements": {
    "allowed": "academic tables, blue arrow labels, restrained red emphasis text, flow arrows, technical route diagrams, paper figure collages, mechanism diagrams, laboratory or equipment photos, certificates, report thumbnails, structured grids, light shadows",
    "avoid": "minimalist empty pages, marketing hero layouts, cartoon illustrations, decorative gradients, random icons, playful stickers, excessive whitespace, vague stock photos, fruits, animals, people cutouts, unrelated decorative objects"
  },
  "writing_style": {
    "sentence_patterns": [
      "Systematically investigate ... and reveal the mechanism of ...",
      "Build a ... system to achieve precise control of ...",
      "Establish a complete closed-loop research chain around ...",
      "Validate the performance of ... through ...",
      "Effectively avoid or mitigate the risk of ...",
      "Define specific, measurable metrics for every outcome"
    ],
    "emphasis_rule": "Use red bold text selectively for the scientific problem, key breakthrough, risk judgment, measurable outcome, or page-level conclusion; do not over-highlight every sentence."
  },
  "rendering_constraints": [
    "The slide must look like a serious Chinese academic research defense deck, not a commercial pitch deck.",
    "Keep a recognizable academic presentation system across slides, but do not force every page into the same header or grid.",
    "Every page should have a clear top-to-bottom or left-to-right reading order.",
    "Use high-density scientific content, but keep text blocks aligned and readable.",
    "Use blue structural labels and red conclusion phrases when useful, without making the page mechanically blue-red.",
    "Do not include fruit, people, animals, random objects, fictional brand marks, or unrelated decorative icons.",
    "No watermark, no unrelated logo, no fake real institution logo, no extra slide number unless requested."
  ]
}
```
