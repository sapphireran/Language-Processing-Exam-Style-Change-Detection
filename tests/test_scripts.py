import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_hand_calculation_script() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_hand_calculation.py")],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "hand calculations ok" in proc.stdout
