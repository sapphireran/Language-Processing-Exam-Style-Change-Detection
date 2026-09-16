from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

CORPUS = ROOT / "examples" / "corpus"
REPORTS = ROOT / "examples" / "reports"


def problem(ident: int) -> Path:
    matches = sorted(CORPUS.glob(f"problem-{ident:02d}-*.txt"))
    if not matches:
        raise FileNotFoundError(ident)
    return matches[0]
