# read_paper_skills

```
        .--.
       / _  \        PDF
      | (_)  |   +---------+       +----------+
       \__  /    | paper   |  ->  | Markdown |  ->  PPT / WeChat
       / /       +---------+
      /_/          panel crops + AI schematics + journal-club slides
```

`read_paper_skills` is a small skill collection for biomedical paper reading, lab-meeting preparation, and WeChat literature article drafting.

It currently contains three linked workflows:

1. `read-literature-pdf`: read a scientific PDF deeply and generate a structured Chinese Markdown report.
2. `literature-ppt-from-markdown`: convert that Markdown report into an editable Chinese lab-meeting PowerPoint deck.
3. `wechat-literature-article`: convert that Markdown report into a 生信探癌-style WeChat literature article where every Result module has a matching original paper figure crop.

The workflow is designed for biomedical and omics papers, especially papers involving single-cell sequencing, spatial transcriptomics, bulk RNA-seq, WES/WGS, imaging, flow cytometry, animal models, clinical cohorts, and immunology or cancer biology.

## Skills

### `read-literature-pdf`

Turns a paper PDF into a structured Chinese Markdown report with bibliographic metadata, study design, sample tables, method summaries, Results-by-heading interpretation, high-resolution panel/module-level figure screenshots, 1-2 required AI-generated mechanism/method schematics, and reusable analysis ideas.

### `literature-ppt-from-markdown`

Turns the Markdown report into an editable lab-meeting PPT. It uses the report text plus `figures/` and `figures_ai/` assets to create a 15-25 slide journal-club deck with:

- conclusion-style slide titles
- figure-module result explanations
- AI method/mechanism schematic slides
- concise speaker-oriented slide text
- PNG previews for visual QA
- strict checks against whole-page Figure screenshots

### `wechat-literature-article`

Turns the Markdown report into a public-facing Chinese WeChat article for `生信探癌`. It rewrites the group-meeting report into a readable research narrative:

- title candidates in the style `期刊 | 技术亮点 + 癌种/疾病 + 核心机制轴`
- `研究背景 -> 样本与方法 -> 结论详解 -> 生信方法看点 -> 小结`
- every Result/结论详解 module must include at least one original paper panel/module crop from the source Markdown
- AI schematics may help explain mechanisms but cannot replace required Result data figures
- `image_manifest.csv` records Result section, figure path, figure label, and usage status

## Output Style

Generated outputs are written in Chinese and are suitable for:

- journal club
- lab meeting
- paper sharing
- project design reference
- omics-method learning notes
- figure-by-figure paper explanation

The Markdown report usually contains:

```text
1. 文献信息
2. 作者与机构信息
3. 期刊信息与影响因子
4. 研究背景与核心科学问题
5. 样本信息与实验设计
6. 测序与实验方法
7. Results 逐段解析
8. 文章主要结论
9. 文章创新点
10. 文章局限性
11. 对用户课题的启发
12. 可复用的分析方法总结
```

The PPT usually contains:

```text
1. 封面
2. 研究背景
3. 核心科学问题
4. 样本与实验设计
5. 方法 / AI workflow 示意图
6. Results 逐段拆解
7. 机制总结
8. 创新点与局限性
9. 对自己课题的启发
10. 总结页
```

The WeChat article usually contains:

```text
1. 标题候选
2. 开头
3. 论文信息
4. 一句话总结
5. 研究背景
6. 样本与方法
7. 结论详解（每个 Result 必须配原文局部图块）
8. 生信方法看点
9. 小结
10. 参考与图源说明
```

## Cartoon Workflow

```text
       Step 1              Step 2                Step 3
   +------------+      +-------------+      +----------------+
   |  PDF paper | ---> | Read deeply | ---> | Markdown notes |
   +------------+      +-------------+      +----------------+
                                                       |
                                                       v
                                             +----------------+
                                             | PPT / WeChat   |
                                             +----------------+

     page text          Result logic          clean panel crops
     metadata           AI schematic          reusable slides
```

Think of it as a tiny paper-reading helper with a highlighter in one hand, a figure cutter in the other, and a slide remote waiting on the desk.

## Repository Structure

