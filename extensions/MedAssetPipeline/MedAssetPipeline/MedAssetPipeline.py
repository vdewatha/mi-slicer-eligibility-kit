import os
import unittest
import vtk
import qt
import ctk
import slicer
from slicer.ScriptedLoadableModule import *


class MedAssetPipeline(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "MedAsset Pipeline"
        self.parent.categories = ["Segmentation"]
        self.parent.dependencies = []
        self.parent.contributors = ["MedAsset Pipeline Authors"]
        self.parent.helpText = """
        Validate segmentations, compute Dice/HD95 vs reference, and export DICOM-SEG
        with provenance JSON for AI research digital asset workflows.
        """
        self.parent.acknowledgementText = """
        Part of the MI Slicer Eligibility Kit — medical imaging digital asset pipeline.
        """


class MedAssetPipelineWidget(ScriptedLoadableModuleWidget, vtk.vtkObject):
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        from MedAssetPipelineLib.MedAssetPipelineWidget import MedAssetPipelineWidget as Widget
        self.widget = Widget(self.parent)
        self.widget.setup()


class MedAssetPipelineLogic(ScriptedLoadableModuleLogic):
    pass


class MedAssetPipelineTest(ScriptedLoadableModuleTest):
    def runTest(self):
        self.setDelayDisplay(0)
        self.test_logicImport()

    def test_logicImport(self):
        from MedAssetPipelineLib.MedAssetPipelineLogic import MedAssetPipelineLogic
        logic = MedAssetPipelineLogic()
        self.assertIsNotNone(logic)
