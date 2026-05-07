---
name: wechat-literature-article
description: Generate Chinese WeChat Official Account publishing packages and optional browser-assisted draft creation for the 生信探癌 account from biomedical literature PDFs. Always use read-literature-pdf first to produce a deep Markdown reading report from PDFs, then rewrite that Markdown into a WeChat article with HTML, metadata, cancer/technology classification, topic tags, figure notes, AI scientific infographic prompts, and pre-publication checks. Use when the user asks for 公众号推文, 微信推文, 生信探癌文章, 文献解读推文, or WeChat draft publishing from a paper PDF or Markdown report.
---

# Wechat Literature Article

## Goal

Produce a WeChat Official Account publishing package for `生信探癌` from a biomedical paper PDF or an existing literature-reading Markdown report. The package should read like a professional Chinese WeChat article for bioinformatics and oncology researchers, not like a formal group-meeting report. It should use a public-facing research narrative: research background -> samples and methods -> conclusion walkthrough -> bioinformatics highlights -> summary.

For PDFs, this skill is explicitly a downstream layer of `$read-literature-pdf`: first create the full Markdown reading report, then rewrite that Markdown into the WeChat article. Do not skip the Markdown reading report and draft directly from raw PDF text unless the user explicitly asks for a fast rough preview.

This skill may help with browser-assisted draft creation only after the publishing package is generated. It must create or prepare a draft only; it must not mass-send, publish, or make irreversible account changes without explicit user confirmation.

When the user explicitly authorizes the whole draft workflow for the current turn, such as `下面所有问题都允许`, `直接帮我做到草稿`, or `我都允许`, treat draft-saving operations as approved for that turn. This approval still does **not** include publishing, mass-sending, changing account settings, changing credentials, or deleting existing materials.

## Inputs

- **PDF input**: Always first use or follow `$read-literature-pdf` to create a deep Chinese literature-reading Markdown report with figure screenshots. The WeChat article must be based on that Markdown report, not on a shallow PDF extraction.
- **Markdown input**: Treat the Markdown as the source report and rewrite it directly into the WeChat article package.
- **Mixed input**: Prefer facts from the PDF/report. Do not invent paper metadata, sample sizes, methods, results, author information, or impact factor values.

If the source is incomplete, mark missing values as `原文未明确说明`.

## Output Package

Create a stable output folder near the input, such as `<paper-stem>_wechat/`, containing:

- `article.md`: WeChat article body in Markdown.
- `wechat.html`: WeChat-editor-friendly HTML generated from `article.md`.
- `metadata.json`: title candidates, summary, cover text, paper facts, classification, tags, and publishing notes.
- `image_manifest.csv`: original figures, AI figures, locations, usage purpose, source/copyright notes, and review status.
- `ai_image_prompts.md`: AI cover and scientific schematic prompts.
- `review_checklist.md`: manual checks before pasting or uploading to WeChat.

Use `scripts/build_wechat_package.py` after drafting `article.md` to generate or refresh support files:

```bash
python /path/to/wechat-literature-article/scripts/build_wechat_package.py article.md --out article_wechat
```

## Article Workflow

1. If the source is a PDF, run the `$read-literature-pdf` workflow first and create a folder such as `<pdf-stem>_reading/` with a final Markdown report and figure assets. The report must contain enough content to support a public-facing article: paper facts, study design, Results-by-heading interpretation, figure/module explanations, conclusions, limitations, and reusable analysis ideas.
2. Read the Markdown report and extract the title, journal, publication date, DOI, cancer type, technology methods, model system, core result, all Result sections, all figure assets, and reusable analysis ideas.
   - Build a Result-to-figure map before drafting.
   - Images must come from Markdown image paths already present in the `$read-literature-pdf` report, especially `figures/` or legacy `figures_panel_modules/`.
   - Do not use PDF page screenshots or whole-page Figure files to satisfy Result image requirements.
3. Decide the article type:
   - `文献解读`: paper interpretation.
   - `技术教程`: method/tutorial article.
   - `数据库工具`: database or software article.
   - `热点综述`: broader field review.
