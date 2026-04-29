---
name: read-literature-pdf
description: Deeply read scientific or biomedical literature PDFs and produce structured Chinese Markdown reading reports with bibliographic metadata, authors and affiliations, journal/date/impact-factor handling, research background, sample and experimental design, sequencing or assay methods, ordered Results-by-heading interpretation, panel/module-level main-figure screenshots, optional AI-generated method/mechanism schematics, conclusions, limitations, and reusable analysis ideas. Use when a user uploads or references a paper PDF and asks for 文献精读, 深度阅读, 结构化整理, 组会/文献分享报告, figure-by-figure or panel-by-panel paper explanation, or figure-based summaries.
---

# Read Literature PDF

## Goal

Produce a Chinese Markdown literature-reading report from a research PDF. The report must be analytical rather than a direct translation, must follow the paper's actual Results order, and must explain main figures at the panel/module level with screenshots saved in a `figures/` folder. Do not use a whole-page figure as the only visual explanation when the figure contains multiple logical parts.

## Workflow

1. Create an output folder near the PDF or in the current workspace. Use a stable name such as `<pdf-stem>_reading/`, with `figures/` inside it.
2. Read the full PDF before drafting: title page, abstract, introduction, Results, Methods, figure legends, tables, and supplement sections included in the PDF. Do not rely on the abstract alone.
3. Use `scripts/pdf_prep.py` when helpful to extract page-delimited text, metadata, rendered pages, and normalized crops. If the default Python lacks PDF packages, call `load_workspace_dependencies` and run the script with the bundled Python path.

   ```bash
   python /path/to/read-literature-pdf/scripts/pdf_prep.py paper.pdf --out paper_reading --text
   python /path/to/read-literature-pdf/scripts/pdf_prep.py paper.pdf --out paper_reading --render-pages 1-3,8,10
   python /path/to/read-literature-pdf/scripts/pdf_prep.py paper.pdf --out paper_reading --crop 5:0.04,0.08,0.96,0.72:Figure_1.png
   ```

4. Extract bibliographic and study-design facts. If a value is not explicitly stated in the PDF, write `原文未明确说明` or, for impact factor, `PDF 中未提供，需外部查询确认`.
5. Draft the Markdown with figure-module placeholders first. Use `references/report-template.md` when a full skeleton is useful.
6. Locate main-text figures in the PDF, render page previews, then crop each figure into logical panel groups. Save module screenshots under `figures/`, then replace all placeholders with real image links.
7. For complex study designs, sequencing/analysis workflows, co-culture experiments, treatment regimens, or mechanistic models, optionally generate original AI schematic diagrams and save them under `figures/`. Label them clearly as AI-generated schematics.
8. Run a final quality pass against the checklist below before delivering the report.

## Required Report Content

Include these sections unless the user asks for a shorter format:

- 文献信息：标题、期刊、发表时间、DOI、文章类型、第一作者、通讯作者、主要作者、作者单位、影响因子处理。
- 作者与机构信息：作者、共同第一/共同通讯、单位归属和国家/机构线索。
- 研究背景与核心科学问题：疾病或生物学问题、领域空白、核心假设、关键问题、创新点。
- 样本信息与实验设计：样本来源、样本类型、患者数量、样本数量、单细胞数量、分组、队列、验证队列、公共数据库。
- 测序与实验方法：scRNA-seq、snRNA-seq、bulk RNA-seq、WES/WGS、ATAC-seq、CITE-seq、空间转录组、IHC/IF、Flow、qPCR、Western blot、功能实验等。
- Results 逐段解析：严格按原文 Results 小标题顺序逐条整理，并在每个 Result 中按 figure panels 或证据模块讲解。
- 主图截图与图示解读：优先 main figures，不优先 supplementary figures；主图必须尽量拆成多个 panel/module 截图，而不是只贴整页图。
- 方法/机制示意图：对复杂实验设计或分析流程，可加入 AI 生成的原创示意图辅助讲解，并与原文数据图分开标注。
- 文章主要结论、创新点、局限性、对用户课题的启发、可复用分析方法总结。

## Information Extraction Rules

- Capture numerical details when present: patient count, sample count, cell count, sequencing platform, sequencing depth, treatment regimen, filtering thresholds, clustering method, annotation method, differential analysis, enrichment analysis, cell-cell communication, trajectory analysis, spatial localization, survival analysis, and database accession IDs.
- Explain what each omics or experimental method was used to answer. For example, say whether scRNA-seq was used to build a cellular atlas, infer cell states, compare treatment groups, or support cell-cell communication analysis.
- Do not fabricate missing information. Mark gaps plainly with `原文未明确说明`.
- For journal impact factor, use only a value printed in the PDF unless the user requests or the task clearly requires external confirmation. If giving a current impact factor from the web, verify it from an authoritative current source and cite the source.
- Preserve exact original Results headings in English, then explain them in Chinese.
## Impact Factor Rule

