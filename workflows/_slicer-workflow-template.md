# Slicer Workflow Template

Copy this structure when documenting any 3D Slicer medical imaging session. Fill every section — AI-training reviewers want decision rationale, not click logs.

---

## Session metadata

| Field | Your answer |
|-------|-------------|
| **Project name** | |
| **Tool** | 3D Slicer |
| **Tool version** | |
| **Extensions used** | |
| **OS** | macOS (version) |
| **Session date** | |
| **Duration** | |
| **Modality / structure** | CT / spleen |

## Goal and constraints

What were you trying to achieve? What limitations did you work within (data quality, time, reference availability)?

> Example: "Build a validated spleen segmentation for MSD Task09 with DICOM-SEG export. Constraint: must preserve geometry for AI training pipeline."

## Source material

| File | Source | Role |
|------|--------|------|
| | MSD Task09 / DICOM | Reference volume |
| | | Segmentation label |

## Workflow timeline

1. 
2. 
3. 

## Technical decisions

For each decision, write **what you did**, **why**, and **what alternative you rejected**.

### Decision 1: [Topic — e.g., Window/level]

- **What:** 
- **Why:** 
- **Alternative considered:** 

### Decision 2: [Topic — e.g., Segmentation method]

- **What:** 
- **Why:** 
- **Alternative considered:** 

### Decision 3: [Topic — e.g., Export format]

- **What:** 
- **Why:** 
- **Alternative considered:** 

## Problems encountered

| Issue | Resolution |
|-------|------------|
| | |

## Self-assessment

| Criterion | Rating (1–5) | Notes |
|-----------|--------------|-------|
| Anatomical accuracy | | |
| Workflow efficiency | | |
| Documentation clarity | | |
| Export interoperability | | |

## QC checklist

- [ ] Volume orientation verified (RAS/LPS consistent with reference)
- [ ] Segmentation reviewed in axial, coronal, sagittal
- [ ] 3D view checked for topology errors
- [ ] Export geometry matches reference FrameOfReferenceUID
- [ ] Provenance sidecar written
