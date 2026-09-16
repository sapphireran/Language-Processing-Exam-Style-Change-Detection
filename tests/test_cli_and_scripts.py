from __future__ import annotations

import io
import os
import subprocess
import sys
import unittest
from pathlib import Path

from hingemark.cli import main
from hingemark.handcalc import trap_numbers

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_trap(self) -> None:
        self.assertEqual(main(["trap"]), 0)

    def test_eval(self) -> None:
        self.assertEqual(main(["eval", str(ROOT / "examples/corpus")]), 0)

    def test_explain_return_mentions_writer(self) -> None:
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            code = main(["explain", str(ROOT / "examples/corpus/problem-22-canal-return.txt")])
        finally:
            sys.stdout = old
        self.assertEqual(code, 0)
        self.assertIn("writer came back", buf.getvalue())

    def test_demo(self) -> None:
        self.assertEqual(main(["demo", "--name", "two-mycologists"]), 0)


class ScriptTests(unittest.TestCase):
    def test_hand_calculation_script(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/check_hand_calculation.py")],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_topic_confound_lab(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "examples/labs/07_topic_confound.py")],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_trap_numbers_export(self) -> None:
        nums = trap_numbers()
        self.assertAlmostEqual(nums["macro_f1"], 0.4444444444, places=6)


if __name__ == "__main__":
    unittest.main()