4. Build the classification metadata using the rules below.
5. Draft `article.md` using `references/article-template.md` when useful. Use a WeChat narrative structure: `研究背景 -> 样本与方法 -> 结论详解 -> 生信方法看点 -> 小结 -> 原文引用与图源说明`.
6. Keep the text lively and readable, but keep every scientific claim traceable to the Markdown reading report.
7. Add original paper figure modules from the reading report for multi-image explanation. Every Result or `结论详解` module in the article must include at least one original paper panel/module image from the source Markdown. Cite each original figure in `image_manifest.csv`.
8. Add AI scientific infographic prompts for the cover and explanatory schematics. AI figures must be marked as schematics, not paper data.
9. Generate the package files with `scripts/build_wechat_package.py`.
10. Run the quality checklist before final delivery.

## Default Article Structure

Use this structure unless the user asks for a different format:

1. 3-5 title candidates. Prefer the style `期刊 | 技术亮点 + 癌种/疾病 + 核心机制轴`, for example `Cancer Discovery | 单细胞测序绘制膀胱癌免疫全景图：SPP1+ 巨噬细胞-IL6-CRP 轴主导免疫逃逸`.
2. Opening hook: 1-2 paragraphs explaining what problem the paper solves and why it matters.
3. Paper information card: title, journal, date, DOI, disease/cancer type, major technologies.
4. One-sentence takeaway.
5. `研究背景`: disease scenario, unresolved question, and why this paper is worth reading.
6. `样本与方法`: cohorts, sample types, sequencing/assay technologies, and validation strategy.
7. `结论详解`: reorganize the source report into a WeChat reading path. Do not mechanically preserve every Results heading if it hurts readability, but do not lose Result-to-figure correspondence.
8. `生信方法看点`: emphasize scRNA-seq, spatial transcriptomics, multi-omics, cell-cell communication, trajectory, CNV, AI/ML, signature, databases, or tools when relevant.
9. `小结`: summarize the mechanism axis, reusable analysis ideas, limitations, and project inspiration.
10. References and image source statement.

## Result-Figure Matching Rule

This is mandatory for public WeChat literature articles.

- Every Result or `结论详解` module must include at least one original paper data figure.
- The image must be a local panel/module crop already referenced in the `$read-literature-pdf` Markdown report, usually under `figures/` or legacy `figures_panel_modules/`.
- AI schematics can help explain mechanisms, but they do **not** satisfy the required original data figure for a Result module.
- Do not use whole-page PDF screenshots, full-page Figure screenshots, or filenames like `page_003.png`, `Figure_1_full.png`, `Figure_2_page_5.png`, or similar as Result images.
- Each Result image must be followed by both:
  - `**图示解读：** ...`
  - `**图源说明：** 原文 Figure/panel，仅用于文献解读，请发布前确认版权/转载要求。`
- If a Result module has no usable image in the source Markdown, do not silently omit the figure. Insert the exact warning:

  ```markdown
  > 该 Result 缺少可用局部图块，需回到 read-literature-pdf 阶段补图。
  ```

  Then list the missing Result title and the expected Figure/panel if known. Do not invent a chart or use a whole-page screenshot to fill the gap.

Before drafting, make a compact Result-to-figure map:

```text
Result module title | source Markdown heading | figure path | Figure/panel label | usable? yes/no
```

Use this map to ensure every public-facing Result module has figure evidence.

## Classification Rules

Default publishing classification is **one primary collection plus 3-5 topic tags**.

### Primary Collection

Use cancer-first classification:

- If one clear cancer type is central, use that cancer collection.
- If the paper is pan-cancer, tumor microenvironment general, or covers many tumors without a single dominant cancer, use `泛癌与肿瘤微环境`.
- If it is a pure method/tutorial/tool article without a dominant cancer, use a technology collection.
- If uncertain, use `其他肿瘤` for tumor articles and explain the uncertainty in `publish_notes`.

Cancer collections:

