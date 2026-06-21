"""Provenance sidecar generation (VIDS-inspired JSON)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from medasset import __version__
from medasset.io import write_json


def build_provenance(
    case_id: str,
    source: str,
    steps: list[str],
    metrics: dict[str, float] | None = None,
    qc_status: str = "pass",
    export_format: str = "DICOM-SEG",
    annotator: str = "expert_review",
    slicer_version: str = "5.6.2",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "case_id": case_id,
        "source": source,
        "slicer_version": slicer_version,
        "pipeline_version": __version__,
        "annotator": annotator,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "steps": steps,
        "qc_status": qc_status,
        "export_format": export_format,
    }
    if metrics:
        record["metrics"] = metrics
    if extra:
        record.update(extra)
    return record


def write_provenance(path: Path, record: dict[str, Any]) -> None:
    write_json(path, record)
