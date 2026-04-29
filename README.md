# read-literature-pdf

```
        .--.
       / _  \        PDF
      | (_)  |   +---------+
       \__  /    | paper   |  ->  Chinese structured reading report
       / /       +---------+
      /_/          panel-by-panel figures + method notes
```

`read-literature-pdf` is a Codex skill for deep reading of scientific literature PDFs. It turns a paper into a structured Chinese Markdown report with bibliographic metadata, study design, sample tables, method summaries, Results-by-heading interpretation, panel/module-level figure screenshots, and reusable analysis ideas.

It is designed for biomedical and omics papers, especially papers involving single-cell sequencing, spatial transcriptomics, bulk RNA-seq, WES/WGS, imaging, flow cytometry, animal models, clinical cohorts, and immunology or cancer biology.

## What It Does

- Reads a full paper PDF, not only the abstract.
- Extracts article information: title, authors, affiliations, journal, date, DOI, article type, and impact-factor handling.
- Summarizes research background, unresolved questions, core hypothesis, and innovation.
- Organizes sample information, patient cohorts, grouping design, sequencing methods, experimental validation, and public datasets.
- Parses the Results section in the paper's original order.
- Explains each Result as a logic chain: purpose -> data/method -> finding -> figure evidence -> conclusion.
- Splits complex main figures into panel or module screenshots instead of pasting one whole page.
- Adds optional method or mechanism schematics for complex workflows.
- Marks missing information clearly as `原文未明确说明` instead of inventing details.

## Output Style

The generated report is written in Chinese and is suitable for:

- journal club
- lab meeting
- paper sharing
- project design reference
- omics-method learning notes
- figure-by-figure paper explanation

The report usually contains:

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

## Cartoon Workflow

```text
       Step 1              Step 2                Step 3
   +------------+      +-------------+      +----------------+
   |  PDF paper | ---> | Read deeply | ---> | Markdown notes |
   +------------+      +-------------+      +----------------+
         |                    |                      |
         v                    v                      v
    page text           Result logic          panel screenshots
    metadata            method summary        reusable ideas
```

Think of it as a tiny paper-reading helper with a highlighter in one hand and a figure cutter in the other.

## Repository Structure

```text
read_paper_skills/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── report-template.md
├── scripts/
│   └── pdf_prep.py
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

## Installation

Clone the repository:

```bash
git clone git@github.com:FanFPu/read_paper_skills.git
```

Install or copy the skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills/read-literature-pdf
cp -R read_paper_skills/* ~/.codex/skills/read-literature-pdf/
```

Then invoke it in Codex with:

```text
$read-literature-pdf
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

## Figure-Module Rule

The skill is intentionally opinionated about figures.

For multi-panel figures, it should avoid using a whole-page figure as the only visual evidence. Instead, it should crop and explain modules such as:

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

## AI Schematic Rule

The skill may add AI-generated or diagrammatic schematics for complex methods or mechanisms, but these must be clearly separated from original paper figures.

Allowed schematic types:

- study design
- sequencing workflow
- co-culture assay
- treatment timeline
- computational analysis pipeline
- mechanism model

Required caption:

```markdown
**AI 示意图说明：** 本图为根据原文信息生成的辅助示意图，不是原文数据图。
```

If image generation is unavailable, Mermaid diagrams or text workflows can be used instead.

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