- `泛癌与肿瘤微环境`
- `肺癌`
- `乳腺癌`
- `肝癌`
- `胃癌/食管癌`
- `结直肠癌`
- `胰腺癌`
- `泌尿男生殖肿瘤`
- `妇科肿瘤`
- `血液肿瘤`
- `脑胶质瘤/神经肿瘤`
- `黑色素瘤`
- `其他肿瘤`

Technology collections:

- `单细胞组学`
- `空间组学`
- `多组学整合`
- `免疫治疗与 TME`
- `AI/机器学习`
- `数据库与工具`
- `生信教程`

### Topic Tags

Generate 3-5 concise topic tags. Prefer a mix of:

- cancer type: `肺癌`, `肝癌`, `泛癌`, `肿瘤微环境`
- technology: `单细胞测序`, `空间转录组`, `CellChat`, `CNV`, `机器学习`
- disease mechanism or scenario: `免疫治疗`, `转移`, `耐药`, `预后模型`
- article type: `文献解读`, `生信教程`, `数据库工具`

Do not generate more than 5 topic tags unless the user explicitly asks. WeChat backend rules may change, so keep tags as metadata suggestions rather than hard guarantees.

## Image Rules

### Original Paper Figures

- Use original paper figure crops for data interpretation when the source report includes them.
- Prefer multi-image explanation for key figures; do not rely on whole-page figures.
- For Result modules, original paper figure crops are mandatory and must come from the source Markdown report.
- For each original figure, record:
  - local path
  - source paper and Figure/panel label
  - intended article section or Result module
  - usage note, such as `原文数据图，仅用于文献解读，请发布前确认版权/转载要求`

### AI Scientific Infographics

Use AI-generated images as explanatory aids, especially:

- cover image
- study design schematic
- analysis workflow schematic
- mechanism model schematic
- cell-cell interaction or tumor microenvironment concept image

Rules:

- Base prompts only on facts extracted from the paper or source report.
- Do not invent sample sizes, pathways, genes, cell types, treatment outcomes, or statistical conclusions.
- Do not recreate or imitate the original paper figures.
- Use clean scientific infographic style suitable for WeChat and biomedical readers.
- Add captions beginning with `**AI 示意图说明：** 本图为根据原文信息生成的辅助示意图，不是原文数据图。`

When the active runtime has an image generation tool and the user asks for actual images, generate them and save them under `figures/` or `ai_images/`. Otherwise, create `ai_image_prompts.md` so the user or a later agent can generate them.

See `references/ai-image-guide.md` for prompt patterns.

## WeChat Publishing Notes

- Do not store or reuse WeChat backend URLs that contain session token query parameters.
- For browser automation, prefer `https://mp.weixin.qq.com/` and rely on the user's browser login state. If the user provides a current backend URL containing a session token, it may be opened transiently in the browser for that session, but never save it to `metadata.json`, Markdown, scripts, references, logs, or other persistent files.
- For future API automation, read AppID/AppSecret from environment variables or an uncommitted local config. Never write credentials into skill files or article packages.
- Automation should create drafts by default. Any mass-send or publish action must require explicit human confirmation.

## Browser/Computer-Assisted Draft Workflow

Use this workflow only after the publishing package exists and the user asks to open WeChat or create a draft.

### Tool Preference

1. Prefer Chrome DevTools MCP when it is available and configured to attach to the user's current stable Chrome session. This is the best route for WeChat because it can reuse login state, cookies, open tabs, and the user's existing browser profile.
2. If Chrome DevTools MCP is not available, try the Browser Use plugin/in-app browser when it can access `mp.weixin.qq.com` with the needed login state.
3. If Browser Use cannot navigate to or control WeChat Official Account pages, and the current session exposes Computer Use or desktop-control tools, use Computer Use to operate the user's real browser.
4. If none of these tools is available, do not pretend the draft was created. Report the blocker and leave the package ready for manual paste or API automation.

### Chrome DevTools MCP Requirements

When Chrome DevTools MCP tools are exposed, use them as the primary WeChat automation route.

1. Verify that the MCP is attached to the user's real Chrome before editing:
   - call the page-list tool;
   - confirm that existing real tabs are visible, such as WeChat backend tabs, user browsing tabs, bookmarks, or already-open pages;
   - avoid treating a newly launched blank browser as success.
