import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_hand_calculation_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_hand_calculation.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ok" in result.stdout


def test_curriculum_easy_eval():
    result = subprocess.run(
        [sys.executable, "-m", "stylechange.cli", "eval", "examples/data/easy"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
    )
    assert result.returncode == 0, result.stderr
    assert "macro-F1 = 1.000" in result.stdout
