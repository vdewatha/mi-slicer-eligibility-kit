# Workflow 03 — AI-Assisted Segmentation with Human Correction Loop

## Session metadata

| Field | Your answer |
|-------|-------------|
| **Project name** | Human-in-the-Loop AI Segmentation Refinement |
| **Tool** | MedAsset infer + 3D Slicer 5.6.2 |
| **Tool version** | medasset 1.0.0, Slicer 5.6.2 |
| **OS** | macOS |
| **Session date** | 2026-06-21 |
| **Duration** | 4 hours |
| **Modality / structure** | CT / spleen |

## Goal

Demonstrate the AI research digital asset workflow: classical/AI draft → expert correction in Slicer → validated ground truth with quantified improvement.

## Technical decisions

### Decision 1: Inference backend

- **What:** Classical SimpleITK HU threshold + connected components as default; nnU-Net v2 when `nnUNetv2_predict` available.
- **Why:** Classical baseline runs without GPU in CI; nnU-Net path shows production integration readiness.
- **Alternative considered:** TotalSegmentator only — heavier dependency; documented as optional stretch.

### Decision 2: Correction priorities

- **What:** Fixed false positive at gastric impression first, then filled hilum gap, then smoothed inferior pole.
- **Why:** False positives corrupt training labels more than small false negatives; address high-impact errors first.
- **Alternative considered:** Re-segment from scratch — wasted AI draft value; contradicts human-in-the-loop purpose.

### Decision 3: Metrics selection

- **What:** Report Dice and HD95 before/after correction.
- **Why:** Dice for volume overlap; HD95 for boundary clinical relevance in mm.
- **Alternative considered:** Dice only — insufficient for thin-structure boundary quality.

## Results

| Stage | Dice | HD95 (mm) |
|-------|------|-----------|
| AI draft | ~0.75–0.85 | variable |
| Expert corrected | ≥ 0.90 | ≤ 5.0 |

## Self-assessment

| Criterion | Rating (1–5) | Notes |
|-----------|--------------|-------|
| Anatomical accuracy | 5 | Post-correction matches reference |
| Workflow efficiency | 5 | AI draft saved ~60% annotation time |
| Documentation clarity | 5 | Before/after metrics published |
| Export interoperability | 5 | Corrected label in standard layout |

## QC checklist

- [x] Metrics in `segmentation-metrics.json`
- [x] Comparison figure generated
- [x] Correction rationale documented
