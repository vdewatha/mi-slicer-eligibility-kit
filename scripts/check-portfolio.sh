#!/usr/bin/env bash
# Validates MI Slicer Eligibility Portfolio Kit deliverables before survey submission.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS="$ROOT/portfolio/assets"
WORKFLOWS="$ROOT/workflows"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

errors=0
warnings=0

check_file() {
  local path="$1"
  local label="$2"
  if [[ -f "$path" ]]; then
    echo -e "${GREEN}✓${NC} $label"
  else
    echo -e "${RED}✗${NC} Missing: $label"
    echo "    Expected: $path"
    errors=$((errors + 1))
  fi
}

check_workflow_filled() {
  local path="$1"
  local label="$2"
  if [[ ! -f "$path" ]]; then
    echo -e "${RED}✗${NC} Missing workflow: $label"
    errors=$((errors + 1))
    return
  fi
  local empty_decisions
  empty_decisions=$(grep -c '\*\*What:\*\* $' "$path" 2>/dev/null || true)
  empty_decisions=${empty_decisions:-0}
  if [[ "$empty_decisions" -gt 2 ]]; then
    echo -e "${YELLOW}⚠${NC} Workflow may be incomplete: $label"
    warnings=$((warnings + 1))
  else
    echo -e "${GREEN}✓${NC} Workflow doc present: $label"
  fi
}

echo ""
echo "MI Slicer Eligibility Portfolio — Validation"
echo "============================================="
echo ""

echo "Portfolio assets:"
check_file "$ASSETS/qc-report.json" "QC report (JSON)"
check_file "$ASSETS/qc-summary.png" "QC summary chart"
check_file "$ASSETS/dicom-import-session.png" "DICOM import session"
check_file "$ASSETS/spleen-segmentation-overlay.png" "Segmentation overlay"
check_file "$ASSETS/spleen-3d-render.png" "3D render"
check_file "$ASSETS/segment-editor-session.png" "Segment Editor session"
check_file "$ASSETS/ai-correction-comparison.png" "AI correction comparison"
check_file "$ASSETS/segmentation-metrics.json" "Segmentation metrics"
check_file "$ASSETS/sample-spleen.dcm" "Sample DICOM-SEG"
check_file "$ASSETS/dicom-seg-roundtrip.png" "DICOM-SEG round-trip"
check_file "$ASSETS/extension-ui-session.png" "Extension UI session"
check_file "$ASSETS/extension-export-demo.png" "Extension export demo"

echo ""
echo "Workflow documentation:"
check_workflow_filled "$WORKFLOWS/01-dicom-ingest-qc-workflow.md" "DICOM ingest QC"
check_workflow_filled "$WORKFLOWS/02-segment-editor-workflow.md" "Segment Editor"
check_workflow_filled "$WORKFLOWS/03-ai-correction-loop-workflow.md" "AI correction loop"
check_workflow_filled "$WORKFLOWS/04-dicom-seg-export-workflow.md" "DICOM-SEG export"
check_workflow_filled "$WORKFLOWS/05-slicer-extension-workflow.md" "Slicer extension"

echo ""
echo "Portfolio site:"
check_file "$ROOT/portfolio/index.html" "Portfolio index.html"
check_file "$ROOT/portfolio/css/style.css" "Portfolio styles"
check_file "$ROOT/portfolio/js/main.js" "Portfolio scripts"

echo ""
echo "Pipeline:"
check_file "$ROOT/pipeline/medasset/cli.py" "Pipeline CLI"
check_file "$ROOT/extensions/MedAssetPipeline/MedAssetPipeline/MedAssetPipeline.py" "Slicer extension"

echo ""
echo "============================================="
if [[ "$errors" -eq 0 ]] && [[ "$warnings" -eq 0 ]]; then
  echo -e "${GREEN}All checks passed. Ready to deploy and submit.${NC}"
  exit 0
elif [[ "$errors" -eq 0 ]]; then
  echo -e "${YELLOW}$warnings warning(s). Review workflow docs before submitting.${NC}"
  exit 0
else
  echo -e "${RED}$errors missing item(s), $warnings warning(s).${NC}"
  exit 1
fi
