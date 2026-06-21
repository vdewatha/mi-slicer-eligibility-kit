cmake_minimum_required(VERSION 3.16.3)
project(MedAssetPipeline)

set(EXTENSION_NAME "MedAssetPipeline")
set(EXTENSION_HOMEPAGE "https://github.com/example/mi-slicer-eligibility-kit")
set(EXTENSION_CATEGORY "Segmentation")
set(EXTENSION_DESCRIPTION "Validate segmentations, compute metrics, and export DICOM-SEG with provenance for AI research asset pipelines.")
set(EXTENSION_ICONURL "")
set(EXTENSION_SCREENSHOTURLS "")
set(EXTENSION_DEPENDS "NA")

find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

add_subdirectory(MedAssetPipeline)
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