2. Prefer the official `chrome-devtools-mcp` server in `autoConnect` mode targeting stable Chrome. Do not rely on a persistent `browserUrl=http://127.0.0.1:9222` or `browserUrl=http://localhost:9222` configuration as the final setup for this skill.
3. If the MCP configuration was just changed, remind the user that Codex usually needs a restart before new MCP tools appear. After restart, re-check that existing Chrome tabs are visible.
4. Select an existing WeChat page when one is already open. Otherwise navigate to `https://mp.weixin.qq.com/` and rely on the user's current Chrome login state.
5. Never store tokenized WeChat backend URLs. A URL containing `token=` may be opened transiently only for the active browser session.

### Navigation And Login

1. Navigate to `https://mp.weixin.qq.com/`, or transiently to the user's current backend URL if they provided one in the same request. Do not persist any URL containing a session token.
2. If using Computer Use, open or focus the user's browser and navigate there through the address bar. Do not inspect browser internals or bypass browser security warnings.
3. If the page requires login, QR scan, CAPTCHA, or account selection, pause and ask the user to complete it. Do not solve CAPTCHA or enter passwords/verification codes unless the user has explicitly provided and authorized that exact action.
4. After login, verify that the visible account is `生信探癌` or ask the user to confirm before creating a draft.

### Draft Creation Entry

1. From the home page, enter the article creation flow. Look for Chinese UI labels such as `新的创作`, `图文消息`, `文章`, `发表`, `草稿箱`, `新的图文`, `新建图文`, or `写新文章`.
2. In the current WeChat backend UI, a common path is:
   - home page card `新的创作`
   - click `文章`
   - wait for the article editor with placeholders like `请在这里输入标题`, `请输入作者`, and `从这里开始写正文`
3. If a draft editor is already open, reuse it only if it is blank or clearly belongs to the current task. Do not overwrite unrelated user drafts without explicit confirmation.

### Field Mapping

Fill fields from the package:

   - title: `metadata.json -> selected_title`
   - author/account: `生信探癌` unless the backend already sets it
   - digest/summary: `metadata.json -> summary`
   - body: paste/copy content from `wechat.html` or `article.md`, preserving images where possible
   - primary collection/topic: `metadata.json -> primary_collection`
   - topic tags: `metadata.json -> topic_tags`
   - original declaration: set to `原创` / `文字原创` when the article is rewritten by 生信探癌 and the user asks for original declaration
   - original article/source URL: prefer DOI URL, PubMed URL, publisher URL, or paper landing page from `metadata.json`
   - creation source: use a transparent source note, for example `基于原文文献解读与 AI 辅助整理，结合生信探癌原创分析撰写`
   - cover: upload an AI-generated cover image from `image_manifest.csv` or `ai_images/`, preferably a visually attractive biomedical schematic related to the paper

### Robust Editor Filling

WeChat's editor is a web app and its DOM may change. Use visible UI controls first. If direct typing/pasting fails, use controlled DOM updates and verify by snapshot.

1. Fill the title and author fields through visible editable placeholders when possible.
2. For the body, prefer inserting sanitized HTML generated from `wechat.html`. If the editor rejects direct paste, set the editor's rich-text container content and dispatch input/change/composition events so the word count updates.
3. After filling the body, verify that:
   - the left preview card title changed;
   - the editor word count is greater than 0;
   - the first paragraph and at least one section heading are visible.
4. Keep the article concise enough for WeChat reading. If the source Markdown is long, draft a polished public-facing version rather than dumping the full literature report.
5. Never insert fabricated data tables, fake charts, or invented paper figures.

### Image Upload And Placement

Images are required for this account's literature articles unless the user explicitly asks for text only.

1. Use `image_manifest.csv` to decide what to upload:
   - `cover`: AI cover image, attractive and related to the paper topic.
   - `body`: AI workflow/mechanism schematic and selected original figures when copyright review allows.
   - `placeholder`: prompts or missing images that should not be uploaded yet.
