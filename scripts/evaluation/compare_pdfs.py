"""Compare any two PDFs and emit metrics plus labeled visual diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pdf_fidelity import (
    METRIC_CONFIG,
    SCORECARD_CONFIG,
    compare_pdfs,
    create_diagnostic_images,
    public_result,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    result, reference, candidate, diffs = compare_pdfs(args.reference, args.candidate)
    assets = create_diagnostic_images(result, reference, candidate, diffs, args.out_dir)
    payload = public_result(result)
    payload["diagnostic_assets"] = assets
    (args.out_dir / "metrics.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (args.out_dir / "metric_config.json").write_text(json.dumps(METRIC_CONFIG, indent=2) + "\n", encoding="utf-8")
    (args.out_dir / "scorecard_config.json").write_text(
        json.dumps(SCORECARD_CONFIG, indent=2) + "\n", encoding="utf-8"
    )
    scores = payload["scores"]
    print(f"overall={100 * scores['overall']:.1f}")
    print(f"visual={100 * scores['visual']:.1f}")
    print(f"content={100 * scores['content']:.1f}")
    print(f"scorecard_status={payload['scorecard']['status']}")
    if payload["scorecard"]["failed_gates"]:
        print(f"failed_gates={','.join(payload['scorecard']['failed_gates'])}")
    print(f"metrics={args.out_dir / 'metrics.json'}")


if __name__ == "__main__":
    main()