```text
read_paper_skills/
├── SKILL.md                         # read-literature-pdf root skill
├── agents/
├── references/
├── scripts/
├── skills/
│   ├── literature-ppt-from-markdown/
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   └── references/
│   │       └── journal-club-ppt-style.md
│   └── wechat-literature-article/
│       ├── SKILL.md
│       ├── agents/
│       ├── references/
│       └── scripts/
└── README.md
```

### `SKILL.md`

The main skill instructions. Codex reads this file when the skill is invoked. It defines the workflow, extraction rules, Results parsing format, figure-module rules, AI schematic rules, and quality checklist.

### `references/report-template.md`

A detailed Chinese Markdown report skeleton. It is useful when a complete structured report is needed.

### `scripts/pdf_prep.py`

A helper script for PDF preparation:

- extract page-delimited text
- extract metadata
- render pages when PyMuPDF is available
- crop figure regions using normalized coordinates

Recommended report output folders:

```text
paper_reading/
├── literature_reading_report.md
├── figures/       # only local panel/module crops from original paper figures
├── figures_ai/    # 1-2 AI-generated method/mechanism schematics
└── presentation_output/
    ├── paper_title_presentation.pptx
    └── previews/
```

### `skills/literature-ppt-from-markdown`

The second-stage PPT skill. It reads a completed Markdown report and builds an editable PowerPoint deck for lab meeting or journal-club presentation.

It follows these rules:

- default 15-25 slides
- no animation requirement
- one slide, one message
- original paper images only from local panel/module crops
- AI schematics only from `figures_ai/`
- no whole-page Figure or PDF-page screenshots
- render PNG previews and visually inspect before delivery

### `skills/wechat-literature-article`

The public-facing WeChat article skill. It consumes the Markdown report from `read-literature-pdf` and creates a WeChat publishing package:

- `article.md`
- `wechat.html`
- `metadata.json`
- `image_manifest.csv`
- `ai_image_prompts.md`
- `review_checklist.md`

It requires every Result/结论详解 module to include a matching original paper panel/module crop from the source Markdown. If the source Markdown lacks a usable crop, the article must say:

```text
该 Result 缺少可用局部图块，需回到 read-literature-pdf 阶段补图。
```

## Installation

Clone the repository:

```bash
git clone git@github.com:FanFPu/read_paper_skills.git
```

Install the PDF reading skill:

```bash
mkdir -p ~/.codex/skills/read-literature-pdf
cp -R read_paper_skills/SKILL.md \
      read_paper_skills/agents \
      read_paper_skills/references \
      read_paper_skills/scripts \
      ~/.codex/skills/read-literature-pdf/
```

Install the PPT skill:

```bash
mkdir -p ~/.codex/skills/literature-ppt-from-markdown
cp -R read_paper_skills/skills/literature-ppt-from-markdown/* \
      ~/.codex/skills/literature-ppt-from-markdown/
```

Install the WeChat article skill:

```bash
mkdir -p ~/.codex/skills/wechat-literature-article
cp -R read_paper_skills/skills/wechat-literature-article/* \
      ~/.codex/skills/wechat-literature-article/
```

Then invoke them in Codex with:

```text
$read-literature-pdf
$literature-ppt-from-markdown
$wechat-literature-article
```

## Typical Usage

Put a paper PDF in your working folder, then ask Codex:

```text
[$read-literature-pdf] 我现在在这个文件夹下放入了一篇文献，
请帮我生成一版中文 Markdown 文献精读报告。
注意 Results 部分按 figure panel/module 拆开讲解。
```

For a more specific request:

```text
[$read-literature-pdf] 请阅读这篇单细胞肿瘤免疫论文，
输出适合组会汇报的 Markdown。
每个 Results 小节都要说明研究目的、样本、方法、主要结果、
对应 figure panels、图示解读和可借鉴分析思路。
```

After the Markdown report and image folders are ready:

```text
[$literature-ppt-from-markdown] 请根据这个 Markdown 文献精读报告，
做一版 15-25 页的中文组会 PPT。
要求按 Result 逻辑拆页，使用 figures/ 里的局部图块，
使用 figures_ai/ 里的 AI 机制图，不要插入整页 Figure。
```

For older reports that used `figures_panel_modules/`, the PPT skill can treat that folder as the paper-derived panel/module image directory.

