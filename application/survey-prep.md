# Survey Application Prep — Medical Imaging & 3D Slicer Specialists

Use this checklist when completing the **Medical Imaging & 3D Slicer Specialists** survey. Map each question to concrete evidence from this kit.

## Before you start

- [ ] Read all five project briefs in [`projects/`](../projects/)
- [ ] Customize portfolio hero name in [`portfolio/index.html`](../portfolio/index.html) (`#portfolio-owner`)
- [ ] Run `./scripts/check-portfolio.sh` — all checks pass
- [ ] Deploy portfolio and have live URL ready

## Evidence mapping

| Survey topic | Your evidence | Location |
|--------------|---------------|----------|
| 3D Slicer experience | Segment Editor + extension screenshots | `portfolio/assets/*-session.png`, `extension-ui-session.png` |
| DICOM workflows | De-ID pipeline + DICOM-SEG round-trip | `workflows/01-*`, `workflows/04-*`, `sample-spleen.dcm` |
| AI digital assets | Correction loop + provenance sidecars | `workflows/03-*`, `pipeline/medasset/provenance.py` |
| Python automation | Pipeline package + extension | `pipeline/medasset/`, `extensions/MedAssetPipeline/` |
| Segmentation expertise | Overlays, 3D render, metrics | `spleen-segmentation-overlay.png`, `segmentation-metrics.json` |
| Reproducibility | CI + Makefile | README, `.github/workflows/ci.yml` |
| Portfolio / work samples | Deployed site URL | GitHub Pages or Netlify link to `portfolio/` |

## Talking points (advanced framing)

### DICOM & QC

- "I built an automated ingest pipeline with PS3.15 Basic de-identification and QC gates for spacing, HU range, and slice integrity before data enters training."
- "QC failures are documented per-case in JSON — not just pass/fail at cohort level."

### 3D Slicer & Segment Editor

- "I use Grow from Seeds with documented HU ranges, then Paint/Erase for hilum and organ-interface corrections."
- "Every segmentation is reviewed in axial, coronal, sagittal, and 3D before export."

### AI human-in-the-loop

- "AI draft masks accelerate annotation, but expert correction in Slicer produces defensible ground truth — I publish Dice before and after correction."
- "This mirrors how AI research teams build training data: model proposal, expert refinement, provenance tracking."

### DICOM-SEG & provenance

- "I export DICOM-SEG with geometry validation — FrameOfReferenceUID, IOP, spacing — not just NIfTI masks on disk."
- "Each asset has a provenance JSON sidecar: tool version, annotator, steps, QC status, metrics."

### Custom extension

- "I shipped a ScriptedLoadableModule (MedAssetPipeline) that wraps QC, Dice validation, and export — tools radiologists and ML engineers can actually use."

## 3-minute verbal walkthrough prep

### Pipeline overview (3 min)

1. **Problem** (30 sec): AI teams need validated, interoperable imaging assets with lineage
2. **Architecture** (45 sec): DICOM → QC → infer → Slicer correction → DICOM-SEG + provenance
3. **Demo** (60 sec): Show portfolio metrics, one overlay, extension screenshot
4. **Differentiator** (30 sec): Clone repo, `make validate`, same metrics — reproducible
5. **Close** (15 sec): Ready to build digital assets for your AI research initiative

### Segment Editor deep-dive (3 min)

1. **Case** (20 sec): MSD Task09 spleen, CE-CT
2. **Approach** (90 sec): Window/level, Grow from Seeds, boundary fixes, smoothing rationale
3. **QC** (40 sec): Multiplanar review, 3D topology, metrics vs reference
4. **Export** (30 sec): DICOM-SEG round-trip validation

## Experience statement (advanced)

> "I design end-to-end medical imaging digital asset pipelines for AI research: DICOM ingest and de-identification, automated QC, AI-assisted segmentation with expert correction in 3D Slicer, and interoperable DICOM-SEG export with provenance sidecars. I've built a custom Slicer extension (MedAssetPipeline) and a reproducible Python pipeline with CI-validated segmentation metrics on public benchmark data (MSD Task09). I'm comfortable shipping tools and documenting expert decision rationale for training-data workflows."

## Pre-submit checklist

- [ ] `./scripts/check-portfolio.sh` exits with 0 errors
- [ ] Portfolio URL loads and shows project cards as Ready
- [ ] `make validate` passes locally
- [ ] All five workflow docs have filled Decision sections
- [ ] GitHub repo is public with CI badge green
- [ ] Reviewed [`sample-ai-evaluation-tasks.md`](sample-ai-evaluation-tasks.md)

## Portfolio customization

Edit [`portfolio/index.html`](../portfolio/index.html):

```html
<span id="portfolio-owner">Your Name</span>
```

## Optional strong signals

- 3-minute screen recording: Slicer correction loop + extension export
- Link to built extension `.s4ext` or install instructions video
- Second organ (MSD Task03 Liver) as stretch demo
