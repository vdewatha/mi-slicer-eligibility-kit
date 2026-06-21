"""CLI entry points for MedAsset pipeline."""

from __future__ import annotations

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from medasset.export_dicom_seg import export_label_as_dicom_seg, run_export
from medasset.figures import run_figures, save_qc_summary_png
from medasset.infer import run_inference
from medasset.ingest import run_ingest
from medasset.io import read_json
from medasset.metrics import run_metrics
from medasset.qc import run_qc
from medasset.synthetic import create_synthetic_case

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "data"
DEFAULT_ASSETS = ROOT / "portfolio" / "assets"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="medasset")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ingest")
    qc_p = sub.add_parser("qc")
    qc_p.add_argument("--output", type=Path, default=DEFAULT_ASSETS / "qc-report.json")
    sub.add_parser("infer")
    metrics_p = sub.add_parser("metrics")
    metrics_p.add_argument("--output", type=Path, default=DEFAULT_ASSETS / "segmentation-metrics.json")
    export_p = sub.add_parser("export")
    export_p.add_argument("--output-dir", type=Path, default=None)
    figures_p = sub.add_parser("figures")
    figures_p.add_argument("--output-dir", type=Path, default=DEFAULT_ASSETS)
    validate_p = sub.add_parser("validate")
    validate_p.add_argument("--golden", type=Path, default=DEFAULT_ASSETS / "segmentation-metrics.json")
    validate_p.add_argument("--tolerance", type=float, default=0.15)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    data_dir: Path = args.data_dir

    if args.command == "ingest":
        result = run_ingest(data_dir)
        print(json.dumps(result, indent=2))
        return 0 if result["count"] > 0 else 1

    if args.command == "qc":
        report = run_qc(data_dir, args.output)
        save_qc_summary_png(report, args.output.parent / "qc-summary.png")
        print(json.dumps({"passed": report["passed"], "failed": report["failed"]}, indent=2))
        return 0

    if args.command == "infer":
        result = run_inference(data_dir)
        print(json.dumps(result, indent=2))
        return 0

    if args.command == "metrics":
        result = run_metrics(data_dir, args.output)
        print(json.dumps(result.get("aggregate", {}), indent=2))
        return 0

    if args.command == "export":
        out_dir = args.output_dir or data_dir / "exports"
        result = run_export(data_dir, out_dir)
        # Copy sample SEG to portfolio assets
        exports = out_dir
        cases = result.get("exported_cases", [])
        if cases:
            src = exports / f"{cases[0]}_seg.dcm"
            dst = DEFAULT_ASSETS / "sample-spleen.dcm"
            DEFAULT_ASSETS.mkdir(parents=True, exist_ok=True)
            if src.exists():
                shutil.copy(src, dst)
        print(json.dumps(result, indent=2))
        return 0

    if args.command == "figures":
        result = run_figures(data_dir, args.output_dir)
        print(json.dumps(result, indent=2))
        return 0

    if args.command == "validate":
        metrics_path = DEFAULT_ASSETS / "segmentation-metrics.json"
        run_metrics(data_dir, metrics_path)
        current = read_json(metrics_path)
        golden_path = args.golden
        if golden_path.exists():
            golden = read_json(golden_path)
            g_dice = golden.get("aggregate", {}).get("mean_dice_corrected", 0)
            c_dice = current.get("aggregate", {}).get("mean_dice_corrected", 0)
            if abs(g_dice - c_dice) > args.tolerance and g_dice > 0:
                print(f"Metrics drift: golden={g_dice}, current={c_dice}", file=sys.stderr)
                return 1
        corr = current.get("aggregate", {}).get("mean_dice_corrected", 0)
        if corr < 0.5:
            print(f"Dice too low: {corr}", file=sys.stderr)
            return 1
        print(json.dumps({"status": "ok", "mean_dice_corrected": corr}, indent=2))
        return 0

    return 1


# Console script entry points
def cmd_ingest() -> None:
    sys.exit(main(["ingest"]))


def cmd_qc() -> None:
    sys.exit(main(["qc"]))


def cmd_infer() -> None:
    sys.exit(main(["infer"]))


def cmd_metrics() -> None:
    sys.exit(main(["metrics"]))


def cmd_export() -> None:
    sys.exit(main(["export"]))


def cmd_figures() -> None:
    sys.exit(main(["figures"]))


if __name__ == "__main__":
    sys.exit(main())
