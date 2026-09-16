"""Locate the bundled collection without installing the package first."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

DOC_DIR = ROOT / "examples" / "documents"
TRUTH_DIR = DOC_DIR / "truth"
AUTHOR_DIR = ROOT / "examples" / "authors"
REPORT_DIR = ROOT / "examples" / "reports"
GENERATED_DIR = ROOT / "examples" / "generated"
