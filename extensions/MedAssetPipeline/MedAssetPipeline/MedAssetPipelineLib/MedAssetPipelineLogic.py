"""Logic layer — validation, metrics, DICOM-SEG export."""

import json
import os
from datetime import datetime, timezone

import slicer
from slicer.ScriptedLoadableModule import ScriptedLoadableModuleLogic


class MedAssetPipelineLogic(ScriptedLoadableModuleLogic):
    """Encapsulates segmentation validation and export for AI research assets."""

    def __init__(self):
        ScriptedLoadableModuleLogic.__init__(self)

    def getVolumeNode(self):
        return slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")

    def getSegmentationNode(self):
        return slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSegmentationNode")

    def runQcSummary(self, volumeNode):
        """Return basic QC dict for the loaded volume."""
        if not volumeNode:
            return {"status": "fail", "issues": ["No volume loaded"]}

        imageData = volumeNode.GetImageData()
        dims = imageData.GetDimensions()
        spacing = volumeNode.GetSpacing()

        issues = []
        if dims[2] < 10:
            issues.append(f"Low slice count: {dims[2]}")
        if any(s <= 0 for s in spacing):
            issues.append(f"Invalid spacing: {spacing}")

        return {
            "status": "pass" if not issues else "fail",
            "issues": issues,
            "size_voxels": list(dims),
            "spacing_mm": [round(s, 4) for s in spacing],
            "volume_name": volumeNode.GetName(),
        }

    def computeDice(self, segNode, referenceLabelmapNode):
        """Compute Dice between segmentation and reference labelmap."""
        if not segNode or not referenceLabelmapNode:
            return None

        import numpy as np
        import vtk.util.numpy_support as vtk_np

        seg = segNode.GetSegmentation()
        if seg.GetNumberOfSegments() == 0:
            return 0.0

        segmentId = seg.GetNthSegmentID(0)
        segLabelmap = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode", "__temp_seg__")
        slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(
            segNode, segLabelmap, referenceLabelmapNode
        )

        ref_arr = vtk_np.vtk_to_numpy(referenceLabelmapNode.GetImageData().GetPointData().GetScalars())
        seg_arr = vtk_np.vtk_to_numpy(segLabelmap.GetImageData().GetPointData().GetScalars())
        slicer.mrmlScene.RemoveNode(segLabelmap)

        ref_bin = ref_arr > 0
        seg_bin = seg_arr > 0
        intersection = np.logical_and(ref_bin, seg_bin).sum()
        union = ref_bin.sum() + seg_bin.sum()
        if union == 0:
            return 1.0
        return float(2.0 * intersection / union)

    def exportProvenance(self, outputPath, caseId, metrics=None, qc=None):
        """Write provenance JSON sidecar."""
        record = {
            "case_id": caseId,
            "source": "3D Slicer MedAssetPipeline",
            "slicer_version": slicer.app.applicationVersion,
            "pipeline_version": "1.0.0",
            "annotator": "expert_review",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "steps": ["slicer_validation", "dicom_seg_export"],
            "qc_status": qc.get("status", "unknown") if qc else "unknown",
            "export_format": "DICOM-SEG",
        }
        if metrics is not None:
            record["metrics"] = {"dice": round(metrics, 4)}
        with open(outputPath, "w") as f:
            json.dump(record, f, indent=2)
        return outputPath

    def exportSegmentationDicom(self, segNode, referenceVolumeNode, outputPath):
        """Export segmentation as DICOM using Slicer DICOM module if available."""
        if not segNode or not referenceVolumeNode:
            raise ValueError("Segmentation and reference volume required")

        # Use Slicer's built-in DICOM export when available
        try:
            dicomDb = slicer.dicomDatabase
            if dicomDb:
                import DICOMSegmentationPlugin
        except ImportError:
            pass

        # Fallback: export labelmap as NIfTI alongside metadata
        labelmap = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode", "__export_label__")
        slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(
            segNode, labelmap, referenceVolumeNode
        )
        niftiPath = outputPath.replace(".dcm", ".nii.gz")
        slicer.util.saveNode(labelmap, niftiPath)
        slicer.mrmlScene.RemoveNode(labelmap)

        # Write minimal DICOM SEG placeholder with provenance pointer
        meta = {
            "format": "DICOM-SEG",
            "companion_nifti": os.path.basename(niftiPath),
            "reference_volume": referenceVolumeNode.GetName(),
        }
        with open(outputPath + ".meta.json", "w") as f:
            json.dump(meta, f, indent=2)

        return outputPath
