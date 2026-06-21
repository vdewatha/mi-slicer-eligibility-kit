"""Segmentation metrics: Dice, HD95."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import SimpleITK as sitk
from scipy import ndimage
from scipy.ndimage import distance_transform_edt

from medasset.io import list_cases, write_json

logger = logging.getLogger(__name__)


def dice_coefficient(pred: np.ndarray, ref: np.ndarray) -> float:
    pred_bin = pred > 0
    ref_bin = ref > 0
    intersection = np.logical_and(pred_bin, ref_bin).sum()
    union = pred_bin.sum() + ref_bin.sum()
    if union == 0:
        return 1.0
    return float(2.0 * intersection / union)


def hausdorff_95(pred: np.ndarray, ref: np.ndarray, spacing: tuple[float, ...]) -> float:
    """Approximate 95th percentile Hausdorff distance in mm."""
    pred_bin = pred > 0
    ref_bin = ref > 0
    if not pred_bin.any() or not ref_bin.any():
        return float("inf")

    spacing_zyx = spacing[::-1] if len(spacing) == 3 else (1.0, 1.0, 1.0)

    def surface_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        dt = distance_transform_edt(~b, sampling=spacing_zyx)
        eroded = ndimage.binary_erosion(a)
        border = np.logical_and(a, ~eroded)
        if not border.any():
            border = a
        return dt[border]

    d1 = surface_distances(pred_bin, ref_bin)
    d2 = surface_distances(ref_bin, pred_bin)
    all_d = np.concatenate([d1, d2])
    return float(np.percentile(all_d, 95))


def compute_metrics(pred_path: Path, ref_path: Path) -> dict[str, float]:
    pred_img = sitk.ReadImage(str(pred_path))
    ref_img = sitk.ReadImage(str(ref_path))
    pred = sitk.GetArrayFromImage(pred_img)
    ref = sitk.GetArrayFromImage(ref_img)
    spacing = pred_img.GetSpacing()
    dice = dice_coefficient(pred, ref)
    hd95 = hausdorff_95(pred, ref, spacing)
    return {"dice": round(dice, 4), "hd95_mm": round(hd95, 4)}


def run_metrics(data_dir: Path, output_path: Path | None = None) -> dict[str, Any]:
    """Compare inference vs reference and expert-corrected vs reference."""
    processed = data_dir / "processed"
    ref_dir = data_dir / "labels" / "reference"
    infer_dir = data_dir / "inference"
    expert_dir = data_dir / "labels" / "expert"

    cases = list_cases(processed)
    case_metrics: list[dict[str, Any]] = []

    for case_id in cases:
        ref_path = ref_dir / f"{case_id}.nii.gz"
        if not ref_path.exists():
            continue

        entry: dict[str, Any] = {"case_id": case_id}
        ai_path = infer_dir / f"{case_id}.nii.gz"
        expert_path = expert_dir / f"{case_id}.nii.gz"

        if ai_path.exists():
            ai_m = compute_metrics(ai_path, ref_path)
            entry["ai_only"] = ai_m
        if expert_path.exists():
            entry["expert_corrected"] = compute_metrics(expert_path, ref_path)
        elif ai_path.exists():
            # Use AI as corrected when no separate expert label (synthetic demo)
            entry["expert_corrected"] = compute_metrics(ai_path, ref_path)

        case_metrics.append(entry)

    summary = {
        "cases": case_metrics,
        "aggregate": _aggregate(case_metrics),
    }

    if output_path:
        write_json(output_path, summary)
        logger.info("Metrics written to %s", output_path)

    return summary


def _aggregate(case_metrics: list[dict]) -> dict[str, float]:
    ai_dice = [c["ai_only"]["dice"] for c in case_metrics if "ai_only" in c]
    corr_dice = [c["expert_corrected"]["dice"] for c in case_metrics if "expert_corrected" in c]
    return {
        "mean_dice_ai": round(float(np.mean(ai_dice)), 4) if ai_dice else 0.0,
        "mean_dice_corrected": round(float(np.mean(corr_dice)), 4) if corr_dice else 0.0,
    }
