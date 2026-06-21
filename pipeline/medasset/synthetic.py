"""Generate synthetic CT + spleen label for CI and offline demos."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import SimpleITK as sitk

from medasset.io import ensure_dir, save_label


def create_synthetic_case(
    output_dir: Path,
    case_id: str = "spleen_001",
    size: tuple[int, int, int] = (64, 128, 128),
    spacing: tuple[float, float, float] = (2.0, 1.0, 1.0),
) -> tuple[Path, Path]:
    """Create a synthetic ellipsoid 'spleen' in a CT-like volume."""
    z, y, x = size
    arr = np.random.normal(-100, 30, size).astype(np.float32)
    # Add body-like background
    arr += 40

    cz, cy, cx = z // 2, y // 2, x // 2
    zz, yy, xx = np.ogrid[:z, :y, :x]
    mask = ((zz - cz) / 12) ** 2 + ((yy - cy) / 25) ** 2 + ((xx - cx) / 20) ** 2 <= 1
    arr[mask] = np.random.normal(55, 10, mask.sum())

    image = sitk.GetImageFromArray(arr)
    image.SetSpacing(spacing)
    image.SetOrigin((0.0, 0.0, 0.0))

    label_arr = mask.astype(np.uint8)
    label = sitk.GetImageFromArray(label_arr)
    label.CopyInformation(image)

    processed = ensure_dir(output_dir / "processed")
    ref_dir = ensure_dir(output_dir / "labels" / "reference")

    image_path = processed / f"{case_id}.nii.gz"
    label_path = ref_dir / f"{case_id}.nii.gz"
    sitk.WriteImage(image, str(image_path), useCompression=True)
    save_label(label, label_path)

    return image_path, label_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic MSD-style case")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--case-id", default="spleen_001")
    args = parser.parse_args()
    create_synthetic_case(args.output_dir, args.case_id)
    print(f"Created synthetic case: {args.case_id}")


if __name__ == "__main__":
    main()
