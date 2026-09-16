"""Resolve repository paths whether scripts are run from root or examples/."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
CORPUS = ROOT / "examples" / "corpus"
REPORTS = ROOT / "examples" / "reports"
GENERATED = ROOT / "examples" / "generated"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def require_corpus() -> Path:
    if not CORPUS.is_dir():
        raise SystemExit(f"missing corpus at {CORPUS}")
    return CORPUS
