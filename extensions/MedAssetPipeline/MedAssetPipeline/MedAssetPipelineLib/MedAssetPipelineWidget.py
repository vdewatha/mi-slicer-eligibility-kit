"""Widget UI for MedAssetPipeline module."""

import os

import ctk
import qt
import slicer
from slicer.ScriptedLoadableModule import ScriptedLoadableModuleWidget

from MedAssetPipelineLib.MedAssetPipelineLogic import MedAssetPipelineLogic


class MedAssetPipelineWidget(ScriptedLoadableModuleWidget):
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        self.logic = MedAssetPipelineLogic()

        # Collapsible sections
        self.qcCollapsible = ctk.ctkCollapsibleButton()
        self.qcCollapsible.text = "QC Summary"
        self.layout.addWidget(self.qcCollapsible)
        qcForm = qt.QFormLayout(self.qcCollapsible)
        self.qcOutput = qt.QTextEdit()
        self.qcOutput.readOnly = True
        self.qcOutput.setMaximumHeight(120)
        qcForm.addRow("Status:", self.qcOutput)

        self.metricsCollapsible = ctk.ctkCollapsibleButton()
        self.metricsCollapsible.text = "Validation Metrics"
        self.layout.addWidget(self.metricsCollapsible)
        metricsForm = qt.QFormLayout(self.metricsCollapsible)
        self.diceLabel = qt.QLabel("—")
        metricsForm.addRow("Dice vs reference:", self.diceLabel)

        self.exportCollapsible = ctk.ctkCollapsibleButton()
        self.exportCollapsible.text = "Export"
        self.layout.addWidget(self.exportCollapsible)
        exportForm = qt.QFormLayout(self.exportCollapsible)

        self.caseIdInput = qt.QLineEdit("spleen_001")
        exportForm.addRow("Case ID:", self.caseIdInput)

        self.outputDirInput = qt.QLineEdit()
        browseBtn = qt.QPushButton("Browse…")
        browseBtn.connect("clicked(bool)", self.onBrowseOutput)
        dirRow = qt.QHBoxLayout()
        dirRow.addWidget(self.outputDirInput)
        dirRow.addWidget(browseBtn)
        exportForm.addRow("Output dir:", dirRow)

        # Action buttons
        self.runQcBtn = qt.QPushButton("Run QC")
        self.runQcBtn.connect("clicked(bool)", self.onRunQc)
        self.layout.addWidget(self.runQcBtn)

        self.computeDiceBtn = qt.QPushButton("Compute Dice")
        self.computeDiceBtn.connect("clicked(bool)", self.onComputeDice)
        self.layout.addWidget(self.computeDiceBtn)

        self.exportBtn = qt.QPushButton("Export DICOM-SEG + Provenance")
        self.exportBtn.connect("clicked(bool)", self.onExport)
        self.layout.addWidget(self.exportBtn)

        self.layout.addStretch(1)

    def onBrowseOutput(self):
        dirPath = qt.QFileDialog.getExistingDirectory(self.parent, "Select output directory")
        if dirPath:
            self.outputDirInput.setText(dirPath)

    def onRunQc(self):
        volume = self.logic.getVolumeNode()
        qc = self.logic.runQcSummary(volume)
        import json
        self.qcOutput.setPlainText(json.dumps(qc, indent=2))
        slicer.util.infoDisplay(f"QC: {qc['status']}")

    def onComputeDice(self):
        seg = self.logic.getSegmentationNode()
        volume = self.logic.getVolumeNode()
        if not seg or not volume:
            slicer.util.errorDisplay("Load a volume and segmentation first.")
            return
        ref = slicer.mrmlScene.GetFirstNodeByName("ReferenceLabelmap")
        if not ref:
            slicer.util.warningDisplay("No 'ReferenceLabelmap' node — Dice requires reference.")
            self.diceLabel.setText("N/A (no reference)")
            return
        dice = self.logic.computeDice(seg, ref)
        self.diceLabel.setText(f"{dice:.4f}" if dice is not None else "—")

    def onExport(self):
        seg = self.logic.getSegmentationNode()
        volume = self.logic.getVolumeNode()
        outDir = self.outputDirInput.text or os.path.expanduser("~/MedAssetExports")
        caseId = self.caseIdInput.text or "case_001"

        if not seg or not volume:
            slicer.util.errorDisplay("Load a volume and segmentation first.")
            return

        os.makedirs(outDir, exist_ok=True)
        segPath = os.path.join(outDir, f"{caseId}_seg.dcm")
        provPath = os.path.join(outDir, f"{caseId}_provenance.json")

        qc = self.logic.runQcSummary(volume)
        dice_text = self.diceLabel.text
        metrics = float(dice_text) if dice_text not in ("—", "N/A (no reference)") else None

        self.logic.exportSegmentationDicom(seg, volume, segPath)
        self.logic.exportProvenance(provPath, caseId, metrics=metrics, qc=qc)
        slicer.util.infoDisplay(f"Exported to {outDir}")
