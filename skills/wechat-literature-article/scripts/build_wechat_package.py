#!/usr/bin/env python3
"""Build support files for a 生信探癌 WeChat literature article package."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CANCER_COLLECTIONS = {
    "泛癌与肿瘤微环境": [
        "泛癌",
        "pan-cancer",
        "tumor microenvironment",
        "tumour microenvironment",
        "肿瘤微环境",
        "tme",
    ],
    "肺癌": ["肺癌", "lung cancer", "nsclc", "sclc", "luad", "lusc"],
    "乳腺癌": ["乳腺癌", "breast cancer", "brca", "tnbc"],
    "肝癌": ["肝癌", "hepatocellular carcinoma", "hcc", "lihc"],
    "胃癌/食管癌": ["胃癌", "食管癌", "gastric cancer", "stomach cancer", "esophageal", "oesophageal"],
    "结直肠癌": ["结直肠癌", "结肠癌", "直肠癌", "colorectal", "colon cancer", "rectal cancer", "crc"],
    "胰腺癌": ["胰腺癌", "pancreatic cancer", "pdac"],
    "泌尿男生殖肿瘤": [
        "前列腺癌",
        "膀胱癌",
        "肾癌",
        "prostate cancer",
        "bladder cancer",
        "renal cell carcinoma",
        "kidney cancer",
    ],
    "妇科肿瘤": [
        "卵巢癌",
        "宫颈癌",
        "子宫内膜癌",
        "ovarian cancer",
        "cervical cancer",
        "endometrial cancer",
    ],
    "血液肿瘤": ["白血病", "淋巴瘤", "多发性骨髓瘤", "leukemia", "lymphoma", "myeloma", "aml", "cll"],
    "脑胶质瘤/神经肿瘤": ["胶质瘤", "脑肿瘤", "glioma", "glioblastoma", "gbm", "brain tumor"],
    "黑色素瘤": ["黑色素瘤", "melanoma"],
}

TECH_COLLECTIONS = {
    "单细胞组学": ["单细胞", "single-cell", "scrna", "scrna-seq", "snrna", "cite-seq"],
    "空间组学": ["空间转录组", "spatial transcript", "visium", "merfish", "stereo-seq", "cosmx"],
    "多组学整合": ["多组学", "multi-omics", "multiomics", "atac", "proteomics", "methylation"],
    "免疫治疗与 TME": ["免疫治疗", "immunotherapy", "checkpoint", "pd-1", "pd-l1", "ctla-4", "tme"],
    "AI/机器学习": ["机器学习", "人工智能", "machine learning", "deep learning", "prediction model"],
    "数据库与工具": ["数据库", "database", "webserver", "web server", "tool", "software", "package", "github"],
    "生信教程": ["教程", "pipeline", "workflow", "教程", "代码", "analysis tutorial"],
}

ARTICLE_TYPE_KEYWORDS = {
    "技术教程": ["教程", "pipeline", "workflow", "代码", "step-by-step", "tutorial"],
    "数据库工具": ["数据库", "database", "webserver", "web server", "tool", "software", "package"],
    "热点综述": ["review", "综述", "perspective", "commentary", "热点"],
}


@dataclass
class ImageRef:
    alt: str
    path: str
    kind: str
    section: str


@dataclass
class ResultFigureStatus:
    section: str
    images: list[ImageRef]


def slugify(value: str) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", value.strip())
    return value.strip("_") or "wechat_article"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_heading(markdown: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    return match.group(1).strip() if match else "原文未明确说明"


def strip_markdown(markdown: str) -> str:
    markdown = re.sub(r"!\[[^\]]*\]\([^)]*ai_images/[^)]+\)", "", markdown, flags=re.IGNORECASE)
    markdown = re.sub(r"\*\*AI\s*示意图说明：\*\*.*", "", markdown, flags=re.IGNORECASE)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", markdown)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[#>*_`|~-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def score_keywords(text_lower: str, mapping: dict[str, list[str]]) -> list[tuple[str, int]]:
    scores = []
    for label, keywords in mapping.items():
        score = sum(text_lower.count(keyword.lower()) for keyword in keywords)
        if score:
            scores.append((label, score))
    return sorted(scores, key=lambda item: (-item[1], item[0]))


def infer_classification(markdown: str) -> dict[str, object]:
    text = strip_markdown(markdown)
    text_lower = text.lower()

    cancer_scores = score_keywords(text_lower, CANCER_COLLECTIONS)
    tech_scores = score_keywords(text_lower, TECH_COLLECTIONS)

    if cancer_scores:
        primary_collection = cancer_scores[0][0]
        cancer_type = primary_collection
    elif tech_scores:
        primary_collection = tech_scores[0][0]
        cancer_type = "原文未明确说明"
    else:
        primary_collection = "其他肿瘤"
        cancer_type = "原文未明确说明"

    article_type = "文献解读"
    for label, keywords in ARTICLE_TYPE_KEYWORDS.items():
        if any(keyword.lower() in text_lower for keyword in keywords):
            article_type = label
            break

    technology_tags = [label for label, _ in tech_scores[:5]]
    topic_tags = []
    for label in [cancer_type, *technology_tags, article_type]:
        if label and label != "原文未明确说明" and label not in topic_tags:
            topic_tags.append(label)
    if "肿瘤微环境" in text and "肿瘤微环境" not in topic_tags:
        topic_tags.append("肿瘤微环境")
    if not topic_tags:
        topic_tags = ["文献解读", "肿瘤研究", "生信分析"]

    return {
        "article_type": article_type,
        "cancer_type": cancer_type,
        "technology_tags": technology_tags,
        "primary_collection": primary_collection,
        "topic_tags": topic_tags[:5],
        "publish_notes": "分类为自动初筛结果，发布前请按微信后台实际合集和话题标签复核。",
    }


def extract_field(markdown: str, names: Iterable[str]) -> str:
    for name in names:
        patterns = [
            rf"\|\s*{re.escape(name)}\s*\|\s*([^|\n]+)\|",
            rf"\*\*{re.escape(name)}[:：]\*\*\s*([^\n]+)",
            rf"{re.escape(name)}[:：]\s*([^\n]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, markdown, flags=re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                return value or "原文未明确说明"
    return "原文未明确说明"


def extract_summary(markdown: str) -> str:
    lines = markdown.splitlines()
    candidates = []
    in_title_candidates = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            in_title_candidates = False
            continue
        if stripped.startswith("> 备选标题"):
            in_title_candidates = True
            continue
        if in_title_candidates or stripped.startswith(">"):
            continue
        if stripped.startswith("#") or stripped.startswith("|") or stripped.startswith("!") or stripped.startswith("-"):
            continue
        if stripped.startswith("**AI 示意图说明"):
            continue
        candidates.append(stripped)
        if len("".join(candidates)) >= 120:
            break
    plain = strip_markdown(" ".join(candidates) if candidates else markdown)
    if not plain:
        return "原文未明确说明"
    sentences = re.split(r"(?<=[。！？.!?])\s+", plain)
    summary = "".join(sentences[:2]).strip()
    return summary[:180] if summary else plain[:180]


def make_title_candidates(title: str, classification: dict[str, object]) -> list[str]:
    cancer = classification.get("cancer_type") or "肿瘤"
    if cancer == "原文未明确说明":
        cancer = "肿瘤"
    techs = classification.get("technology_tags") or []
    tech = techs[0] if techs else "生信分析"
    clean_title = title if title != "原文未明确说明" else "这篇肿瘤生信研究"
    return [
        f"{cancer}研究新线索：一文读懂这篇文献的核心发现",
        f"{tech}如何解析{cancer}？这篇文章值得细看",
        f"从数据到机制：{clean_title}",
        f"生信探癌读文献：{cancer}中的关键细胞状态与分析思路",
    ]


def extract_images(markdown: str) -> list[ImageRef]:
    images = []
    current_section = "未定位章节"
    for line in markdown.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            current_section = heading.group(2).strip()
        for match in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", line):
            alt = match.group(1).strip()
            path = match.group(2).strip()
            lower = f"{alt} {path}".lower()
            kind = "AI示意图" if "ai" in lower or "示意" in lower else "原文数据图"
            images.append(ImageRef(alt=alt, path=path, kind=kind, section=current_section))
    return images


def is_result_heading(title: str) -> bool:
    normalized = title.strip().lower()
    if "参考" in normalized or "图源" in normalized:
        return False
    return (
        normalized.startswith("result ")
        or normalized.startswith("result：")
        or normalized.startswith("result:")
        or normalized.startswith("结果")
        or normalized.startswith("结论")
    )


def is_forbidden_figure_path(path: str) -> bool:
    name = Path(path.split("#", 1)[0].split("?", 1)[0]).name.lower()
    return bool(
        re.search(r"(^|[_-])page[_-]?\d+", name)
        or re.search(r"figure[_-]?\d+[_-]?(full|page)", name)
        or re.search(r"(full[_-]?figure|whole[_-]?page)", name)
    )


def extract_result_figure_status(markdown: str) -> list[ResultFigureStatus]:
    current: ResultFigureStatus | None = None
    statuses: list[ResultFigureStatus] = []
    in_conclusion_walkthrough = False

    for line in markdown.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            title = heading.group(2).strip()
            if "结论详解" in title:
                in_conclusion_walkthrough = True
                current = None
            elif in_conclusion_walkthrough and re.match(r"^#{1,2}\s+", line) and "结论详解" not in title:
                in_conclusion_walkthrough = False
                current = None

            if is_result_heading(title) and title.strip() != "结论详解":
                current = ResultFigureStatus(section=title, images=[])
                statuses.append(current)

        for match in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", line):
            if current is None:
                continue
            alt = match.group(1).strip()
            path = match.group(2).strip()
            lower = f"{alt} {path}".lower()
            kind = "AI示意图" if "ai" in lower or "示意" in lower else "原文数据图"
            current.images.append(ImageRef(alt=alt, path=path, kind=kind, section=current.section))

    return statuses


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def markdown_table_to_html(rows: list[str]) -> str:
    parsed = []
    for row in rows:
        cells = [inline_markdown(cell.strip()) for cell in row.strip().strip("|").split("|")]
        if cells and not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            parsed.append(cells)
    if not parsed:
        return ""
    html_rows = []
    for index, cells in enumerate(parsed):
        tag = "th" if index == 0 else "td"
        html_rows.append("<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in cells) + "</tr>")
    return '<table class="wx-table">' + "".join(html_rows) + "</table>"


def markdown_to_wechat_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out = []
    paragraph = []
    list_items = []
    table_rows = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{inline_markdown(' '.join(paragraph).strip())}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            out.append("<ul>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in list_items) + "</ul>")
            list_items.clear()

    def flush_table() -> None:
        if table_rows:
            html_table = markdown_table_to_html(table_rows)
            if html_table:
                out.append(html_table)
            table_rows.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            flush_list()
            flush_table()
            continue

        image = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if image:
            flush_paragraph()
            flush_list()
            flush_table()
            alt = html.escape(image.group(1).strip())
            src = html.escape(image.group(2).strip())
            out.append(f'<figure><img src="{src}" alt="{alt}"><figcaption>{alt}</figcaption></figure>')
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            flush_table()
            level = min(len(heading.group(1)) + 1, 4)
            out.append(f"<h{level}>{inline_markdown(heading.group(2).strip())}</h{level}>")
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            flush_list()
            flush_table()
            out.append(f"<blockquote>{inline_markdown(stripped.lstrip('> ').strip())}</blockquote>")
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            table_rows.append(stripped)
            continue

        bullet = re.match(r"^[-*+]\s+(.+)$", stripped) or re.match(r"^\d+[.、]\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            flush_table()
            list_items.append(bullet.group(1).strip())
            continue

        flush_list()
        flush_table()
        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    flush_table()

    css = """
body { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; color: #222; line-height: 1.75; }
h2 { font-size: 22px; margin: 28px 0 12px; border-left: 4px solid #1b7f79; padding-left: 10px; }
h3 { font-size: 19px; margin: 24px 0 10px; color: #1b4f72; }
h4 { font-size: 17px; margin: 20px 0 8px; color: #444; }
p { margin: 12px 0; }
blockquote { margin: 14px 0; padding: 10px 14px; background: #f5f7f8; border-left: 4px solid #7aa7a3; color: #444; }
figure { margin: 18px 0; text-align: center; }
img { max-width: 100%; height: auto; border-radius: 4px; }
figcaption { font-size: 13px; color: #666; margin-top: 6px; }
.wx-table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 14px; }
.wx-table th, .wx-table td { border: 1px solid #d9e2e4; padding: 8px; vertical-align: top; }
.wx-table th { background: #eef6f5; }
""".strip()
    return f"<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n<style>{css}</style>\n</head>\n<body>\n" + "\n".join(out) + "\n</body>\n</html>\n"


def write_metadata(markdown: str, out_dir: Path, source: Path) -> dict[str, object]:
    title = first_heading(markdown)
    classification = infer_classification(markdown)
    metadata = {
        "account": "生信探癌",
        "source_file": str(source),
        "wechat_entry": "https://mp.weixin.qq.com/",
        "draft_mode": "browser_assisted",
        "draft_safety": "仅创建或保存草稿；不得自动群发、发表或点击不可逆确认按钮。",
        "title_candidates": make_title_candidates(title, classification),
        "selected_title": title,
        "summary": extract_summary(markdown),
        "cover_text": title[:28] if title != "原文未明确说明" else "生信探癌文献解读",
        "paper": {
            "title": extract_field(markdown, ["论文题目", "题目", "标题", "Title"]),
            "journal": extract_field(markdown, ["期刊", "Journal"]),
            "date": extract_field(markdown, ["发表时间", "发表日期", "Date"]),
            "doi": extract_field(markdown, ["DOI", "doi"]),
        },
        **classification,
    }
    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return metadata


def write_image_manifest(markdown: str, out_dir: Path, article_dir: Path) -> None:
    rows = []
    result_statuses = {status.section: status for status in extract_result_figure_status(markdown)}
    for image in extract_images(markdown):
        path = Path(image.path)
        exists = path.exists() if path.is_absolute() else (article_dir / path).exists()
        forbidden = is_forbidden_figure_path(image.path)
        in_result = image.section in result_statuses
        usage_status = "ok"
        if forbidden:
            usage_status = "forbidden_whole_page_or_full_figure"
        elif in_result and image.kind != "原文数据图":
            usage_status = "ai_image_does_not_satisfy_result_requirement"
        elif not exists:
            usage_status = "missing_file"
        source_note = (
            "AI生成示意图，不代表原文数据"
            if image.kind == "AI示意图"
            else "原文数据图，仅用于文献解读，请发布前确认版权/转载要求"
        )
        rows.append(
            {
                "kind": image.kind,
                "path": image.path,
                "figure_path": image.path,
                "exists": "yes" if exists else "no",
                "alt": image.alt,
                "section": image.section,
                "result_section": image.section if in_result else "",
                "figure_label": image.alt or "待补充",
                "source_or_figure": image.alt or "待补充",
                "usage": "正文配图",
                "usage_status": usage_status,
                "review_note": source_note,
            }
        )

    for section, status in result_statuses.items():
        usable_original_images = [
            image
            for image in status.images
            if image.kind == "原文数据图" and not is_forbidden_figure_path(image.path)
        ]
        if not usable_original_images:
            rows.append(
                {
                    "kind": "原文数据图",
                    "path": "",
                    "figure_path": "",
                    "exists": "no",
                    "alt": "缺少可用局部图块",
                    "section": section,
                    "result_section": section,
                    "figure_label": "待补图",
                    "source_or_figure": "待补图",
                    "usage": "Result必配图",
                    "usage_status": "missing_result_figure",
                    "review_note": "该 Result 缺少可用局部图块，需回到 read-literature-pdf 阶段补图。",
                }
            )

    if not rows:
        rows.append(
            {
                "kind": "AI示意图",
                "path": "ai_images/AI_Cover.png",
                "figure_path": "ai_images/AI_Cover.png",
                "exists": "no",
                "alt": "AI cover",
                "section": "封面",
                "result_section": "",
                "figure_label": "AI cover",
                "source_or_figure": "AI生成",
                "usage": "公众号封面",
                "usage_status": "prompt_only",
                "review_note": "根据 ai_image_prompts.md 生成，发布前确认不含伪造数据",
            }
        )

    with (out_dir / "image_manifest.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "kind",
                "path",
                "figure_path",
                "exists",
                "alt",
                "section",
                "result_section",
                "figure_label",
                "source_or_figure",
                "usage",
                "usage_status",
                "review_note",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_ai_prompts(out_dir: Path, metadata: dict[str, object]) -> None:
    cancer = metadata.get("cancer_type", "肿瘤")
    tech_tags = metadata.get("technology_tags") or ["生信分析"]
    topic_tags = metadata.get("topic_tags") or ["文献解读"]
    title = metadata.get("selected_title", "生信探癌文献解读")
    content = f"""# AI Image Prompts

## AI_Cover.png

```text
Create a clean biomedical scientific infographic cover for a Chinese WeChat article from the account "生信探癌".
Topic: {title}.
Cancer type: {cancer}.
Key technologies: {", ".join(str(tag) for tag in tech_tags)}.
Core theme tags: {", ".join(str(tag) for tag in topic_tags)}.
Visual concept: a tumor microenvironment scene with stylized tumor cells, immune cells, omics data layers, and subtle sequencing or spatial transcriptomics elements.
Style: professional scientific infographic, modern biomedical illustration, clean composition, high contrast, suitable for WeChat article cover, no paper figure replication, no fake charts, no unreadable dense text.
Text on image: {metadata.get("cover_text", "生信探癌")}.
Aspect ratio: 2.35:1 for WeChat cover.
```

## AI_Analysis_Workflow.png

```text
Create a clean bioinformatics workflow schematic for a Chinese biomedical WeChat article.
Cancer context: {cancer}.
Input data and methods: use only the confirmed technologies from the source article, especially {", ".join(str(tag) for tag in tech_tags)}.
Output: show the flow from samples to sequencing/experiment, computational analysis, validation, and biological interpretation.
Style: professional biomedical workflow diagram, simple arrows, labeled modules, light background, no invented sample numbers, no fake statistics, not a copy of any paper figure.
```

## Caption

```markdown
**AI 示意图说明：** 本图为根据原文信息生成的辅助示意图，不是原文数据图。
```
"""
    (out_dir / "ai_image_prompts.md").write_text(content, encoding="utf-8")


def write_review_checklist(out_dir: Path) -> None:
    content = """# 发布前人工核对清单

- [ ] 标题、摘要、封面文案适合「生信探癌」公众号。
- [ ] 论文标题、期刊、发表时间、DOI 没有编造；缺失处已写 `原文未明确说明`。
- [ ] `metadata.json` 中 `primary_collection`、`topic_tags` 与微信后台实际合集/话题标签一致。
- [ ] 原文数据图已在 `image_manifest.csv` 标明 Figure/panel 和版权/转载审核提示。
- [ ] 每个 Result/结论详解模块至少包含一张来自源 Markdown 的原文局部图块；`image_manifest.csv` 中无 `missing_result_figure`。
- [ ] 未使用 `page_003.png`、`Figure_1_full.png`、`Figure_2_page_5.png` 等整页截图或整页 Figure 作为 Result 配图。
- [ ] AI 图仅作为封面或示意图，已明确标注不是原文数据图。
- [ ] `wechat.html` 中图片路径可访问，复制到微信编辑器后版式正常。
- [ ] 未保存任何包含微信后台会话 token 参数的链接、AppID、AppSecret 或其他凭据。
- [ ] 浏览器自动化只保存草稿，不点击群发、发表、发布或其他不可逆确认按钮。
"""
    (out_dir / "review_checklist.md").write_text(content, encoding="utf-8")


def assert_no_wechat_token(out_dir: Path) -> None:
    offenders = []
    for path in out_dir.glob("*"):
        if path.is_file() and path.suffix in {".md", ".html", ".json", ".csv", ".txt"}:
            if "token=" in path.read_text(encoding="utf-8", errors="ignore").lower():
                offenders.append(path.name)
    if offenders:
        raise SystemExit(f"Refusing to keep WeChat token URLs in output files: {', '.join(offenders)}")


def build_package(article_path: Path, out_dir: Path) -> None:
    markdown = read_text(article_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "article.md").write_text(markdown, encoding="utf-8")
    (out_dir / "wechat.html").write_text(markdown_to_wechat_html(markdown), encoding="utf-8")
    metadata = write_metadata(markdown, out_dir, article_path)
    write_image_manifest(markdown, out_dir, article_path.parent)
    write_ai_prompts(out_dir, metadata)
    write_review_checklist(out_dir)
    assert_no_wechat_token(out_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path, help="Path to article.md or a drafted Markdown article.")
    parser.add_argument("--out", type=Path, help="Output package directory. Defaults to <article-stem>_wechat.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    article_path = args.article.expanduser().resolve()
    if not article_path.exists():
        raise SystemExit(f"Article file not found: {article_path}")
    out_dir = args.out.expanduser().resolve() if args.out else article_path.with_name(f"{slugify(article_path.stem)}_wechat")
    build_package(article_path, out_dir)
    print(f"WeChat package written to: {out_dir}")


if __name__ == "__main__":
    main()
