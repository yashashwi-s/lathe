#!/usr/bin/env python3
"""Audit the 32 expansion reference PDFs for clipping and visual corruption.

The audit combines PDF structure checks, glyph bounds, raster edge contact,
compile-log overfull warnings, suspicious extracted text, and contact sheets
that expose every expansion reference page for manual review. The canonical
157-document base is deliberately outside this audit.

Run with:
  mamba run -n lathe python scripts/dataset/audit_reference_visuals.py
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "data" / "latex_benchmark_v0"
DEFAULT_SPLIT = DATASET / "splits" / "expansion_32.csv"
OUT_DIR = (
    ROOT / "results" / "latex_benchmark_v0" / "reference_visual_audit_expansion_32"
)
OVERFULL_RE = re.compile(r"Overfull \\([hv])box \(([0-9.]+)pt")
RAW_TEX_RE = re.compile(
    r"(?:\\(?:fontfamily|selectfont|textstyle|displaystyle|scriptstyle|"
    r"rmfamily|sffamily|ttfamily|mathbf|mathrm|mathit)\b|\^\^[A-Za-z0-9])"
)
REPLACEMENT_MARKERS = ("\ufffd", "[unknown glyph]", "cid:")


@dataclass
class PageAudit:
    sample_id: str
    category: str
    page_number: int
    width_pt: float
    height_pt: float
    text_blocks: int
    word_count: int
    char_count: int
    text_outside_count: int
    text_touching_edge_count: int
    raster_edge_ink_pixels: int
    raster_ink_fraction: float
    suspicious_text_hits: int
    replacement_marker_hits: int
    blank_page: bool
    render_ok: bool
    flags: str
    contact_sheet: str = ""
    contact_slot: int = 0


@dataclass
class DocumentAudit:
    sample_id: str
    category: str
    manifest_pages: int
    actual_pages: int
    page_count_match: bool
    render_ok: bool
    text_outside_count: int
    pages_with_edge_text: int
    pages_with_raster_edge_ink: int
    blank_pages: int
    suspicious_text_hits: int
    replacement_marker_hits: int
    overfull_warning_count: int
    max_overfull_pt: float
    overfull_axes: str
    auto_status: str
    flags: str


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def compile_overfull(log_path: Path) -> tuple[list[tuple[str, float]], list[str]]:
    if not log_path.exists():
        return [], []
    text = log_path.read_text(encoding="utf-8", errors="replace")
    occurrences = [(axis, float(amount)) for axis, amount in OVERFULL_RE.findall(text)]
    # Logs often contain repeated compiler passes. Preserve unique warning text
    # for the report while using the maximum amount for risk classification.
    warning_lines = []
    seen = set()
    for line in text.splitlines():
        if "Overfull \\" not in line and "overfull \\" not in line:
            continue
        normalized = re.sub(r"^warning:\s*", "", line.strip())
        if normalized not in seen:
            seen.add(normalized)
            warning_lines.append(normalized)
    return occurrences, warning_lines


def chars_and_flags(page: fitz.Page) -> tuple[int, int, int, int, int, str]:
    raw = page.get_text("rawdict")
    page_rect = page.rect
    char_count = 0
    outside = 0
    touching = 0
    text_parts: list[str] = []
    text_blocks = 0
    tolerance = 0.25
    edge_tolerance = 0.75
    for block in raw.get("blocks", []):
        if block.get("type") != 0:
            continue
        text_blocks += 1
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                for char in span.get("chars", []):
                    value = char.get("c", "")
                    text_parts.append(value)
                    if not value.strip():
                        continue
                    char_count += 1
                    x0, y0, x1, y1 = (float(v) for v in char.get("bbox", (0, 0, 0, 0)))
                    if (
                        x0 < page_rect.x0 - tolerance
                        or y0 < page_rect.y0 - tolerance
                        or x1 > page_rect.x1 + tolerance
                        or y1 > page_rect.y1 + tolerance
                    ):
                        outside += 1
                    if (
                        x0 <= page_rect.x0 + edge_tolerance
                        or y0 <= page_rect.y0 + edge_tolerance
                        or x1 >= page_rect.x1 - edge_tolerance
                        or y1 >= page_rect.y1 - edge_tolerance
                    ):
                        touching += 1
    extracted = "".join(text_parts)
    suspicious = len(RAW_TEX_RE.findall(extracted))
    replacements = sum(extracted.lower().count(marker) for marker in REPLACEMENT_MARKERS)
    return text_blocks, char_count, outside, touching, suspicious, extracted


def render_page(page: fitz.Page, dpi: int) -> tuple[Image.Image, int, float]:
    scale = dpi / 72.0
    pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    mode = "RGB" if pixmap.n == 3 else "RGBA"
    image = Image.frombytes(mode, (pixmap.width, pixmap.height), pixmap.samples).convert("RGB")
    gray = np.asarray(image.convert("L"))
    ink = gray < 245
    ink_fraction = float(ink.mean()) if ink.size else 0.0
    band = max(1, int(round(dpi / 72.0)))
    edge = np.concatenate(
        [
            ink[:band, :].ravel(),
            ink[-band:, :].ravel(),
            ink[:, :band].ravel(),
            ink[:, -band:].ravel(),
        ]
    )
    edge_ink = int(edge.sum())
    return image, edge_ink, ink_fraction


def page_flags(
    *, outside: int, touching: int, edge_ink: int, ink_fraction: float,
    suspicious: int, replacements: int, render_ok: bool, compile_overfull: bool,
) -> list[str]:
    flags = []
    if not render_ok:
        flags.append("render_failed")
    if outside:
        flags.append("text_outside_page")
    if touching:
        flags.append("text_touching_edge")
    if edge_ink:
        flags.append("raster_edge_ink")
    if ink_fraction < 0.00002:
        flags.append("blank_page")
    if suspicious:
        flags.append("raw_tex_suspicion")
    if replacements:
        flags.append("replacement_marker")
    if compile_overfull:
        flags.append("compile_overfull")
    return flags


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def flush_contact_sheet(
    entries: list[tuple[PageAudit, Image.Image]], output: Path, index: int,
    columns: int, rows: int,
) -> Path:
    cell_w, cell_h = 500, 700
    label_h = 56
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "#d9d9d9")
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(17)
    flag_font = load_font(13)
    path = output / "contact_sheets" / f"reference_pages_{index:03d}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    for slot, (record, image) in enumerate(entries, start=1):
        grid_index = slot - 1
        row, column = divmod(grid_index, columns)
        x0, y0 = column * cell_w, row * cell_h
        severe = any(
            name in record.flags
            for name in ("render_failed", "text_outside_page", "raster_edge_ink")
        )
        review = bool(record.flags)
        header_color = "#ffb3b3" if severe else "#ffe6a6" if review else "#c8efc8"
        draw.rectangle((x0, y0, x0 + cell_w - 1, y0 + label_h), fill=header_color)
        label = f"{record.sample_id}  p{record.page_number}"
        draw.text((x0 + 8, y0 + 5), label, fill="black", font=title_font)
        flag_text = record.flags or "auto-clear"
        if len(flag_text) > 66:
            flag_text = flag_text[:63] + "..."
        draw.text((x0 + 8, y0 + 31), flag_text, fill="#333333", font=flag_font)
        available_w = cell_w - 18
        available_h = cell_h - label_h - 14
        scale = min(available_w / image.width, available_h / image.height)
        width = max(1, int(image.width * scale))
        height = max(1, int(image.height * scale))
        thumb = image.resize((width, height), Image.Resampling.LANCZOS)
        px = x0 + (cell_w - width) // 2
        py = y0 + label_h + (available_h - height) // 2
        sheet.paste(thumb, (px, py))
        draw.rectangle((px, py, px + width, py + height), outline="#666666", width=1)
        record.contact_sheet = relative(path)
        record.contact_slot = slot
    sheet.save(path, format="PNG", optimize=True)
    return path


def audit(args: argparse.Namespace) -> tuple[list[DocumentAudit], list[PageAudit], list[Path]]:
    accepted_by_id = {
        row["sample_id"]: row
        for row in read_csv(args.dataset / "manifests" / "accepted.csv")
    }
    split_rows = read_csv(args.split)
    split_ids = [row["sample_id"] for row in split_rows]
    duplicate_ids = sorted(
        sample_id for sample_id, count in Counter(split_ids).items() if count > 1
    )
    if duplicate_ids:
        raise ValueError(f"duplicate sample IDs in split: {duplicate_ids}")
    missing_ids = [sample_id for sample_id in split_ids if sample_id not in accepted_by_id]
    if missing_ids:
        raise ValueError(f"split IDs missing from accepted manifest: {missing_ids}")
    accepted = [accepted_by_id[sample_id] for sample_id in split_ids]
    documents: list[DocumentAudit] = []
    pages: list[PageAudit] = []
    contact_entries: list[tuple[PageAudit, Image.Image]] = []
    contact_paths: list[Path] = []
    capacity = args.sheet_columns * args.sheet_rows
    sheet_index = 1

    for document_index, row in enumerate(accepted, start=1):
        sample_id = row["sample_id"]
        category = row["category"]
        sample_dir = ROOT / row["sample_dir"]
        reference = sample_dir / "reference.pdf"
        overfull, _warning_lines = compile_overfull(sample_dir / "compile.log")
        page_rows: list[PageAudit] = []
        render_ok = True
        try:
            pdf = fitz.open(reference)
        except Exception:
            pdf = None
            render_ok = False
        actual_pages = pdf.page_count if pdf is not None else 0
        if pdf is not None:
            for page_index in range(actual_pages):
                page = pdf.load_page(page_index)
                text_blocks, chars, outside, touching, suspicious, extracted = chars_and_flags(page)
                replacements = sum(
                    extracted.lower().count(marker) for marker in REPLACEMENT_MARKERS
                )
                words = len(page.get_text("words"))
                page_render_ok = True
                try:
                    image, edge_ink, ink_fraction = render_page(page, args.render_dpi)
                except Exception:
                    image = Image.new("RGB", (800, 1000), "white")
                    edge_ink, ink_fraction = 0, 0.0
                    page_render_ok = False
                    render_ok = False
                flags = page_flags(
                    outside=outside,
                    touching=touching,
                    edge_ink=edge_ink,
                    ink_fraction=ink_fraction,
                    suspicious=suspicious,
                    replacements=replacements,
                    render_ok=page_render_ok,
                    compile_overfull=bool(overfull),
                )
                record = PageAudit(
                    sample_id=sample_id,
                    category=category,
                    page_number=page_index + 1,
                    width_pt=round(page.rect.width, 3),
                    height_pt=round(page.rect.height, 3),
                    text_blocks=text_blocks,
                    word_count=words,
                    char_count=chars,
                    text_outside_count=outside,
                    text_touching_edge_count=touching,
                    raster_edge_ink_pixels=edge_ink,
                    raster_ink_fraction=round(ink_fraction, 7),
                    suspicious_text_hits=suspicious,
                    replacement_marker_hits=replacements,
                    blank_page=ink_fraction < 0.00002,
                    render_ok=page_render_ok,
                    flags=";".join(flags),
                )
                pages.append(record)
                page_rows.append(record)
                contact_entries.append((record, image))
                if len(contact_entries) == capacity:
                    contact_paths.append(
                        flush_contact_sheet(
                            contact_entries, args.out, sheet_index,
                            args.sheet_columns, args.sheet_rows,
                        )
                    )
                    sheet_index += 1
                    contact_entries = []
            pdf.close()

        aggregate_flags = []
        manifest_pages = int(row["page_count"])
        if actual_pages != manifest_pages:
            aggregate_flags.append("page_count_mismatch")
        if not render_ok:
            aggregate_flags.append("render_failed")
        text_outside = sum(page.text_outside_count for page in page_rows)
        edge_text_pages = sum(page.text_touching_edge_count > 0 for page in page_rows)
        edge_ink_pages = sum(page.raster_edge_ink_pixels > 0 for page in page_rows)
        blank_pages = sum(page.blank_page for page in page_rows)
        suspicious_hits = sum(page.suspicious_text_hits for page in page_rows)
        replacement_hits = sum(page.replacement_marker_hits for page in page_rows)
        if text_outside:
            aggregate_flags.append("text_outside_page")
        if edge_text_pages:
            aggregate_flags.append("text_touching_edge")
        if edge_ink_pages:
            aggregate_flags.append("raster_edge_ink")
        if blank_pages:
            aggregate_flags.append("blank_page")
        if suspicious_hits:
            aggregate_flags.append("raw_tex_suspicion")
        if replacement_hits:
            aggregate_flags.append("replacement_marker")
        max_overfull = max((amount for _, amount in overfull), default=0.0)
        if overfull:
            aggregate_flags.append("compile_overfull")
        severe = bool(
            text_outside
            or edge_ink_pages
            or not render_ok
            or actual_pages != manifest_pages
            or replacement_hits
        )
        review = bool(aggregate_flags)
        documents.append(
            DocumentAudit(
                sample_id=sample_id,
                category=category,
                manifest_pages=manifest_pages,
                actual_pages=actual_pages,
                page_count_match=actual_pages == manifest_pages,
                render_ok=render_ok,
                text_outside_count=text_outside,
                pages_with_edge_text=edge_text_pages,
                pages_with_raster_edge_ink=edge_ink_pages,
                blank_pages=blank_pages,
                suspicious_text_hits=suspicious_hits,
                replacement_marker_hits=replacement_hits,
                overfull_warning_count=len(overfull),
                max_overfull_pt=round(max_overfull, 5),
                overfull_axes=";".join(sorted({axis for axis, _ in overfull})),
                auto_status="fail" if severe else "review" if review else "clear",
                flags=";".join(aggregate_flags),
            )
        )
        print(
            f"[{document_index}/{len(accepted)}] {sample_id}: "
            f"pages={actual_pages} status={documents[-1].auto_status}",
            flush=True,
        )

    if contact_entries:
        contact_paths.append(
            flush_contact_sheet(
                contact_entries, args.out, sheet_index,
                args.sheet_columns, args.sheet_rows,
            )
        )
    return documents, pages, contact_paths


def write_reports(
    args: argparse.Namespace, documents: list[DocumentAudit],
    pages: list[PageAudit], contact_paths: list[Path],
) -> None:
    document_rows = [asdict(row) for row in documents]
    page_rows = [asdict(row) for row in pages]
    write_csv(
        args.out / "document_audit.csv",
        document_rows,
        list(DocumentAudit.__dataclass_fields__),
    )
    write_csv(
        args.out / "page_audit.csv",
        page_rows,
        list(PageAudit.__dataclass_fields__),
    )
    status_counts = Counter(row.auto_status for row in documents)
    manual_path = args.out / "manual_review.csv"
    manual_rows = read_csv(manual_path) if manual_path.exists() else []
    manual_counts = Counter(row["manual_status"] for row in manual_rows)
    if manual_rows:
        expected_ids = {row.sample_id for row in documents}
        reviewed_ids = {row["sample_id"] for row in manual_rows}
        if reviewed_ids != expected_ids or len(manual_rows) != len(documents):
            missing = sorted(expected_ids - reviewed_ids)
            extra = sorted(reviewed_ids - expected_ids)
            raise ValueError(
                "manual review must cover the expansion split exactly once; "
                f"missing={missing}, extra={extra}, rows={len(manual_rows)}"
            )
        pages_by_id = {row.sample_id: row.actual_pages for row in documents}
        wrong_page_counts = [
            row["sample_id"] for row in manual_rows
            if int(row["pages_reviewed"]) != pages_by_id[row["sample_id"]]
        ]
        if wrong_page_counts:
            raise ValueError(
                f"manual review page counts do not match PDFs: {wrong_page_counts}"
            )
    category_counts: dict[str, Counter] = {}
    for row in documents:
        category_counts.setdefault(row.category, Counter())[row.auto_status] += 1
    summary = {
        "documents": len(documents),
        "pages": len(pages),
        "split": relative(args.split),
        "render_dpi": args.render_dpi,
        "status_counts": dict(status_counts),
        "page_count_mismatches": sum(not row.page_count_match for row in documents),
        "render_failures": sum(not row.render_ok for row in documents),
        "documents_with_text_outside": sum(row.text_outside_count > 0 for row in documents),
        "documents_with_raster_edge_ink": sum(
            row.pages_with_raster_edge_ink > 0 for row in documents
        ),
        "documents_with_overfull_warnings": sum(
            row.overfull_warning_count > 0 for row in documents
        ),
        "max_overfull_pt": max((row.max_overfull_pt for row in documents), default=0.0),
        "contact_sheets": [relative(path) for path in contact_paths],
        "manual_review": {
            "completed": len(manual_rows) == len(documents),
            "documents": len(manual_rows),
            "status_counts": dict(manual_counts),
        },
    }
    (args.out / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Expansion-32 reference visual audit",
        "",
        "This audit covers only the 32 newly added references named in",
        "`data/latex_benchmark_v0/splits/expansion_32.csv` and every one of",
        "their rendered pages. The original 157 references are not included.",
        "Automatic flags are triage signals; acceptance requires recording the",
        "manual contact-sheet decision separately.",
        "",
        f"- Documents: {len(documents)}",
        f"- Pages: {len(pages)}",
        f"- Render DPI: {args.render_dpi}",
        f"- Auto-clear: {status_counts.get('clear', 0)}",
        f"- Needs review: {status_counts.get('review', 0)}",
        f"- Automatic failures: {status_counts.get('fail', 0)}",
        f"- Documents with TeX overfull warnings: "
        f"{sum(row.overfull_warning_count > 0 for row in documents)}",
        f"- Largest reported overfull amount: {summary['max_overfull_pt']:.3f} pt",
        f"- Manually reviewed: {len(manual_rows)}/{len(documents)}",
        f"- Manual passes: {manual_counts.get('pass', 0)}",
        f"- Manual failures: {manual_counts.get('fail', 0)}",
        "",
        "## By category",
        "",
        "| Category | Documents | Clear | Review | Fail |",
        "|---|---:|---:|---:|---:|",
    ]
    for category in sorted(category_counts):
        counts = category_counts[category]
        lines.append(
            f"| `{category}` | {sum(counts.values())} | {counts.get('clear', 0)} | "
            f"{counts.get('review', 0)} | {counts.get('fail', 0)} |"
        )
    lines.extend(
        [
            "",
            "## Flagged documents",
            "",
            "| Sample | Category | Status | Max overfull | Flags |",
            "|---|---|---|---:|---|",
        ]
    )
    for row in documents:
        if row.auto_status == "clear":
            continue
        lines.append(
            f"| `{row.sample_id}` | `{row.category}` | `{row.auto_status}` | "
            f"{row.max_overfull_pt:.3f} pt | {row.flags or '-'} |"
        )
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- `document_audit.csv`: one automatic QA record per expansion document.",
            "- `page_audit.csv`: one automatic QA record per rendered reference page.",
            "- `contact_sheets/`: every reference page, labeled and rendered for review.",
            "- `manual_review.csv`: reviewer disposition; created after contact-sheet review.",
        ]
    )
    (args.out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    parser.add_argument("--render-dpi", type=int, default=110)
    parser.add_argument("--sheet-columns", type=int, default=4)
    parser.add_argument("--sheet-rows", type=int, default=4)
    args = parser.parse_args()
    args.dataset = args.dataset.resolve()
    args.split = args.split.resolve()
    args.out = args.out.resolve()
    if args.render_dpi < 72:
        parser.error("--render-dpi must be at least 72")
    return args


def main() -> None:
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    documents, pages, contact_paths = audit(args)
    write_reports(args, documents, pages, contact_paths)


if __name__ == "__main__":
    main()