2. Original paper figures:
   - upload only local figure files that exist;
   - caption them as original paper data figures;
   - include paper/Figure label and copyright review note.
3. AI figures:
   - upload the generated PNG/JPEG files;
   - caption every AI figure as `AI 生成示意图`;
   - never present AI figures as original experimental data.
4. If a top-toolbar image upload inserts a body image but disrupts the current article body, capture the uploaded WeChat image URL, then restore the full article body and embed that URL in the correct section.
5. After upload, verify that image elements are visible in the editor, not merely listed in local files.

### Cover, Original, Source, And Article Settings

Before saving the draft, complete the article settings panel as far as the current WeChat UI allows.

1. Cover:
   - upload the AI cover image if a cover picker or `编辑封面` dialog is available;
   - crop/confirm the cover when WeChat requires it;
   - if cover upload fails because the UI blocks automation, leave the cover file ready and report it explicitly.
2. Original:
   - when the user asks for original declaration and the text is rewritten by 生信探癌, enable `原创` / `文字原创`;
   - set author to `生信探癌` when requested;
   - do not enable settings that create unrelated account changes.
3. Original/source link:
   - add the DOI or publisher URL when available;
   - if WeChat requires a specific URL format, prefer the DOI URL form such as `https://doi.org/<doi>`.
4. Creation source:
   - if the UI asks for a source, use a transparent statement such as `基于原文文献解读与 AI 辅助整理，结合生信探癌原创分析撰写`;
   - do not imply endorsement by the original authors or journal.
5. Digest/summary:
   - fill the article summary from `metadata.json`;
   - keep it readable and below WeChat's current character limit.
6. Collection and topic tags:
   - set the primary collection and 3-5 topic tags when the UI exposes these fields;
   - if the backend requires manual choice from existing collections, choose the closest existing collection and report any mismatch.

### Save Draft And Verify

1. If the user has not already approved saving a draft for the current turn, ask before clicking `保存为草稿`, `保存`, or equivalent controls.
2. If the user explicitly approved the whole workflow for the current turn, save the draft without asking again.
3. Click only draft-saving controls. Avoid buttons labeled `发表`, `发布`, `群发`, `群发给订阅用户`, `群发确认`, `免费发布`, or irreversible confirmation dialogs.
4. After saving, verify success by one or more of:
   - WeChat shows a saved timestamp/history version;
   - a success toast appears;
   - the draft remains in the editor with the filled title/body;
   - the draft list/history shows the new draft.
5. Report the exact status:
   - draft saved or not saved;
   - title used;
   - body image count visible in the editor;
   - cover status;
   - original/source/creation-source status;
   - any manual review still needed.

### API Draft Route For Later Automation

The API route is a future automation path and should not be silently used unless the user has configured official account API credentials.

1. Read AppID/AppSecret/access token only from environment variables or an uncommitted local secret file.
2. Upload permanent or draft media according to the current WeChat Official Account API requirements.
3. Create a draft in the official account draft box by API.
4. Default to creating a draft only. Do not mass-send by API.
5. Record API response IDs in a local, non-tokenized run log only when the user asks for logs.

## Quality Checklist

Before finalizing:

- The article has title candidates, opening hook, paper card, core takeaway, result walkthrough, method highlights, project inspiration, and source statement.
- Missing facts are marked `原文未明确说明`.
- Cancer type, technology tags, primary collection, and 3-5 topic tags are present in `metadata.json`.
- Original paper figures are listed in `image_manifest.csv` with source and review notes.
- AI images/prompts are clearly marked as schematics and do not imply they are original data.
- `wechat.html` renders the article with headings, paragraphs, blockquotes, lists, tables, and images suitable for copy-paste into a WeChat editor.
- No WeChat backend token URL or credential is stored in any output file.

## Resources

- `references/style-guide.md`: default voice, title style, section rhythm, terminology, and image captions for 生信探癌.
- `references/article-template.md`: reusable WeChat article skeleton.
- `references/ai-image-guide.md`: AI cover and schematic prompt templates.
- `scripts/build_wechat_package.py`: builds or refreshes the publication package support files from `article.md`.
