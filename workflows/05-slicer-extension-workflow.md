# Workflow 05 — Custom Slicer Extension: MedAssetPipeline

## Session metadata

| Field | Your answer |
|-------|-------------|
| **Project name** | MedAssetPipeline ScriptedLoadableModule |
| **Tool** | 3D Slicer Extension development |
| **Tool version** | Slicer 5.6.2 |
| **OS** | macOS |
| **Session date** | 2026-06-21 |
| **Duration** | 6 hours |
| **Modality / structure** | CT / general segmentation export |

## Goal

Ship a reusable Slicer module that encapsulates QC → Dice validation → DICOM-SEG + provenance export for AI research asset workflows.

## Technical decisions

### Decision 1: Module architecture

- **What:** Standard ScriptedLoadableModule with separate Widget and Logic classes.
- **Why:** Slicer convention; Logic testable without UI; matches Extension Wizard scaffold.
- **Alternative considered:** Single-file script — not maintainable for portfolio extension.

### Decision 2: Dice computation

- **What:** Export visible segments to labelmap on reference grid, numpy Dice.
- **Why:** Uses Slicer segmentation infrastructure; avoids external SimpleITK dependency inside Slicer runtime.
- **Alternative considered:** SegmentStatistics module only — doesn't compare to external reference labelmap node.

### Decision 3: Export strategy

- **What:** Labelmap NIfTI + metadata JSON companion; DICOM-SEG via pipeline for batch.
- **Why:** Slicer DICOM-SEG export requires DICOM database context; extension provides one-click path with provenance; batch path uses Python pipeline.
- **Alternative considered:** Full highdicom inside Slicer Python — dependency conflict risk.

## Extension UI structure

1. **QC Summary** — collapsible panel, JSON output
2. **Validation Metrics** — Dice vs `ReferenceLabelmap` node
3. **Export** — case ID, output directory, one-click export button

## Self-assessment

| Criterion | Rating (1–5) | Notes |
|-----------|--------------|-------|
| Anatomical accuracy | N/A | Tool module |
| Workflow efficiency | 5 | One-click export path |
| Documentation clarity | 5 | Build instructions in README |
| Export interoperability | 4 | Companion NIfTI + meta; batch DICOM-SEG via pipeline |

## QC checklist

- [x] Module loads in Slicer without errors
- [x] QC panel reports volume spacing
- [x] Export writes provenance JSON
- [x] Screenshot in portfolio assets
