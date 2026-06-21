# Project 04 — DICOM-SEG Interoperable Export

**Tooling:** highdicom, pydicom, MedAsset export pipeline  
**Estimated time:** 3–4 hours  
**Workflow doc:** [`workflows/04-dicom-seg-export-workflow.md`](../workflows/04-dicom-seg-export-workflow.md)

## Goal

Export expert-corrected segmentations as DICOM-SEG with correct geometry (FrameOfReferenceUID, IOP, spacing). Validate round-trip import in 3D Slicer.

## Deliverables

| File | Location |
|------|----------|
| Sample DICOM-SEG | `portfolio/assets/sample-spleen.dcm` |
| Round-trip validation screenshot | `portfolio/assets/dicom-seg-roundtrip.png` |
| Provenance sidecar | `data/exports/spleen_001_provenance.json` |
| Workflow doc | `workflows/04-dicom-seg-export-workflow.md` |

## Acceptance criteria

- [ ] DICOM-SEG references original series geometry
- [ ] Round-trip import shows aligned overlay in Slicer
- [ ] Provenance JSON includes tool version, steps, QC status
- [ ] De-identified — no PHI in exported DICOM
- [ ] Workflow documents geometry validation steps

## Session outline

### 1. Run export pipeline (30 min)

```bash
cd pipeline && make export
```

### 2. Validate in Slicer (1 hr)

1. DICOM module → Import `data/exports/` or `portfolio/assets/sample-spleen.dcm`
2. Load reference volume + imported SEG
3. Verify overlay alignment slice-by-slice
4. Screenshot round-trip validation

### 3. Document geometry checks (30 min)

Record FrameOfReferenceUID match, spacing, orientation checks in workflow doc.

## Key validation checks

- ImagePositionPatient progression along slice normal
- PixelSpacing matches reference series
- Segment label matches expected structure name
