#!/usr/bin/env python3
"""Render the boxed PDF excerpts used by the current fidelity report."""

from __future__ import annotations

import json
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "assets" / "pdf_fidelity_v3"

COLORS = {
    "reference": "#147A7E",
    "candidate": "#B04A35",
    "automatic": "#C9881C",
    "expected": "#72777A",
}


def dashed_rectangle(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, width: int) -> None:
    x0, y0, x1, y1 = xy
    dash = 14
    gap = 8
    for start in range(x0, x1, dash + gap):
        draw.line((start, y0, min(start + dash, x1), y0), fill=fill, width=width)
        draw.line((start, y1, min(start + dash, x1), y1), fill=fill, width=width)
    for start in range(y0, y1, dash + gap):
        draw.line((x0, start, x0, min(start + dash, y1)), fill=fill, width=width)
        draw.line((x1, start, x1, min(start + dash, y1)), fill=fill, width=width)


def render(spec: dict) -> dict:
    doc = fitz.open(ROOT / spec["pdf"])
    page = doc[spec["page"] - 1]
    page_rect = page.rect
    crop_n = spec.get("crop")
    if crop_n is None and spec.get("auto_crop"):
        x0 = min(box["bbox"][0] for box in spec["boxes"])
        y0 = min(box["bbox"][1] for box in spec["boxes"])
        x1 = max(box["bbox"][2] for box in spec["boxes"])
        y1 = max(box["bbox"][3] for box in spec["boxes"])
        width = max(x1 - x0 + 0.10, 0.34)
        height = max(y1 - y0 + 0.07, 0.11)
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        crop_n = [max(0, cx - width / 2), max(0, cy - height / 2), min(1, cx + width / 2), min(1, cy + height / 2)]
    if crop_n is None:
        crop_n = [0, 0, 1, 1]
    crop = fitz.Rect(
        crop_n[0] * page_rect.width,
        crop_n[1] * page_rect.height,
        crop_n[2] * page_rect.width,
        crop_n[3] * page_rect.height,
    )
    zoom = spec.get("zoom", 3.0)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=crop, alpha=False)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    draw = ImageDraw.Draw(image)
    stroke = max(4, round(2.0 * zoom))

    for box in spec.get("boxes", []):
        x0, y0, x1, y1 = box["bbox"]
        px = (
            round((x0 * page_rect.width - crop.x0) * zoom),
            round((y0 * page_rect.height - crop.y0) * zoom),
            round((x1 * page_rect.width - crop.x0) * zoom),
            round((y1 * page_rect.height - crop.y0) * zoom),
        )
        color = COLORS[box["kind"]]
        if box.get("dashed", box["kind"] in {"reference", "expected"}):
            dashed_rectangle(draw, px, color, stroke)
        else:
            draw.rectangle(px, outline=color, width=stroke)

    out_path = OUT / f"{spec['name']}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path, optimize=True)
    return {
        "name": spec["name"],
        "pdf": spec["pdf"],
        "page": spec["page"],
        "crop_normalized": crop_n,
        "boxes": spec.get("boxes", []),
        "output": str(out_path.relative_to(ROOT)),
        "pixel_size": [image.width, image.height],
    }


