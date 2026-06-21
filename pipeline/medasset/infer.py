"""AI-assisted segmentation inference (classical baseline + optional refinement)."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import SimpleITK as sitk
from scipy import ndimage

from medasset.io import ensure_dir, list_cases, save_label

logger = logging.getLogger(__name__)


def classical_spleen_segmentation(image: sitk.Image) -> sitk.Image:
    """
    SimpleITK baseline: HU threshold + connected components + largest component.
    Mimics a coarse AI draft mask for human-in-the-loop correction demos.
    """
    arr = sitk.GetArrayFromImage(image)
    # Spleen typically 30-70 HU in contrast-enhanced CT; use wider range for robustness
    mask = (arr > -50) & (arr < 150)
    mask = ndimage.binary_opening(mask, iterations=1)
    mask = ndimage.binary_closing(mask, iterations=2)

    labeled, n = ndimage.label(mask)
    if n == 0:
        result = np.zeros_like(arr, dtype=np.uint8)
    else:
        sizes = ndimage.sum(mask, labeled, range(1, n + 1))
        # Pick largest component in upper abdomen region (heuristic for demo)
        largest = int(np.argmax(sizes)) + 1
        result = (labeled == largest).astype(np.uint8)

    out = sitk.GetImageFromArray(result)
    out.CopyInformation(image)
    return sitk.Cast(out, sitk.sitkUInt8)


def simulate_ai_correction(draft: sitk.Image, reference: sitk.Image | None) -> sitk.Image:
    """
    Simulate expert correction by morphologically refining draft toward reference.
    In real workflow, correction happens in 3D Slicer Segment Editor.
    """
    draft_arr = sitk.GetArrayFromImage(draft) > 0
    if reference is not None:
        ref_arr = sitk.GetArrayFromImage(reference) > 0
        # Blend: union with reference erosion to simulate expert fix
        corrected = np.logical_or(draft_arr, ndimage.binary_erosion(ref_arr, iterations=1))
        corrected = ndimage.binary_closing(corrected, iterations=1)
    else:
        corrected = ndimage.binary_closing(draft_arr, iterations=2)

    out = sitk.GetImageFromArray(corrected.astype(np.uint8))
    out.CopyInformation(draft)
    return sitk.Cast(out, sitk.sitkUInt8)


def run_inference(data_dir: Path, backend: str = "classical") -> dict:
    """
    Run inference on all processed cases.
    backend: 'classical' (default, no GPU) or 'nnunet' (requires nnU-Net install).
    """
    processed = data_dir / "processed"
    infer_dir = data_dir / "inference"
    expert_dir = data_dir / "labels" / "expert"
    ref_dir = data_dir / "labels" / "reference"
    ensure_dir(infer_dir)
    ensure_dir(expert_dir)

    cases = list_cases(processed)
    results = []

    for case_id in cases:
        image_path = processed / f"{case_id}.nii.gz"
        image = sitk.ReadImage(str(image_path))

        if backend == "nnunet":
            draft = _try_nnunet(image, data_dir, case_id)
            if draft is None:
                logger.warning("nnU-Net unavailable; falling back to classical for %s", case_id)
                draft = classical_spleen_segmentation(image)
        else:
            draft = classical_spleen_segmentation(image)

        save_label(draft, infer_dir / f"{case_id}.nii.gz")

        ref_path = ref_dir / f"{case_id}.nii.gz"
        reference = sitk.ReadImage(str(ref_path)) if ref_path.exists() else None
        corrected = simulate_ai_correction(draft, reference)
        save_label(corrected, expert_dir / f"{case_id}.nii.gz")

        results.append({"case_id": case_id, "backend": backend})
        logger.info("Inference complete: %s", case_id)

    return {"inferred_cases": results, "count": len(results)}


def _try_nnunet(image: sitk.Image, data_dir: Path, case_id: str) -> sitk.Image | None:
    """Attempt nnU-Net v2 inference if installed; return None if unavailable."""
    import shutil
    import subprocess
    import tempfile

    if not shutil.which("nnUNetv2_predict"):
        return None

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()
        sitk.WriteImage(image, str(input_dir / f"{case_id}_0000.nii.gz"))
        try:
            subprocess.run(
                [
                    "nnUNetv2_predict",
                    "-i", str(input_dir),
                    "-o", str(output_dir),
                    "-d", "09",
                    "-c", "3d_fullres",
                    "-f", "0",
                ],
                check=True,
                capture_output=True,
            )
            pred_path = output_dir / f"{case_id}.nii.gz"
            if pred_path.exists():
                return sitk.ReadImage(str(pred_path))
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    return None
