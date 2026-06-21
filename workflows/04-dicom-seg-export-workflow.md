# Workflow 04 — DICOM-SEG Interoperable Export

## Session metadata

| Field | Your answer |
|-------|-------------|
| **Project name** | DICOM-SEG Export with Geometry Validation |
| **Tool** | highdicom + MedAsset export pipeline |
| **Tool version** | highdicom 0.22+, medasset 1.0.0 |
| **OS** | macOS |
| **Session date** | 2026-06-21 |
| **Duration** | 3 hours |
| **Modality / structure** | CT / spleen |

## Technical decisions

### Decision 1: Export library

- **What:** highdicom `Segmentation` SOP for primary export; fallback minimal SEG + NIfTI companion.
- **Why:** highdicom is the standard Python path for interoperable DICOM-SEG; fallback ensures portfolio works offline.
- **Alternative considered:** dcmqi only — heavier build; Slicer GUI export only — not batchable.

### Decision 2: Reference series handling

- **What:** Generate minimal reference DICOM series from SimpleITK volume metadata for SEG linkage.
- **Why:** DICOM-SEG requires source image geometry; synthetic reference series preserves IOP/spacing from NIfTI.
- **Alternative considered:** SEG without reference — invalid per DICOM standard.

### Decision 3: Provenance sidecar

- **What:** JSON sidecar with case_id, pipeline_version, steps, qc_status, metrics.
- **Why:** AI research teams need lineage beyond the DICOM file; VIDS-inspired without full validator dependency.
- **Alternative considered:** DICOM private tags only — not portable across PACS.

## Geometry validation

- FrameOfReferenceUID assigned consistently
- ImageOrientationPatient matches source volume direction cosines
- Slice spacing verified on round-trip overlay in Slicer

## Self-assessment

| Criterion | Rating (1–5) | Notes |
|-----------|--------------|-------|
| Anatomical accuracy | 5 | Label unchanged; geometry validated |
| Workflow efficiency | 4 | Batch export via `make export` |
| Documentation clarity | 5 | Round-trip steps documented |
| Export interoperability | 5 | DICOM-SEG in portfolio assets |

## QC checklist

- [x] `sample-spleen.dcm` in portfolio/assets
- [x] Provenance JSON alongside export
- [x] Round-trip screenshot captured
- [x] No PHI in exported DICOM
