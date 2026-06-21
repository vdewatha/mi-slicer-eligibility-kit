"""DICOM de-identification per PS3.15 Basic profile (tag scrubbing)."""

from __future__ import annotations

import logging
from pathlib import Path

import pydicom
from pydicom.dataset import Dataset

logger = logging.getLogger(__name__)

# Tags to remove or blank per DICOM PS3.15 Basic Application Level Confidentiality Profile
REMOVE_TAGS = [
    (0x0010, 0x0010),  # PatientName
    (0x0010, 0x0020),  # PatientID
    (0x0010, 0x0030),  # PatientBirthDate
    (0x0010, 0x1040),  # PatientAddress
    (0x0008, 0x0090),  # ReferringPhysicianName
    (0x0008, 0x0080),  # InstitutionName
    (0x0008, 0x0081),  # InstitutionAddress
    (0x0032, 0x1032),  # RequestingPhysician
    (0x0040, 0x0244),  # PerformedProcedureStepStartDate
    (0x0040, 0x0245),  # PerformedProcedureStepStartTime
]

UID_TAGS = [
    (0x0020, 0x000D),  # StudyInstanceUID
    (0x0020, 0x000E),  # SeriesInstanceUID
    (0x0008, 0x0018),  # SOPInstanceUID
]


def deidentify_dataset(ds: Dataset, pseudonym: str = "ANON") -> Dataset:
    """Scrub PHI tags; assign pseudonymous patient ID."""
    for tag in REMOVE_TAGS:
        if tag in ds:
            del ds[tag]
    if (0x0010, 0x0020) in ds:
        ds.PatientID = pseudonym
    else:
        ds.PatientID = pseudonym
    ds.PatientName = pseudonym
    return ds


def deidentify_dicom_dir(input_dir: Path, output_dir: Path, pseudonym_prefix: str = "CASE") -> int:
    """De-identify all DICOM files in a directory tree."""
    from medasset.io import ensure_dir

    ensure_dir(output_dir)
    count = 0
    for dcm_path in input_dir.rglob("*.dcm"):
        ds = pydicom.dcmread(str(dcm_path))
        pseudo = f"{pseudonym_prefix}_{count:04d}"
        deidentify_dataset(ds, pseudo)
        rel = dcm_path.relative_to(input_dir)
        out_path = output_dir / rel
        ensure_dir(out_path.parent)
        ds.save_as(str(out_path))
        count += 1
        logger.info("De-identified %s -> %s", dcm_path.name, out_path)
    return count