If the impact factor is printed in the PDF, report it directly and note that it comes from the PDF.

If the impact factor is not printed in the PDF, write:

`PDF 中未提供，需外部查询确认。`

Only search the web for the current impact factor when the user explicitly asks for it or when the runtime environment supports web access. If externally verified, include the source and year, for example:

`影响因子：XX.X（Journal Citation Reports 2024 / 2025，需以最新 JCR 为准）`

## Bioinformatics Method Explanation Rule

在 Results 逐段解析时，如果某个 Result 小节涉及生物信息学方法，必须判断该方法是否需要进一步解释。

### 1. 需要解释的方法类型

只有当该方法属于文章核心分析、非常规方法、复杂算法、文章创新分析流程，或直接支撑关键结论时，才需要单独介绍。

例如：

- trajectory / pseudotime analysis
- RNA velocity
- CellChat / NicheNet / CellPhoneDB 等细胞通讯方法
- SCENIC / pySCENIC / regulon analysis
- CNV inference / inferCNV / CopyKAT
- cNMF / consensus NMF / meta-program analysis
- spatial domain detection
- spatial cell-cell interaction analysis
- spatial deconvolution
- WGCNA / gene module analysis
- multi-omics integration
- batch correction or data integration methods if they are central to the paper
- machine learning / prediction model / signature construction
- survival model / Cox regression / risk score model
- ligand-receptor prioritization
- pathway activity scoring
- clone evolution / phylogenetic analysis
- mutation signature analysis
- any custom computational pipeline proposed by the paper

### 2. 不需要展开解释的基础方法

以下常规分析方法一般不需要单独做方法介绍，除非文章对其进行了明显改造，或者它是本文最核心的方法创新：

- PCA
- UMAP
- t-SNE
- Leiden / Louvain clustering
- Seurat / Scanpy 标准质控流程
- NormalizeData / ScaleData
- FindVariableFeatures / highly variable genes
- FindMarkers / differential expression
- basic GO / KEGG / Hallmark enrichment
- basic cell type annotation
- basic DotPlot / FeaturePlot / violin plot
- standard cell proportion comparison
- standard correlation analysis

对于这些基础方法，只需要在 Results 中简要说明其用途即可，例如：

`作者使用 UMAP 和 Leiden 聚类构建单细胞图谱，并根据经典 marker 注释主要细胞类型。`

不要为这些基础方法单独写长篇算法介绍。

### 3. 方法介绍的来源优先级

如果需要解释某个生物信息学方法，必须优先依据文章自身的 Methods、Supplementary Methods、Figure legend 或相关结果描述。

优先级如下：

1. Methods / Supplementary Methods 中对该方法的描述
2. Figure legend 中对该方法用途的说明
3. Results 中对该方法输出结果的解释
4. 如果原文没有具体说明，可以进行外部检索，但必须使用可靠来源，例如：
   - 原方法论文
   - 官方文档
   - 软件 GitHub / Bioconductor / CRAN / PyPI 页面
   - 期刊方法学文章

如果外部检索仍无法确认，应写：

`原文未详细说明该方法的具体参数或算法细节。`

不要自行编造参数、阈值或软件版本。

### 4. 方法解释写法

在对应 Result 小节中，如果需要介绍方法，可加入以下小节：

