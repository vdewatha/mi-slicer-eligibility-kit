set(MODULE_NAME MedAssetPipeline)

set(MODULE_PYTHON_SCRIPTS
  MedAssetPipeline.py
  MedAssetPipelineLib/__init__.py
  MedAssetPipelineLib/MedAssetPipelineLogic.py
  MedAssetPipelineLib/MedAssetPipelineWidget.py
  )

include(${Slicer_CMAKE_DIR}/SlicerMacroBuildScriptedModule.cmake)
SlicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  WITH_GENERIC_TESTS
  )