To draft a WeChat article from the same reading report:

```text
[$wechat-literature-article] 请根据这个 Markdown 文献精读报告，
写一版生信探癌公众号推文。
要求学习公众号文献解读风格，但保留专业机制分析；
每个 Result/结论详解模块都必须配一张 Markdown 中已有的原文局部图块，
不能用整页 Figure 或 AI 图替代 Result 数据图。
```

## Figure-Module Rule

The skill is intentionally opinionated about figures.

For multi-panel figures, it must never use a whole-page figure as report evidence. Instead, it should crop and explain high-resolution modules such as:

- cohort or study design
- UMAP / atlas construction
- cell proportion or differential abundance
- spatial imaging validation
- clinical cohort validation
- survival or recurrence analysis
- functional assay
- perturbation or treatment response
- final mechanism model

Example:

```markdown
##### 模块 1：样本设计与细胞图谱建立
![Figure 1A-C](figures/Figure_1A_C.png)

**图示解读：**
Figure 1A-C 主要展示……

##### 模块 2：关键细胞状态随疾病进展变化
![Figure 1D-F](figures/Figure_1D_F.png)

**图示解读：**
Figure 1D-F 说明……
```

### Full-page Figure Ban

Whole-page figure screenshots are forbidden in report outputs.

Do not save or reference files like:

```text
Figure_1_full.png
page_003.png
Figure_2_page_5.png
```

Even when the paper has a single-panel figure, crop away page headers, footers, citation strips, journal watermarks, unrelated margins, and neighboring content. Keep only the figure body and the necessary legend or labels.

### Figure Clarity Checklist

Before final delivery, each paper-derived figure crop should pass this check:

- panel letter is visible
- axes and legends are readable
- important statistics and labels are readable
- crop is not blurry or too small
- unrelated page text has been removed
- no whole-page figure appears in Markdown or output folders

## AI Schematic Rule

Every final report must include 1-2 AI-generated schematics for complex methods, experimental design, computational workflow, or biological mechanism. These must be clearly separated from original paper figures.

Allowed schematic types:

- study design
- sequencing workflow
- co-culture assay
- treatment timeline
- computational analysis pipeline
- mechanism model

Required caption:

```markdown
**AI 示意图说明：** 本图为根据原文信息生成的辅助机制/方法示意图，不是原文数据图。
```

If image generation fails or is unavailable, the final report must say why. Mermaid diagrams or text workflows can be added as fallback summaries, but they do not count as the required AI-generated image unless an actual image file is produced.

## PDF Helper Script

Basic text extraction:

```bash
python scripts/pdf_prep.py paper.pdf --out paper_reading --text
```

Render pages when PyMuPDF is installed:

```bash
python scripts/pdf_prep.py paper.pdf --out paper_reading --render-pages 1-3,8,10
```

Crop a figure region using normalized page coordinates:

```bash
python scripts/pdf_prep.py paper.pdf \
  --out paper_reading \
  --crop 5:0.04,0.08,0.96,0.72:Figure_1.png
```

Coordinate format:

```text
PAGE:x0,y0,x1,y1:filename.png
```

All coordinates are normalized from `0` to `1`.

## Quality Principles

This skill should:

- preserve the original Results heading order
- explain findings rather than only translating them
- cite sample sizes and methods when stated
- mark missing details clearly
- avoid fabricating impact factors or sample numbers
- distinguish original data figures from generated schematics
- connect each figure module to a concrete claim
- include 1-2 AI-generated schematics under `figures_ai/`
- exclude whole-page figure screenshots from final outputs
- verify panel/module crops are clear and readable
- end with summary, limitations, and reusable ideas

## Best-Fit Papers

This skill works especially well for papers with:

- single-cell RNA-seq
- spatial transcriptomics
- immune microenvironment profiling
- multi-cohort validation
- animal model perturbation
- cancer progression
- treatment response and resistance
- survival or recurrence cohorts
- complex multi-panel figures

## Notes

The skill is not a citation database and does not automatically guarantee current journal impact factors. If the PDF does not print the impact factor, the report should say:

```text
PDF 中未提供，需外部查询确认。
```

External impact-factor lookup should be done only when requested or when web access is available.

## License

No license has been specified yet.
