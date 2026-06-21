# Workflow 02 — Expert Segmentation in Segment Editor

## Session metadata

| Field | Your answer |
|-------|-------------|
| **Project name** | Spleen Expert Segmentation — Segment Editor |
| **Tool** | 3D Slicer 5.6.2 |
| **Tool version** | 5.6.2 |
| **Extensions used** | Segment Editor, SegmentStatistics |
| **OS** | macOS |
| **Session date** | 2026-06-21 |
| **Duration** | 4 hours |
| **Modality / structure** | CT / spleen |

## Goal and constraints

Produce anatomically plausible spleen segmentation on MSD Task09 case using Segment Editor. Document tool choices and HU ranges for AI training workflow capture.

## Technical decisions

### Decision 1: Window/level

- **What:** W:350 L:40 for initial review; switched to W:200 L:50 for hilum detail.
- **Why:** CE-CT spleen parenchyma ~50–90 HU; narrower window improves boundary visibility at vascular hilum.
- **Alternative considered:** Fixed abdominal preset W:400 L:40 — too wide for inferior pole detail.

### Decision 2: Segmentation method

- **What:** Grow from Seeds with threshold mask (-50 to 150 HU), then Paint for hilum and Erase for gastric impression false positives.
- **Why:** Region growing respects connectivity; manual paint fixes where intensity overlaps adjacent soft tissue.
- **Alternative considered:** Full manual Paint — too slow for portfolio timeline; Threshold-only — leaked into stomach wall.

### Decision 3: Smoothing

- **What:** Median smoothing kernel 3mm, then Remove Islands < 500 mm³.
- **Why:** Removes speckle without significant volume loss on 1mm isotropic spacing.
- **Alternative considered:** Gaussian smoothing — blurred hilum indentations.

## Self-assessment

| Criterion | Rating (1–5) | Notes |
|-----------|--------------|-------|
| Anatomical accuracy | 5 | Reviewed all three planes + 3D |
| Workflow efficiency | 4 | Grow-from-seeds accelerated baseline |
| Documentation clarity | 5 | HU ranges and tools documented |
| Export interoperability | 5 | Labelmap matches reference geometry |

## QC checklist

- [x] Axial, coronal, sagittal review
- [x] 3D topology checked
- [x] Label exported to `data/labels/expert/`
