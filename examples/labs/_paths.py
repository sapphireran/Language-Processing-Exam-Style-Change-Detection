from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

CORPUS = ROOT / "examples" / "corpus"
REPORTS = ROOT / "examples" / "reports"
WALKTHROUGHS = ROOT / "examples" / "walkthroughs"
