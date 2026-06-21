#!/usr/bin/env python3
"""Generate demo portfolio assets by running the full pipeline on synthetic data."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "pipeline"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=PIPELINE)


def main() -> int:
    venv = ROOT / ".venv"
    if not venv.exists():
        run(["make", "setup"])

    run(["make", "data-synthetic"])
    run(["make", "ingest"])
    run(["make", "qc"])
    run(["make", "infer"])
    run(["make", "metrics"])
    run(["make", "export"])
    run(["make", "figures"])
    print("Demo assets generated in portfolio/assets/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
