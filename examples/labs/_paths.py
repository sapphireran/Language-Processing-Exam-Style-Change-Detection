"""Make `import quoin` and the corpus root work when labs are run as scripts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

CORPUS = ROOT / "examples" / "corpus"
REPORTS = ROOT / "examples" / "reports"
