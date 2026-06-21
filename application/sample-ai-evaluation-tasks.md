# Sample AI Evaluation Tasks — Medical Imaging & 3D Slicer

Practice questions modeled on **medical imaging AI trainer** screening (Micro1-style). For each task: write your answer, then compare against the rubric.

---

## Task 1: DICOM won't load as single volume

**Question:** A user imports a CT study into 3D Slicer but gets multiple separate volumes instead of one 3D volume. What steps diagnose and fix this?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| Diagnosis | Multiple series UIDs; mixed modalities; scout/localizer series included |
| DICOM module | Use DICOM browser to select correct series by slice count and SeriesDescription |
| Advanced | Check ImageOrientationPatient consistency across slices |
| Fix | Load single series; exclude scouts; use DICOM Scalar Volume Plugin |
| Prevention | Pre-filter series in ingest pipeline by slice count and Modality=CT |

---

## Task 2: Segment Editor threshold leaks into adjacent organ

**Question:** Threshold-based spleen segmentation includes stomach wall. How do you fix without starting over?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| Immediate fix | Erase tool or Remove selected island in Segment Editor |
| Refinement | Grow from Seeds with fewer seeds; Paint brush for boundary |
| Window/level | Adjust W/L to increase spleen vs stomach contrast before threshold |
| Alternative | Use Surface Cut or Logical operators to subtract overlapping region |
| Vocabulary | Segment Editor, labelmap, island, HU range, connectivity |

---

## Task 3: DICOM-SEG geometry mismatch after export

**Question:** After exporting a segmentation as DICOM-SEG and re-importing, the overlay is shifted relative to the source volume. What causes this?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| Root causes | FrameOfReferenceUID mismatch; different ImageOrientationPatient; resampling without updating metadata |
| IOP | ImageOrientationPatient must match reference series |
| Position | ImagePositionPatient sequence must align with slice spacing along normal |
| Spacing | PixelSpacing and SliceThickness must match reference |
| Fix | Export SEG referencing original DICOM series; verify with ITK/SimpleITK geometry before export |

---

## Task 4: When Grow from Seeds vs Paint

**Question:** In partial-volume slices at the superior spleen pole, when do you use Grow from Seeds vs manual Paint?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| Grow from Seeds | Homogeneous intensity, clear boundary, good contrast on slice |
| Paint | Partial volume, indistinct boundary, hilum vessels, organ interface |
| Partial volume | Single voxel thickness — Paint with small brush; avoid aggressive threshold |
| Seeds caution | Too many seeds in heterogeneous tissue causes leaks |
| Workflow | Coarse Grow from Seeds first, Paint for edge refinement |

---

## Task 5: QC flags for training data exclusion

**Question:** What automated QC checks would you run before CT segmentations enter an AI training set?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| Coverage | Minimum slice count; FOV includes full structure |
| Spacing | Anisotropic spacing outliers; missing slices (gaps in IPP) |
| Intensity | HU range sanity; metal artifact detection (optional) |
| PHI | De-identification verification; burned-in annotation detection |
| Segmentation | Empty mask; extreme volume vs population; disconnected components |
| Documentation | Per-case pass/fail log with exclusion reason |

---

## Task 6: Evaluating AI answer about nnU-Net in Slicer

**Prompt given to AI:** "Run nnU-Net in 3D Slicer by going to Modules → nnU-Net → Predict."

**AI response:** "Open 3D Slicer, go to Modules, select nnU-Net, click Predict, and choose your model folder."

**Your evaluation:** Is this accurate? What's missing?

### Expert evaluation rubric

| Verdict | Reasoning |
|---------|-----------|
| Partially accurate | Requires SlicerNNUnet or MONAI Label extension — not built-in |
| Missing | Model/dataset ID, fold, input preprocessing, GPU requirement |
| Missing | Input must be NIfTI with correct _0000 channel naming for nnU-Net |
| Missing | Output labelmap import and geometry check steps |
| Good reviewer note | "Correct high-level intent but omits extension dependency and nnU-Net environment setup" |

---

## Task 7: HU window for spleen segmentation

**Question:** What window/level do you use for spleen segmentation on contrast-enhanced CT, and why?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| Typical W/L | W:350 L:40 or W:200 L:50 for detail |
| HU range | Spleen parenchyma ~50–90 HU post-contrast |
| Rationale | Wider window for overview; narrower for hilum and pole boundaries |
| Phase | Arterial vs portal venous affects enhancement — document phase |
| Pitfall | Using bone window or lung window hides soft-tissue boundaries |

---

## Task 8: Provenance for AI training assets

**Question:** Why should segmentation exports include provenance metadata beyond the mask file?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| Lineage | Source study, annotator, tool version, date |
| Steps | AI draft vs manual correction; model version/hash |
| QC | Pass/fail status; exclusion reasons |
| Reproducibility | Enables audit, dataset versioning, regulatory traceability |
| Standards | VIDS/BIDS-inspired sidecars for ML-ready datasets |

---

## Task 9: SimpleITK vs Slicer Segment Editor

**Question:** When would you use a Python SimpleITK pipeline vs 3D Slicer Segment Editor?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| SimpleITK | Batch processing, CI, reproducible classical/ML pipelines, headless servers |
| Slicer | Interactive expert review, complex anatomy, visual QC, teaching AI correction |
| Combined | Pipeline generates draft; Slicer for human-in-the-loop refinement |
| Export | SimpleITK for metrics; Slicer for clinical review UI and DICOM-SEG validation |

---

## Task 10: Documenting workflow for AI training

**Question:** Why do AI imaging programs ask for segmentation decision rationale, not just final masks?

### Expert answer rubric

| Criterion | Strong answer includes |
|-----------|---------------------|
| Intent | Models need expert reasoning, not just binary labels |
| Ambiguity | Same HU threshold wrong across contrast phases and scanners |
| Edge cases | Hilum, partial volume, organ interfaces require contextual judgment |
| Vocabulary | Teaches domain terms: Grow from Seeds, FrameOfReferenceUID, HD95 |
| Quality | Enables evaluation of AI suggestions against expert standards |

---

## Practice protocol

1. Pick 3 tasks (one DICOM, one segmentation, one meta/evaluation)
2. Write 150–250 words without looking at rubric
3. Compare — note gaps in vocabulary or missing steps
4. Revise once before survey submission
