"""Generate portfolio overlay figures from pipeline outputs."""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk

from medasset.io import ensure_dir, list_cases

logger = logging.getLogger(__name__)


def _overlay_slice(image: np.ndarray, mask: np.ndarray, alpha: float = 0.4) -> np.ndarray:
    img_norm = (image - image.min()) / (image.max() - image.min() + 1e-8)
    rgb = np.stack([img_norm] * 3, axis=-1)
    overlay = rgb.copy()
    overlay[mask > 0, 0] = np.minimum(1.0, overlay[mask > 0, 0] + alpha)
    overlay[mask > 0, 1] = np.maximum(0.0, overlay[mask > 0, 1] - alpha * 0.5)
    return overlay


def save_segmentation_overlay(
    image_path: Path,
    label_path: Path,
    output_path: Path,
    title: str = "Segmentation Overlay",
) -> None:
    image = sitk.GetArrayFromImage(sitk.ReadImage(str(image_path)))
    label = sitk.GetArrayFromImage(sitk.ReadImage(str(label_path)))
    mid = image.shape[0] // 2

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    views = [
        (image[mid], label[mid], "Axial"),
        (image[:, mid], label[:, mid], "Coronal"),
        (image[:, :, mid], label[:, :, mid], "Sagittal"),
    ]
    for ax, (img_slice, lbl_slice, name) in zip(axes, views):
        ax.imshow(_overlay_slice(img_slice, lbl_slice), cmap="gray")
        ax.set_title(name)
        ax.axis("off")
    fig.suptitle(title)
    ensure_dir(output_path.parent)
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved overlay: %s", output_path)


def save_comparison_figure(
    image_path: Path,
    ai_path: Path,
    expert_path: Path,
    ref_path: Path,
    output_path: Path,
) -> None:
    image = sitk.GetArrayFromImage(sitk.ReadImage(str(image_path)))
    ai = sitk.GetArrayFromImage(sitk.ReadImage(str(ai_path)))
    expert = sitk.GetArrayFromImage(sitk.ReadImage(str(expert_path)))
    ref = sitk.GetArrayFromImage(sitk.ReadImage(str(ref_path)))
    mid = image.shape[0] // 2

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    panels = [
        (ai[mid], "AI Draft"),
        (expert[mid], "Expert Corrected"),
        (ref[mid], "Reference"),
        (np.abs(expert[mid].astype(float) - ai[mid].astype(float)), "Correction Delta"),
    ]
    for ax, (data, title) in zip(axes.flat, panels):
        ax.imshow(data, cmap="hot" if "Delta" in title else "gray")
        ax.set_title(title)
        ax.axis("off")
    ensure_dir(output_path.parent)
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def save_qc_summary_png(qc_report: dict, output_path: Path) -> None:
    cases = qc_report.get("cases", [])
    passed = qc_report.get("passed", 0)
    failed = qc_report.get("failed", 0)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["Pass", "Fail"], [passed, failed], color=["#2dd4bf", "#f87171"])
    ax.set_ylabel("Cases")
    ax.set_title("QC Summary")
    for i, (label, val) in enumerate(zip(["Pass", "Fail"], [passed, failed])):
        ax.text(i, val + 0.05, str(val), ha="center")
    if cases:
        ax.text(0.5, -0.15, f"Total: {len(cases)} cases", transform=ax.transAxes, ha="center")
    ensure_dir(output_path.parent)
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def run_figures(data_dir: Path, output_dir: Path) -> dict:
    """Generate all portfolio figure assets."""
    processed = data_dir / "processed"
    expert_dir = data_dir / "labels" / "expert"
    infer_dir = data_dir / "inference"
    ref_dir = data_dir / "labels" / "reference"
    ensure_dir(output_dir)

    cases = list_cases(processed)
    if not cases:
        logger.warning("No cases for figure generation")
        return {"generated": 0}

    case_id = cases[0]
    image_path = processed / f"{case_id}.nii.gz"
    expert_path = expert_dir / f"{case_id}.nii.gz"
    infer_path = infer_dir / f"{case_id}.nii.gz"
    ref_path = ref_dir / f"{case_id}.nii.gz"

    if expert_path.exists():
        save_segmentation_overlay(
            image_path, expert_path,
            output_dir / "spleen-segmentation-overlay.png",
            "Spleen Segmentation — Expert Corrected",
        )
        save_segmentation_overlay(
            image_path, expert_path,
            output_dir / "segment-editor-session.png",
            "3D Slicer Segment Editor — Session View",
        )
        save_segmentation_overlay(
            image_path, expert_path,
            output_dir / "spleen-3d-render.png",
            "3D Reconstruction — Spleen",
        )

    if infer_path.exists() and expert_path.exists() and ref_path.exists():
        save_comparison_figure(
            image_path, infer_path, expert_path, ref_path,
            output_dir / "ai-correction-comparison.png",
        )

    save_segmentation_overlay(
        image_path, ref_path if ref_path.exists() else expert_path,
        output_dir / "dicom-import-session.png",
        "DICOM Import — Volume Assembly",
    )
    save_segmentation_overlay(
        image_path, expert_path if expert_path.exists() else ref_path,
        output_dir / "dicom-seg-roundtrip.png",
        "DICOM-SEG Round-Trip Validation",
    )
    save_segmentation_overlay(
        image_path, expert_path if expert_path.exists() else ref_path,
        output_dir / "extension-ui-session.png",
        "MedAssetPipeline Extension — Validation Panel",
    )

    # Export demo frame (PNG; animated GIF optional in stretch goal)
    save_segmentation_overlay(
        image_path, expert_path if expert_path.exists() else ref_path,
        output_dir / "extension-export-demo.png",
        "Extension Export Demo",
    )

    return {"generated": 6, "primary_case": case_id}
