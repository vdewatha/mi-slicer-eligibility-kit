"""Shared I/O helpers for MedAsset pipeline."""

from __future__ import annotations

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import SimpleITK as sitk


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    ensure_dir(path.parent)
    with path.open("w") as f:
        json.dump(data, f, indent=2)


def load_label(path: Path) -> sitk.Image:
    return sitk.ReadImage(str(path))


def load_volume(path: Path) -> sitk.Image:
    return sitk.ReadImage(str(path))


def save_label(image: sitk.Image, path: Path) -> None:
    ensure_dir(path.parent)
    sitk.WriteImage(image, str(path), useCompression=True)


def list_cases(processed_dir: Path, suffix: str = ".nii.gz") -> list[str]:
    if not processed_dir.exists():
        return []
    return sorted(p.name[: -len(suffix)] for p in processed_dir.glob(f"*{suffix}"))