SPECS = [
    {
        "name": "strict_math_reference",
        "pdf": "data/latex_benchmark_v0/corpus/03_math_inline_display/03_math_inline_display_005/reference.pdf",
        "page": 1,
        "crop": [0.14, 0.285, 0.91, 0.39],
        "boxes": [{"kind": "reference", "bbox": [0.197307, 0.320289, 0.857540, 0.354085]}],
    },
    {
        "name": "strict_math_candidate",
        "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v2_heldout_v1_failures/samples/03_math_inline_display_005/output.pdf",
        "page": 1,
        "crop": [0.0, 0.165, 1.0, 0.245],
        "boxes": [{"kind": "candidate", "bbox": [0.0, 0.197593, 1.0, 0.210659]}],
    },
    {
        "name": "citation_reference",
        "pdf": "data/latex_benchmark_v0/corpus/08_crossrefs_citations/08_crossrefs_citations_004/reference.pdf",
        "page": 1,
        "crop": [0.28, 0.318, 0.50, 0.397],
        "boxes": [{"kind": "reference", "bbox": [0.346364, 0.350145, 0.427184, 0.363919]}],
    },
    {
        "name": "citation_candidate",
        "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_heldout_clean/samples/08_crossrefs_citations_004/output.pdf",
        "page": 1,
        "crop": [0.30, 0.258, 0.61, 0.34],
        "boxes": [{"kind": "candidate", "bbox": [0.364226, 0.292412, 0.542122, 0.305478]}],
    },
    {
        "name": "date_reference",
        "pdf": "data/latex_benchmark_v0/corpus/11_forms_cv_letters/11_forms_cv_letters_007/reference.pdf",
        "page": 1,
        "crop": [0.70, 0.305, 0.92, 0.385],
        "boxes": [
            {"kind": "reference", "bbox": [0.765480, 0.337711, 0.790625, 0.351912]},
            {"kind": "reference", "bbox": [0.797172, 0.337711, 0.829125, 0.351912]},
            {"kind": "reference", "bbox": [0.835692, 0.337711, 0.875056, 0.351912]},
        ],
    },
    {
        "name": "date_candidate_absent",
        "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/11_forms_cv_letters_007/output.pdf",
        "page": 1,
        "crop": [0.70, 0.305, 0.92, 0.385],
        "boxes": [{"kind": "expected", "bbox": [0.765480, 0.337711, 0.875056, 0.351912]}],
    },
    {
        "name": "geometry_address_reference",
        "pdf": "data/latex_benchmark_v0/corpus/11_forms_cv_letters/11_forms_cv_letters_007/reference.pdf",
        "page": 1,
        "crop": [0.055, 0.18, 0.32, 0.30],
        "boxes": [{"kind": "reference", "bbox": [0.095238, 0.214061, 0.270828, 0.262578]}],
    },
    {
        "name": "geometry_address_candidate",
        "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/11_forms_cv_letters_007/output.pdf",
        "page": 1,
        "crop": [0.70, 0.05, 0.95, 0.16],
        "boxes": [{"kind": "candidate", "bbox": [0.750002, 0.081092, 0.904762, 0.130167]}],
    },
    {
        "name": "ltsim_flow_reference",
        "pdf": "data/latex_benchmark_v0/corpus/11_forms_cv_letters/11_forms_cv_letters_007/reference.pdf",
        "page": 1,
        "crop": [0.08, 0.44, 0.44, 0.52],
        "boxes": [{"kind": "automatic", "bbox": [0.124999, 0.474981, 0.383393, 0.489181]}],
    },
    {
        "name": "ltsim_flow_candidate",
        "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/11_forms_cv_letters_007/output.pdf",
        "page": 1,
        "crop": [0.72, 0.05, 0.95, 0.13],
        "boxes": [{"kind": "automatic", "bbox": [0.764156, 0.081092, 0.904762, 0.095987]}],
    },
    {
        "name": "pagination_reference",
        "pdf": "data/latex_benchmark_v0/corpus/04_math_aligned/04_math_aligned_014/reference.pdf",
        "page": 2,
        "crop": [0.17, 0.118, 0.83, 0.205],
        "boxes": [{"kind": "reference", "bbox": [0.235322, 0.153548, 0.764705, 0.168755]}],
    },
    {
        "name": "pagination_candidate",
        "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/04_math_aligned_014/output.pdf",
        "page": 1,
        "crop": [0.16, 0.315, 0.85, 0.395],
        "boxes": [{"kind": "candidate", "bbox": [0.218589, 0.350028, 0.787546, 0.357794]}],
    },
    {
        "name": "typography_reference",
        "pdf": "data/latex_benchmark_v0/corpus/05_tables_simple/05_tables_simple_025/reference.pdf",
        "page": 3,
        "crop": [0.29, 0.33, 0.55, 0.45],
        "boxes": [{"kind": "reference", "bbox": [0.352132, 0.374740, 0.489430, 0.407027]}],
    },
    {
        "name": "typography_candidate",
        "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_heldout_clean/samples/05_tables_simple_025/output.pdf",
        "page": 3,
        "crop": [0.39, 0.17, 0.57, 0.27],
        "boxes": [{"kind": "candidate", "bbox": [0.445183, 0.214666, 0.506274, 0.227732]}],
    },
    {
        "name": "ssim_collision_reference",
        "pdf": "data/latex_benchmark_v0/corpus/06_tables_moderate/06_tables_moderate_008/reference.pdf",
        "page": 2,
        "crop": [0.06, 0.84, 0.94, 1.0],
        "boxes": [{"kind": "reference", "bbox": [0.117647, 0.883838, 0.875817, 0.999369]}],
    },
    {
        "name": "ssim_collision_candidate",
        "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_heldout_clean/samples/06_tables_moderate_008/output.pdf",
        "page": 2,
        "crop": [0.10, 0.85, 0.90, 0.99],
        "boxes": [{"kind": "candidate", "bbox": [0.179739, 0.895202, 0.820261, 0.965278]}],
    },
    {
        "name": "corrupt_row_reference",
        "pdf": "data/latex_benchmark_v0/corpus/05_tables_simple/05_tables_simple_023/reference.pdf",
        "page": 3,
        "crop": [0.08, 0.41, 0.87, 0.57],
        "boxes": [{"kind": "reference", "bbox": [0.117647, 0.454940, 0.824778, 0.527329]}],
    },
    {
        "name": "corrupt_row_candidate",
        "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_023/claude-opus-4-7.pdf",
        "page": 3,
        "crop": [0.24, 0.22, 0.76, 0.32],
        "boxes": [{"kind": "candidate", "bbox": [0.296242, 0.264112, 0.703758, 0.278001]}],
    },
]


