"""DICOM / NIfTI ingestion and volume normalization."""

from __future__ import annotations

import logging
from pathlib import Path

import SimpleITK as sitk

from medasset.io import ensure_dir, list_cases, save_label

logger = logging.getLogger(__name__)


def _read_dicom_series(series_dir: Path) -> sitk.Image:
    reader = sitk.ImageSeriesReader()
    series_ids = reader.GetGDCMSeriesIDs(str(series_dir))
    if not series_ids:
        raise FileNotFoundError(f"No DICOM series in {series_dir}")
    file_names = reader.GetGDCMSeriesFileNames(str(series_dir), series_ids[0])
    reader.SetFileNames(file_names)
    return reader.Execute()


def ingest_nifti_pair(
    image_path: Path,
    label_path: Path | None,
    output_dir: Path,
    case_id: str,
) -> Path:
    """Copy/normalize a NIfTI image (and optional label) into processed layout."""
    ensure_dir(output_dir)
    image = sitk.ReadImage(str(image_path))
    image = sitk.Cast(image, sitk.sitkFloat32)
    out_image = output_dir / f"{case_id}.nii.gz"
    sitk.WriteImage(image, str(out_image), useCompression=True)

    if label_path and label_path.exists():
        label = sitk.ReadImage(str(label_path))
        label = sitk.Cast(label > 0, sitk.sitkUInt8)
        labels_dir = output_dir.parent / "labels" / "reference"
        ensure_dir(labels_dir)
        save_label(label, labels_dir / f"{case_id}.nii.gz")

    return out_image


def ingest_msd_task09(data_dir: Path) -> list[str]:
    """Ingest MSD Task09 Spleen layout: imagesTr/*.nii.gz + labelsTr/*.nii.gz."""
    raw = data_dir / "raw" / "Task09_Spleen"
    images_tr = raw / "imagesTr"
    labels_tr = raw / "labelsTr"
    processed = data_dir / "processed"
    ingested: list[str] = []

    if not images_tr.exists():
        logger.warning("MSD imagesTr not found at %s", images_tr)
        return ingested

    for image_path in sorted(images_tr.glob("*.nii.gz")):
        case_id = image_path.name.replace(".nii.gz", "").replace("spleen_", "spleen_")
        label_path = labels_tr / image_path.name
        ingest_nifti_pair(image_path, label_path, processed, case_id)
        ingested.append(case_id)
        logger.info("Ingested %s", case_id)

    return ingested


def ingest_synthetic(data_dir: Path) -> list[str]:
    """Ingest synthetic case if present."""
    processed = data_dir / "processed"
    cases = list_cases(processed)
    return cases


def run_ingest(data_dir: Path) -> dict:
    """Run ingestion from MSD or existing processed volumes."""
    cases = ingest_msd_task09(data_dir)
    if not cases:
        cases = ingest_synthetic(data_dir)
    return {"ingested_cases": cases, "count": len(cases)}
