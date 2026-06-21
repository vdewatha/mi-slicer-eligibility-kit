# Project 02 — Expert Segmentation in Segment Editor

**Tool:** 3D Slicer 5.x Segment Editor  
**Estimated time:** 4–6 hours  
**Structure:** Spleen (MSD Task09)  
**Workflow doc:** [`workflows/02-segment-editor-workflow.md`](../workflows/02-segment-editor-workflow.md)

## Goal

Produce an expert-quality spleen segmentation using Segment Editor tools. Document window/level, segmentation strategy, and edge-case handling.

## Deliverables

| File | Location |
|------|----------|
| Segmentation overlay | `portfolio/assets/spleen-segmentation-overlay.png` |
| 3D render | `portfolio/assets/spleen-3d-render.png` |
| Segment Editor screenshot | `portfolio/assets/segment-editor-session.png` |
| Expert label (optional) | `data/labels/expert/spleen_001.nii.gz` |
| Workflow doc | `workflows/02-segment-editor-workflow.md` |

## Acceptance criteria

- [ ] Segmentation reviewed in axial, coronal, sagittal views
- [ ] 3D view checked for topology errors (holes, islands)
- [ ] HU range / threshold documented
- [ ] At least 2 segmentation tools used (e.g., threshold + smoothing)
- [ ] Workflow doc includes rejected alternatives

## Session outline

### 1. Load volume (15 min)

Load `data/processed/spleen_001.nii.gz` in Slicer.

### 2. Create segmentation (2–3 hr)

1. Modules → Segment Editor
2. Add segment "Spleen"
3. Threshold or Grow from Seeds with documented HU range
4. Remove islands, fill holes, smooth surface
5. Use Paint for boundary refinement at hilum

### 3. Export and screenshot (30 min)

1. Segmentations → Export to labelmap
2. Save as `data/labels/expert/spleen_001.nii.gz`
3. Capture overlay and 3D views

## Decision prompts

- Why threshold vs region growing for this contrast phase?
- How did you handle partial-volume slices at superior/inferior extent?
- What smoothing kernel preserved detail without shrinking volume?
