"""Automated QC checks for CT volumes."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import SimpleITK as sitk

from medasset.io import ensure_dir, list_cases, write_json

logger = logging.getLogger(__name__)

HU_MIN_EXPECTED = -1024
HU_MAX_EXPECTED = 3071
SPACING_TOLERANCE = 0.5
MIN_SLICES = 10


def _check_volume(image: sitk.Image, case_id: str) -> dict[str, Any]:
    arr = sitk.GetArrayFromImage(image)
    spacing = image.GetSpacing()
    size = image.GetSize()
    hu_min = float(np.min(arr))
    hu_max = float(np.max(arr))
    slice_gaps_ok = len(spacing) >= 3 and spacing[2] < 10.0

    issues: list[str] = []
    if hu_min < HU_MIN_EXPECTED - 500 or hu_max > HU_MAX_EXPECTED + 500:
        issues.append(f"HU range unusual: [{hu_min:.1f}, {hu_max:.1f}]")
    if size[2] < MIN_SLICES:
        issues.append(f"Low slice count: {size[2]}")
    if not slice_gaps_ok:
        issues.append(f"Slice spacing suspicious: {spacing[2]:.2f} mm")
    if np.any(~np.isfinite(arr)):
        issues.append("Non-finite voxel values detected")

    status = "pass" if not issues else "fail"
    return {
        "case_id": case_id,
        "status": status,
        "issues": issues,
        "spacing_mm": [round(s, 4) for s in spacing],
        "size_voxels": list(size),
        "hu_range": [round(hu_min, 2), round(hu_max, 2)],
        "orientation": list(image.GetDirection()),
    }


def run_qc(data_dir: Path, output_path: Path | None = None) -> dict[str, Any]:
    """Run QC on all processed cases."""
    processed = data_dir / "processed"
    cases = list_cases(processed)
    results = [_check_volume(sitk.ReadImage(str(processed / f"{c}.nii.gz")), c) for c in cases]

    summary: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pipeline_version": "1.0.0",
        "total_cases": len(results),
        "passed": sum(1 for r in results if r["status"] == "pass"),
        "failed": sum(1 for r in results if r["status"] == "fail"),
        "cases": results,
    }

    if output_path:
        write_json(output_path, summary)
        logger.info("QC report written to %s", output_path)

    return summary
