# Workflow 01 — DICOM Ingest, De-ID, and QC

## Session metadata

| Field | Your answer |
|-------|-------------|
| **Project name** | MSD Task09 Spleen — DICOM Ingest & QC |
| **Tool** | MedAsset pipeline + 3D Slicer 5.6.2 |
| **Tool version** | Slicer 5.6.2, medasset 1.0.0 |
| **Extensions used** | Quantitative Reporting (optional) |
| **OS** | macOS |
| **Session date** | 2026-06-21 |
| **Duration** | 3 hours |
| **Modality / structure** | CT / spleen |

## Goal and constraints

Ingest MSD Task09 spleen CT volumes, apply PS3.15 Basic de-identification, and run automated QC before they enter the AI training asset pipeline. Constraint: no PHI in exported artifacts; all cases must have documented pass/fail status.

## Source material

| File | Source | Role |
|------|--------|------|
| `spleen_001.nii.gz` | MSD Task09 imagesTr | Reference CT volume |
| `spleen_001.nii.gz` | MSD Task09 labelsTr | Reference segmentation |

## Workflow timeline

1. `make data` — download MSD subset or generate synthetic fallback
2. `make ingest` — normalize NIfTI into `data/processed/`
3. `make qc` — write `portfolio/assets/qc-report.json`
4. Load volume in Slicer Data module; verify LPS/RAS orientation
5. Screenshot volume assembly; document QC thresholds

## Technical decisions

### Decision 1: Series assembly strategy

- **What:** Used MSD pre-converted NIfTI rather than raw DICOM series for Task09 subset.
- **Why:** MSD NIfTI files are pre-oriented and widely used in segmentation benchmarks; reduces DICOM series ambiguity for portfolio reproducibility.
- **Alternative considered:** Raw DICOM import via `dcm2niix` — rejected for CI simplicity; documented as production path in README.

### Decision 2: De-identification profile

- **What:** Applied DICOM PS3.15 Basic profile tag scrubbing (PatientName, PatientID, InstitutionName, etc.).
- **Why:** Minimum bar for sharing research assets; aligns with TCIA and MSD redistribution terms.
- **Alternative considered:** Retired profile with full UID remapping — unnecessary for public MSD data already de-identified.

### Decision 3: QC thresholds

- **What:** Fail cases with < 10 slices, non-finite voxels, or HU range outside [-1524, 3571].
- **Why:** Catches corrupt conversions and truncated downloads before they pollute training sets.
- **Alternative considered:** Manual-only QC — rejected; automated gates scale to cohort curation.

## Problems encountered

| Issue | Resolution |
|-------|------------|
| MSD download slow on CI | Synthetic fallback via `make data-synthetic` |
| Double `.nii` in case ID parsing | Fixed `list_cases()` to strip full `.nii.gz` suffix |

## Self-assessment

| Criterion | Rating (1–5) | Notes |
|-----------|--------------|-------|
| Anatomical accuracy | 4 | QC verifies volume integrity, not anatomy |
| Workflow efficiency | 5 | One-command ingest + QC |
| Documentation clarity | 5 | Thresholds documented with rationale |
| Export interoperability | 4 | NIfTI normalized; DICOM path in Project 04 |

## QC checklist

- [x] Volume orientation verified
- [x] QC JSON generated with per-case status
- [x] HU range within expected CT bounds
- [x] No PHI in portfolio assets
