# AI 科研信息图指南

## General Rules

- AI 图用于解释，不用于代替原文数据。
- 提示词只使用原文或精读稿中已经确认的事实。
- 不写具体样本数、P 值、通路方向、疗效结论，除非来源明确。
- 不要求模型复刻论文图版式。
- 图中文字尽量少，优先用简短英文或中英混合标签。

## Cover Prompt Template

```text
Create a clean biomedical scientific infographic cover for a Chinese WeChat article from the account "生信探癌".
Topic: <paper topic>.
Cancer type: <cancer type>.
Key technologies: <technologies>.
Core biological theme: <cell states / tumor microenvironment / therapy resistance / metastasis / immune interaction>.
Visual concept: a tumor microenvironment scene with stylized tumor cells, immune cells, omics data layers, and subtle sequencing/spatial transcriptomics elements.
Style: professional scientific infographic, modern biomedical illustration, clean composition, high contrast, suitable for WeChat article cover, no paper figure replication, no fake charts, no unreadable dense text.
Text on image: <short cover title or no text>.
Aspect ratio: 2.35:1 for WeChat cover.
```

## Study Design Schematic Prompt

```text
Create a clean scientific schematic summarizing the study design of a biomedical paper.
Disease/cancer type: <cancer type>.
Samples/models: <confirmed sample or model types only>.
Assays: <confirmed assays>.
Analysis modules: <confirmed analysis modules>.
Output: show the flow from sample collection to sequencing/experiment, computational analysis, validation, and biological conclusion.
Style: professional biomedical workflow diagram, simple arrows, labeled modules, light background, no invented sample numbers, no fake statistics.
```

## Mechanism Schematic Prompt

```text
Create a clean mechanism model schematic for a biomedical WeChat article.
Cancer context: <cancer type>.
Key cells: <confirmed cells>.
Key molecules/pathways: <confirmed molecules/pathways>.
Main interaction: <confirmed interaction or mechanism>.
Style: professional scientific infographic, tumor microenvironment layout, clear arrows, minimal labels, no invented genes or effects, not a copy of any paper figure.
Caption requirement: AI-generated explanatory schematic, not original paper data.
```

## Analysis Workflow Prompt

```text
Create a bioinformatics workflow schematic for a WeChat article.
Input data: <confirmed data types>.
Main analyses: <confirmed methods, such as scRNA-seq clustering, cell annotation, CNV inference, CellChat, trajectory analysis, spatial mapping>.
Main outputs: <confirmed outputs>.
Style: clean information graphic, modular pipeline, icons for cells, sequencing, computation, validation, light background, readable labels, no fake plots or statistics.
```

## Suggested File Names

- `AI_Cover.png`
- `AI_Study_Design.png`
- `AI_Analysis_Workflow.png`
- `AI_Mechanism_Model.png`

## Caption

Use this caption under every AI-generated image:

```markdown
**AI 示意图说明：** 本图为根据原文信息生成的辅助示意图，不是原文数据图。
```
