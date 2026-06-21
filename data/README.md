# Sample Data

This directory is gitignored except for this README. Download MSD Task09 Spleen data:

```bash
make data
# or
./scripts/download-sample-data.sh
```

## Dataset

[Medical Segmentation Decathlon Task09 — Spleen](http://medicaldecathlon.com/)

- Modality: CT
- Structure: spleen
- License: see MSD terms of use

## Layout (after download)

```
data/
├── raw/Task09_Spleen/          # MSD imagesTr / labelsTr
├── processed/                  # Normalized NIfTI volumes
├── labels/expert/              # Expert-corrected segmentations
├── inference/                  # AI draft masks
└── exports/                    # DICOM-SEG + provenance JSON
```

For CI and offline demos, `make data-synthetic` creates a minimal synthetic case at `data/processed/spleen_001.nii.gz`.
