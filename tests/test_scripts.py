import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = {**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")}


def _run(rel: str) -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / rel)],
        cwd=ROOT,
        env=ENV,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise AssertionError(f"{rel} failed\n{proc.stdout}\n{proc.stderr}")


class ScriptSmokeTests(unittest.TestCase):
    def test_curriculum_and_walkthroughs(self):
        _run("scripts/run_curriculum.py")
        _run("scripts/write_walkthroughs.py")
        named = ROOT / "examples" / "walkthroughs" / "problem-01-kiln-then-notice.md"
        self.assertTrue(named.exists())
        self.assertIn("true fold", named.read_text(encoding="utf-8"))

    def test_hand_lab_and_accuracy_lab(self):
        _run("examples/labs/01_feature_table.py")
        _run("examples/labs/08_accuracy_trap.py")


if __name__ == "__main__":
    unittest.main()