COMPARISONS = {
    "math014": {
        "reference": {
            "pdf": "data/latex_benchmark_v0/corpus/04_math_aligned/04_math_aligned_014/reference.pdf",
            "page": 2,
            "bbox": [0.235322, 0.153548, 0.764705, 0.168755],
        },
        "gemini": {
            "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/04_math_aligned_014/output.pdf",
            "page": 1,
            "bbox": [0.218589, 0.700100, 0.787546, 0.713100],
        },
        "sonnet": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/04_math_aligned_014/claude-sonnet-4-6.pdf",
            "page": 1,
            "bbox": [0.223300, 0.853100, 0.787500, 0.867000],
        },
        "opus": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/04_math_aligned_014/claude-opus-4-7.pdf",
            "page": 1,
            "bbox": [0.223300, 0.784100, 0.787500, 0.798000],
        },
    },
    "table005": {
        "reference": {
            "pdf": "data/latex_benchmark_v0/corpus/05_tables_simple/05_tables_simple_005/reference.pdf",
            "page": 1,
            "bbox": [0.123700, 0.829400, 0.578500, 0.837300],
        },
        "gemini": {
            "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/05_tables_simple_005/output.pdf",
            "page": 2,
            "bbox": [0.143800, 0.917200, 0.804300, 0.949300],
        },
        "sonnet": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_005/claude-sonnet-4-6.pdf",
            "page": 1,
            "bbox": [0.122500, 0.885000, 0.618300, 0.892600],
        },
        "opus": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_005/claude-opus-4-7.pdf",
            "page": 1,
            "bbox": [0.124200, 0.890000, 0.597700, 0.898200],
        },
    },
    "table021": {
        "reference": {
            "pdf": "data/latex_benchmark_v0/corpus/05_tables_simple/05_tables_simple_021/reference.pdf",
            "page": 2,
            "bbox": [0.323500, 0.102200, 0.676400, 0.116000],
        },
        "gemini": {
            "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/05_tables_simple_021/output.pdf",
            "page": 1,
            "bbox": [0.339100, 0.755700, 0.660900, 0.770600],
        },
        "sonnet": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_021/claude-sonnet-4-6.pdf",
            "page": 2,
            "bbox": [0.323500, 0.089200, 0.676500, 0.103100],
        },
        "opus": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_021/claude-opus-4-7.pdf",
            "page": 2,
            "bbox": [0.323500, 0.089200, 0.676500, 0.103100],
        },
    },
    "table023": {
        "reference": {
            "pdf": "data/latex_benchmark_v0/corpus/05_tables_simple/05_tables_simple_023/reference.pdf",
            "page": 3,
            "bbox": [0.117600, 0.936100, 0.824800, 1.000000],
        },
        "gemini": {
            "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/05_tables_simple_023/output.pdf",
            "page": 2,
            "bbox": [0.359000, 0.539200, 0.632400, 0.595000],
        },
        "sonnet": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_023/claude-sonnet-4-6.pdf",
            "page": 3,
            "bbox": [0.127500, 0.385600, 0.429600, 0.423500],
        },
        "opus": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_023/claude-opus-4-7.pdf",
            "page": 3,
            "bbox": [0.296200, 0.264100, 0.617400, 0.278000],
            "extra_boxes": [{"kind": "automatic", "bbox": [0.435600, 0.266900, 0.556800, 0.278000]}],
        },
    },
    "table010": {
        "reference": {
            "pdf": "data/latex_benchmark_v0/corpus/06_tables_moderate/06_tables_moderate_010/reference.pdf",
            "page": 1,
            "bbox": [0.143900, 0.791700, 0.860900, 0.810700],
        },
        "gemini": {
            "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_v0_failures/samples/06_tables_moderate_010/output.pdf",
            "page": 2,
            "bbox": [0.110000, 0.918800, 0.850700, 1.000000],
        },
        "sonnet": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/06_tables_moderate_010/claude-sonnet-4-6.pdf",
            "page": 1,
            "bbox": [0.140600, 0.662000, 0.860000, 0.677000],
        },
        "opus": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/06_tables_moderate_010/claude-opus-4-7.pdf",
            "page": 1,
            "bbox": [0.163600, 0.768000, 0.840000, 0.786000],
        },
    },
    "figure007": {
        "reference": {
            "pdf": "data/latex_benchmark_v0/corpus/07_figures_captions/07_figures_captions_007/reference.pdf",
            "page": 1,
            "bbox": [0.368600, 0.433600, 0.506600, 0.447400],
            "extra_boxes": [{"kind": "automatic", "bbox": [0.368600, 0.433600, 0.506600, 0.447400]}],
        },
        "gemini": {
            "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/07_figures_captions_007/output.pdf",
            "page": 1,
            "bbox": [0.123200, 0.309500, 0.191100, 0.324200],
            "extra_boxes": [{"kind": "automatic", "bbox": [0.123200, 0.309500, 0.191100, 0.324200]}],
        },
        "sonnet": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/07_figures_captions_007/claude-sonnet-4-6.pdf",
            "page": 1,
            "bbox": [0.390400, 0.397750, 0.513430, 0.411640],
        },
        "opus": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/07_figures_captions_007/claude-opus-4-7.pdf",
            "page": 1,
            "bbox": [0.390400, 0.432460, 0.513430, 0.446350],
        },
    },
    "algorithm003": {
        "reference": {
            "pdf": "data/latex_benchmark_v0/corpus/09_algorithms/09_algorithms_003/reference.pdf",
            "page": 2,
            "bbox": [0.117600, 0.143900, 0.592600, 0.157700],
            "extra_boxes": [{"kind": "automatic", "bbox": [0.117600, 0.143900, 0.226200, 0.157700]}],
        },
        "gemini": {
            "pdf": "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_v0_failures/samples/09_algorithms_003/output.pdf",
            "page": 1,
            "bbox": [0.272500, 0.822300, 0.727500, 0.835400],
            "extra_boxes": [{"kind": "automatic", "bbox": [0.272500, 0.822300, 0.345200, 0.835400]}],
        },
        "sonnet": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/09_algorithms_003/claude-sonnet-4-6.pdf",
            "page": 2,
            "bbox": [0.117600, 0.093200, 0.564000, 0.105800],
        },
        "opus": {
            "pdf": "results/metric_calibration/canonical_ai_v0_3/compiled/canonical/09_algorithms_003/claude-opus-4-7.pdf",
            "page": 2,
            "bbox": [0.117600, 0.110100, 0.599700, 0.124000],
        },
    },
}

for sample, roles in COMPARISONS.items():
    for role, item in roles.items():
        kind = "reference" if role == "reference" else "candidate"
        box = {"kind": kind, "bbox": item["bbox"]}
        boxes = [box] + item.get("extra_boxes", [])
        SPECS.append(
            {
                "name": f"grid_{sample}_{role}",
                "pdf": item["pdf"],
                "page": item["page"],
                "zoom": 1.6,
                "boxes": boxes,
            }
        )
        SPECS.append(
            {
                "name": f"detail_{sample}_{role}",
                "pdf": item["pdf"],
                "page": item["page"],
                "auto_crop": True,
                "boxes": boxes,
            }
        )


def main() -> None:
    rendered = [render(spec) for spec in SPECS]
    (OUT / "manifest.json").write_text(json.dumps(rendered, indent=2) + "\n", encoding="utf-8")
    print(f"rendered {len(rendered)} assets to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