```markdown
#### 方法补充说明：<方法名称>

**为什么这里需要这个方法：**  
说明该方法在本 Result 中用于回答什么问题。

**文章中如何使用：**  
根据 Methods / Figure legend / Results 描述本文如何使用该方法，包括输入数据、分组、参数、输出结果等。

**方法基本原理：**  
用 3–6 句话解释该方法的基本思想，避免过度技术化。

**在本文中的作用：**  
说明这个方法如何支持该 Result 的关键结论。

**需要注意的局限：**  
如果适用，说明该方法可能存在的假设、偏差或解释限制。

## Results Parsing Format

For each Results subsection, include:

1. 原文小标题
2. 研究目的
3. 使用的数据、样本和方法
4. 主要结果
5. 结果逻辑链
6. 对应图表与 panel/module 解读
7. 图片或截图
8. 作者结论
9. 可借鉴分析思路

Use this compact structure:

```markdown
### Result N：<原文小标题>
#### 7.N.1 研究目的
#### 7.N.2 使用的数据与方法
#### 7.N.3 主要结果
#### 7.N.4 结果逻辑链
#### 7.N.5 图表模块解读
##### 模块 1：<逻辑主题，例如样本设计 / UMAP / 空间验证>
![Figure N module](figures/Figure_NA_C.png)
**图示解读：**
##### 模块 2：<逻辑主题，例如临床验证 / 功能实验>
![Figure N module](figures/Figure_ND_F.png)
**图示解读：**
#### 7.N.6 方法或机制示意图
![AI schematic](figures/AI_Method_Schematic_Result_N.png)
**图示说明：** 本图为 AI 生成示意图，用于概括实验设计或机制模型，不代表原文数据。
#### 7.N.7 该部分结论
#### 7.N.8 可借鉴分析思路
```

In `主要结果`, add brief "这说明什么" interpretation for complex findings.

## Figure Workflow

1. In the first draft, insert module-level placeholders. Prefer panel groups that match the paper's reasoning, not just the visual layout:

   ```markdown
   ##### 模块 1：样本设计与细胞图谱建立
   ![Figure 1A-C placeholder](FIGURE_1A_C_PLACEHOLDER)
   > 待替换图片：Figure 1A-C，建议截取 PDF 第 X 页，展示样本/UMAP/细胞类型注释。

   ##### 模块 2：关键细胞状态随疾病进展变化
   ![Figure 1D-F placeholder](FIGURE_1D_F_PLACEHOLDER)
   > 待替换图片：Figure 1D-F，建议截取 PDF 第 X 页，展示差异丰度和关键细胞状态。
   ```

2. Return to the PDF and locate main figures. First render full pages as previews, then crop each main figure into logical modules. Use the figure legend to map each panel to a claim.
3. Split figures by reasoning units:
   - Study design / cohort overview
   - UMAP or atlas construction
   - Quantification / differential abundance
   - Spatial validation / microscopy
   - Clinical cohort validation / survival / recurrence
   - Functional experiment / perturbation
   - Mechanistic model
4. Save screenshots under `figures/` with names like `Figure_1A_C.png`, `Figure_1D_F.png`, `Figure_3_Coculture.png`, `Figure_4_Recurrence.png`. A whole figure screenshot such as `Figure_1_full.png` may be included only as a supplement or overview, not as the only image for that Result.
5. Replace every placeholder:

   ```markdown
   ![Figure 1A-C](figures/Figure_1A_C.png)
   **图示解读：**
   Figure 1A-C 主要展示……
   ```

6. Under each figure module, explain:
   - 这个图块对应什么问题
   - 用了什么样本/方法
   - 读图时先看哪里
   - 得到什么结果
   - 这说明什么
   - 它如何支持本 Results 小节的结论
7. Do not leave placeholders in the final report unless the PDF is inaccessible or figure extraction fails. If that happens, state the reason and the exact figure/page/panel that still needs manual capture.

## AI Schematic Workflow

Use AI-generated schematics only as explanatory aids for methods, experimental design, analytical workflow, or mechanism models. They must not replace original data panels from the PDF.

When useful, generate schematics with the available image generation tool, such as ChatGPT-Image-2 or the active image generation capability. Save outputs under `figures/` with names such as:

- `AI_Study_Design.png`
- `AI_scRNAseq_Workflow.png`
- `AI_Coculture_Assay.png`
- `AI_Mechanism_Model.png`

Rules:

- Base the prompt only on facts extracted from the paper.
- Avoid inventing sample sizes, pathways, cell types, or outcomes.
- Use clean scientific schematic style suitable for a group meeting.
- Prefer simple labels and arrows over dense text.
- Add a caption beginning with `**AI 示意图说明：** 本图为根据原文信息生成的辅助示意图，不是原文数据图。`
- If image generation is unavailable, insert a Mermaid diagram or a text workflow instead and mark it as a schematic summary.

## Quality Checklist

Before finalizing, verify:

- 作者、机构、通讯作者、期刊、发表时间、DOI are captured or marked missing.
- Impact factor is sourced from the PDF, externally verified with citation, or marked `PDF 中未提供，需外部查询确认`.
- Results sections follow the paper's original order.
- Each Result includes purpose, samples/data, methods, findings, logic chain, figure modules, conclusion, and reusable analysis ideas.
- Main figures are split into panel/module screenshots wherever feasible; whole-page figures are not the only visual explanation for multi-panel Results.
- All main figure placeholders are replaced with paths under `figures/`.
- Figure module screenshots correspond to the surrounding text and cite the correct panel labels.
- AI-generated schematics, if used, are clearly marked and do not imply they are original paper data.
- The report ends with an integrated summary and user-topic inspiration.
- No information is invented beyond the PDF or cited external sources.
## Do Not

- Do not only summarize the abstract.
- Do not merge all Results into one broad summary.
- Do not describe figures only as “the figure shows the result”; explain what each panel/module proves.
- Do not write vague phrases such as “multi-omics analysis was performed” without specifying the exact method.
- Do not invent missing sample numbers, sequencing platforms, impact factors, pathways, or author affiliations.
- Do not leave figure placeholders in the final report unless figure extraction fails.
- Do not use AI-generated schematics as substitutes for original paper figures.

## Resource

- `references/report-template.md`: full Chinese Markdown skeleton for the report.
- `scripts/pdf_prep.py`: helper for extracting PDF text/metadata, rendering pages, and cropping figure screenshots from normalized page coordinates.
