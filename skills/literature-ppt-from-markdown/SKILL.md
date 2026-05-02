---
name: literature-ppt-from-markdown
description: Convert a structured Chinese Markdown literature-reading report into an editable lab-meeting PowerPoint deck. Use when the user asks to make a PPT, slides, presentation, 组会汇报, 文献分享 PPT, or journal-club deck from a Markdown report produced by read-literature-pdf, including figure-module layouts, AI mechanism/method schematics, speaker-oriented summaries, slide previews, and visual QA.
---

# Literature PPT From Markdown

Create an editable PowerPoint deck from a structured Markdown literature-reading report. This skill is the second stage after `read-literature-pdf`: Markdown report -> lab-meeting PPT.

Use the built-in Presentations capability for authoring, export, rendering, and QA. If another PPTX reference skill exists locally, treat it only as workflow inspiration; do not copy proprietary skill text, scripts, or licensed assets into outputs or repositories.

## Inputs

Expected working folder:

```text
paper_reading/
├── literature_reading_report.md
├── figures/       # original paper panel/module crops only
└── figures_ai/    # 1-2 AI-generated method/mechanism schematics
```

If the user provides only a Markdown file, infer the figure folders from sibling `figures/` and `figures_ai/` directories. If `figures/` is absent but `figures_panel_modules/` exists, use `figures_panel_modules/` as the paper-derived panel/module folder for compatibility with earlier reports. If images are missing, build the deck text plan and clearly list missing assets before final delivery.

## Output Contract

Produce:

- editable `.pptx`
- PNG previews for visual QA
- a concise final note with the PPTX path, preview path, test/render command, and unresolved issues

Default output folder:

```text
presentation_output/
├── paper_title_presentation.pptx
├── previews/
└── assets/
```

## Deck Defaults

- 16:9 widescreen.
- 15-25 slides for a normal lab meeting.
- No animation or decorative transitions.
- Chinese main text; keep original English terms for key methods, cell types, genes, pathways, and figure labels when useful.
- One slide, one message, one dominant evidence object.
- Figure-heavy, text-light: do not paste Markdown paragraphs into slides.
- Add speaker notes when a result needs detailed explanation that would overcrowd the slide.

## Required Workflow

1. Read the Markdown report and list its major sections: metadata, background, study design, methods, each Result heading, conclusions, limitations, and ideas for the user's project.
2. Inventory image assets under `figures/` or `figures_panel_modules/`, plus `figures_ai/`. Reject whole-page assets by filename or appearance, such as `page_003.png`, `Figure_1_full.png`, or full PDF-page screenshots.
3. Read `references/journal-club-ppt-style.md` for style guidance before writing slide content.
4. Create a slide outline before authoring. Default structure:
   - cover
   - why this paper matters
   - scientific question
   - study design and samples
   - method or AI workflow schematic
   - Results sections, split into 2-4 slides per major Result when needed
   - integrated mechanism or conclusion model
   - innovation and limitations
   - takeaways for the user's project
   - final summary
5. Convert each Result into slide modules by logic, not by figure number alone. Prefer slide titles that state the conclusion, not generic titles like "Result 1".
6. Use paper-derived images only as local panel/module crops from `figures/` or legacy `figures_panel_modules/`. Never insert whole-page figures or full PDF screenshots.
7. Use `figures_ai/` images for method, workflow, or mechanism slides. Label them clearly:

   ```text
   AI 示意图：根据原文信息生成，用于辅助理解；不是原文数据图。
   ```

8. Export the `.pptx`, render PNG previews, and inspect previews before final response.

## Slide Content Rules

### Cover

Include paper title, journal/year if available, presenter/date if known, and a short Chinese subtitle explaining the paper's central question.

### Background

Use 1-2 slides. Explain:

- disease or biological context
- unresolved problem
- why the paper's approach matters

Avoid long literature-review bullets.

### Study Design

Use sample tables, cohort diagrams, or AI workflow schematics. Include patient/sample/cell numbers only when stated in the report. If unknown, write `原文未明确说明` in notes rather than inventing.

### Results

For each major Results heading:

- open with the question the section answers
- use 1-3 key panel/module images
- explain the logic chain: method -> observation -> interpretation -> conclusion
- keep each slide to one claim
- move dense details to speaker notes

Suggested Result slide patterns:

- claim title + large figure crop + 2-3 callouts
- left logic chain + right figure module
- top conclusion + two compared modules
- method mini-diagram + data panel + interpretation
- final mechanism summary using AI schematic plus supporting panels

### Summary

End with:

- 3-5 core findings
- 2-3 innovations
- 2-3 limitations
- practical ideas for the user's project

## Figure Rules

- Only use high-resolution panel/module crops from `figures/` or legacy `figures_panel_modules/`.
- Do not use or save whole-page figure screenshots in the PPT output folder.
- Do not stretch images out of aspect ratio.
- Crop or mask only to improve focus; never remove information needed to interpret the result.
- Keep panel letters, axes, legends, labels, scale bars, and statistical markers readable.
- If a crop is too blurry or small, stop and report that a better crop is needed.

## AI Schematic Rules

- Every final deck must include 1-2 AI-generated schematics from `figures_ai/` when those files exist.
- AI schematics may show study design, sequencing workflow, computational pipeline, co-culture system, treatment timeline, or mechanism model.
- They must be visibly separated from original paper data figures.
- Do not present AI schematics as paper evidence.
- If the Markdown report requires AI schematics but files are missing, state this in the final response and create a placeholder slide only when the user still needs a draft. Do not silently omit the required AI schematic.

## Visual QA

After export, render slide previews and inspect them. The deck is not done until these checks pass:

- no text overlap or clipping
- no image distortion
- no unreadable key labels in figure panels
- no leftover placeholders such as `TODO`, `FIGURE_PLACEHOLDER`, `lorem`, `xxxx`
- no whole-page Figure or full PDF page screenshot
- AI schematic captions are present
- slide density is suitable for live presentation

If any issue is found, revise the deck and re-render affected slides.

## Final Response

Report:

- PPTX path
- preview folder path
- validation/render command used
- whether whole-page figures were absent
- any missing assets or unresolved issues
