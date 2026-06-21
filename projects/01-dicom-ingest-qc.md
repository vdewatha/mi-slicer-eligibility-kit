# Project 01 — DICOM Ingest, De-ID, and QC

**Tooling:** pydicom, SimpleITK, MedAsset pipeline  
**Estimated time:** 3–4 hours  
**Dataset:** MSD Task09 Spleen (CT)  
**Workflow doc:** [`workflows/01-dicom-ingest-qc-workflow.md`](../workflows/01-dicom-ingest-qc-workflow.md)

## Goal

Ingest a CT series, apply DICOM PS3.15 Basic de-identification, run automated QC gates, and produce a JSON QC report suitable for AI training data curation.

## Deliverables

| File | Location |
|------|----------|
| QC report (JSON) | `portfolio/assets/qc-report.json` |
| QC summary chart | `portfolio/assets/qc-summary.png` |
| Import session screenshot | `portfolio/assets/dicom-import-session.png` |
| Workflow doc | `workflows/01-dicom-ingest-qc-workflow.md` |

## Acceptance criteria

- [ ] At least one case ingested into `data/processed/`
- [ ] PHI tags scrubbed per PS3.15 Basic profile
- [ ] QC report flags spacing, HU range, slice count
- [ ] All cases marked pass or fail with documented reasons
- [ ] Workflow doc includes series selection and QC threshold rationale

## Session outline

### 1. Download data (15 min)

```bash
make data
```

### 2. Run ingest + QC (30 min)

```bash
cd pipeline && make ingest && make qc
```

### 3. Review in 3D Slicer (45 min)

1. File → Add DICOM Data / load NIfTI from `data/processed/`
2. Verify orientation in Data module
3. Check window/level for spleen visibility (W:350 L:40 typical for CE-CT)
4. Screenshot volume assembly view

### 4. Document decisions (30 min)

Fill workflow doc: series selection, de-ID approach, QC thresholds.

## Export settings

| Setting | Value |
|---------|-------|
| Output format | NIfTI `.nii.gz` |
| QC output | JSON + PNG summary |
| De-ID profile | DICOM PS3.15 Basic |

## References

- [pipeline/medasset/ingest.py](../pipeline/medasset/ingest.py)
- [pipeline/medasset/qc.py](../pipeline/medasset/qc.py)
