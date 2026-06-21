"""Pipeline unit tests."""

from pathlib import Path

import numpy as np
import pytest
import SimpleITK as sitk

from medasset.ingest import ingest_nifti_pair
from medasset.metrics import compute_metrics, dice_coefficient
from medasset.qc import run_qc
from medasset.synthetic import create_synthetic_case


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    create_synthetic_case(tmp_path, "spleen_001")
    return tmp_path


def test_dice_perfect_match():
    arr = np.ones((10, 10, 10), dtype=np.uint8)
    assert dice_coefficient(arr, arr) == 1.0


def test_dice_no_overlap():
    a = np.zeros((10, 10, 10), dtype=np.uint8)
    b = np.ones((10, 10, 10), dtype=np.uint8)
    assert dice_coefficient(a, b) == 0.0


def test_synthetic_case_creates_files(data_dir: Path):
    assert (data_dir / "processed" / "spleen_001.nii.gz").exists()
    assert (data_dir / "labels" / "reference" / "spleen_001.nii.gz").exists()


def test_qc_passes_synthetic(data_dir: Path):
    report = run_qc(data_dir)
    assert report["total_cases"] == 1
    assert report["passed"] == 1


def test_ingest_nifti_pair(data_dir: Path, tmp_path: Path):
    src = data_dir / "processed" / "spleen_001.nii.gz"
    out = tmp_path / "processed"
    ingest_nifti_pair(src, None, out, "copy_001")
    assert (out / "copy_001.nii.gz").exists()


def test_compute_metrics_identical(data_dir: Path):
    ref = data_dir / "labels" / "reference" / "spleen_001.nii.gz"
    m = compute_metrics(ref, ref)
    assert m["dice"] == 1.0
