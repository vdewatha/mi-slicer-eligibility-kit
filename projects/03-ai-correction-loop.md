# Project 03 — AI-Assisted Segmentation with Human Correction Loop

**Tooling:** MedAsset infer pipeline + 3D Slicer Segment Editor  
**Estimated time:** 4–5 hours  
**Workflow doc:** [`workflows/03-ai-correction-loop-workflow.md`](../workflows/03-ai-correction-loop-workflow.md)

## Goal

Run AI/classical inference to generate a draft mask, correct errors in 3D Slicer, and publish before/after metrics (Dice, HD95) demonstrating the human-in-the-loop asset refinement workflow.

## Deliverables

| File | Location |
|------|----------|
| AI vs corrected comparison | `portfolio/assets/ai-correction-comparison.png` |
| Metrics JSON | `portfolio/assets/segmentation-metrics.json` |
| Workflow doc | `workflows/03-ai-correction-loop-workflow.md` |

## Acceptance criteria

- [ ] AI draft mask generated via `make infer`
- [ ] Expert correction documented with time-on-task
- [ ] Dice improvement after correction quantified
- [ ] `mean_dice_corrected` ≥ 0.90 on portfolio case
- [ ] Workflow explains what AI got wrong and how you fixed it

## Session outline

### 1. Generate AI draft (30 min)

```bash
cd pipeline && make infer && make metrics
```

### 2. Import draft to Slicer (30 min)

1. Load volume + `data/inference/spleen_001.nii.gz` as labelmap
2. Compare against `data/labels/reference/`

### 3. Correct in Segment Editor (2–3 hr)

1. Identify false positives (adjacent soft tissue) and false negatives (hilum gap)
2. Use Paint/Erase and Smoothing
3. Export corrected label to `data/labels/expert/`

### 4. Recompute metrics (15 min)

```bash
make metrics
```

## Target metrics

| Metric | AI only | After correction |
|--------|---------|------------------|
| Dice | document | ≥ 0.90 |
| HD95 (mm) | document | ≤ 5.0 |
