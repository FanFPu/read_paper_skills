#!/usr/bin/env python3
"""Prepare a literature PDF for structured reading.

Text and metadata extraction use PyMuPDF when available, otherwise pypdf.
Page rendering and figure cropping require PyMuPDF.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def parse_pages(spec: str, total_pages: int) -> list[int]:
    if spec.lower() == "all":
        return list(range(total_pages))

    pages: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_s, end_s = chunk.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                raise ValueError(f"Invalid page range: {chunk}")
            pages.update(range(start, end + 1))
        else:
            pages.add(int(chunk))

    indexes = sorted(page - 1 for page in pages)
    bad = [page + 1 for page in indexes if page < 0 or page >= total_pages]
    if bad:
        raise ValueError(f"Page(s) out of range: {bad}; PDF has {total_pages} pages")
    return indexes


def parse_crop(spec: str) -> tuple[int, tuple[float, float, float, float], str]:
    match = re.fullmatch(
        r"(\d+):([0-9.]+),([0-9.]+),([0-9.]+),([0-9.]+):([^:]+)",
        spec,
    )
    if not match:
        raise ValueError(
            "Crop must be PAGE:x0,y0,x1,y1:filename.png with normalized 0-1 coordinates"
        )

    page = int(match.group(1))
    coords = tuple(float(match.group(i)) for i in range(2, 6))
    name = match.group(6)
    if any(value < 0 or value > 1 for value in coords):
        raise ValueError("Crop coordinates must be normalized values between 0 and 1")
    x0, y0, x1, y1 = coords
    if not (x0 < x1 and y0 < y1):
        raise ValueError("Crop coordinates must satisfy x0 < x1 and y0 < y1")
    return page - 1, coords, name


def try_load_fitz():
    try:
        import fitz  # type: ignore
    except ImportError:
        return None
    return fitz


def load_pypdf():
    try:
        import pypdf  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "Text extraction requires PyMuPDF or pypdf. Try the Codex bundled Python "
            "runtime or install one of them."
        ) from exc
    return pypdf


def write_text_fitz(doc, out_dir: Path) -> None:
    text_path = out_dir / "pdf_text.md"
    with text_path.open("w", encoding="utf-8") as handle:
        for index, page in enumerate(doc, start=1):
            handle.write(f"\n\n<!-- page {index} -->\n\n")
            handle.write(page.get_text("text").strip())
            handle.write("\n")


def write_text_pypdf(reader, out_dir: Path) -> None:
    text_path = out_dir / "pdf_text.md"
    with text_path.open("w", encoding="utf-8") as handle:
        for index, page in enumerate(reader.pages, start=1):
            handle.write(f"\n\n<!-- page {index} -->\n\n")
            handle.write((page.extract_text() or "").strip())
            handle.write("\n")


def write_metadata_fitz(doc, pdf_path: Path, out_dir: Path) -> None:
    metadata = dict(doc.metadata or {})
    metadata["file"] = str(pdf_path)
    metadata["page_count"] = doc.page_count
    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_metadata_pypdf(reader, pdf_path: Path, out_dir: Path) -> None:
    raw_metadata = reader.metadata or {}
    metadata = {
        str(key).lstrip("/"): str(value)
        for key, value in raw_metadata.items()
        if value is not None
    }
    metadata["file"] = str(pdf_path)
    metadata["page_count"] = len(reader.pages)
    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def render_pages(doc, fitz, pages: list[int], out_dir: Path, dpi: int) -> None:
    page_dir = out_dir / "pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    for index in pages:
        pix = doc[index].get_pixmap(matrix=matrix, alpha=False)
        pix.save(page_dir / f"page_{index + 1:03d}.png")


def crop_figures(doc, fitz, crop_specs: list[str], out_dir: Path, dpi: int) -> None:
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    for spec in crop_specs:
        page_index, coords, name = parse_crop(spec)
        if page_index < 0 or page_index >= doc.page_count:
            raise ValueError(
                f"Crop page {page_index + 1} out of range; PDF has {doc.page_count} pages"
            )
        page = doc[page_index]
        x0, y0, x1, y1 = coords
        rect = page.rect
        clip = fitz.Rect(
            rect.x0 + rect.width * x0,
            rect.y0 + rect.height * y0,
            rect.x0 + rect.width * x1,
            rect.y0 + rect.height * y1,
        )
        output_name = Path(name).name
        if not output_name.lower().endswith(".png"):
            output_name += ".png"
        pix = page.get_pixmap(matrix=matrix, clip=clip, alpha=False)
        pix.save(fig_dir / output_name)


def run_with_fitz(fitz, pdf_path: Path, out_dir: Path, args) -> None:
    doc = fitz.open(pdf_path)
    try:
        write_metadata_fitz(doc, pdf_path, out_dir)
        if args.text:
            write_text_fitz(doc, out_dir)
        if args.render_pages:
            render_pages(doc, fitz, parse_pages(args.render_pages, doc.page_count), out_dir, args.dpi)
        if args.crop:
            crop_figures(doc, fitz, args.crop, out_dir, args.dpi)
    finally:
        doc.close()


def run_with_pypdf(pdf_path: Path, out_dir: Path, args) -> None:
    if args.render_pages or args.crop:
        raise SystemExit(
            "Rendering pages and cropping figures require PyMuPDF. "
            "Install it with: python -m pip install pymupdf"
        )
    pypdf = load_pypdf()
    reader = pypdf.PdfReader(str(pdf_path))
    write_metadata_pypdf(reader, pdf_path, out_dir)
    if args.text:
        write_text_pypdf(reader, out_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Input PDF")
    parser.add_argument("--out", type=Path, default=None, help="Output directory")
    parser.add_argument("--dpi", type=int, default=200, help="Render/crop DPI")
    parser.add_argument("--text", action="store_true", help="Write page-delimited text")
    parser.add_argument(
        "--render-pages",
        default=None,
        help="Pages to render, e.g. 1-3,8,10 or all",
    )
    parser.add_argument(
        "--crop",
        action="append",
        default=[],
        help="Crop as PAGE:x0,y0,x1,y1:filename.png using normalized page coordinates",
    )
    args = parser.parse_args()

    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    out_dir = args.out or Path(f"{pdf_path.stem}_reading")
    out_dir.mkdir(parents=True, exist_ok=True)

    fitz = try_load_fitz()
    if fitz is not None:
        run_with_fitz(fitz, pdf_path, out_dir, args)
    else:
        run_with_pypdf(pdf_path, out_dir, args)

    print(f"Wrote PDF preparation output to {out_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
