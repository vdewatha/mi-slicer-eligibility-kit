# Project 05 — Custom Slicer Extension: MedAssetPipeline

**Tool:** 3D Slicer ScriptedLoadableModule development  
**Estimated time:** 6–8 hours  
**Workflow doc:** [`workflows/05-slicer-extension-workflow.md`](../workflows/05-slicer-extension-workflow.md)

## Goal

Build and document a custom Slicer extension that wraps validate → metrics → DICOM-SEG export + provenance — demonstrating you ship tools radiologists and AI teams can use.

## Deliverables

| File | Location |
|------|----------|
| Extension source | `extensions/MedAssetPipeline/` |
| Extension UI screenshot | `portfolio/assets/extension-ui-session.png` |
| Export demo frame | `portfolio/assets/extension-export-demo.gif` |
| Workflow doc | `workflows/05-slicer-extension-workflow.md` |

## Acceptance criteria

- [ ] `ScriptedLoadableModule` with Widget + Logic pattern
- [ ] QC summary panel for loaded volume
- [ ] Dice computation vs reference labelmap
- [ ] One-click export writes DICOM-SEG + provenance JSON
- [ ] Build/install instructions in README
- [ ] Workflow documents architecture decisions

## Extension features

1. **QC Summary** — spacing, slice count, volume name
2. **Validation Metrics** — Dice vs `ReferenceLabelmap` node
3. **Export** — DICOM-SEG + provenance sidecar to chosen directory

## Build options

### Option A — Developer install (fastest)

Copy `extensions/MedAssetPipeline/MedAssetPipeline/` into Slicer's scripted modules path or add via Extension Wizard.

### Option B — CMake build

```bash
mkdir build && cd build
cmake -DSlicer_DIR=/path/to/Slicer-build ..
make
```

## Session outline

1. Scaffold module with Extension Wizard or repo template (1 hr)
2. Implement Logic: QC, Dice, export (3 hr)
3. Build Widget UI with collapsible sections (2 hr)
4. Test on MSD case, screenshot UI (1 hr)
5. Document in workflow doc (1 hr)
