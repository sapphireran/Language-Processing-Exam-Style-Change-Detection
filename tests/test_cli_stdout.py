from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path

from hingemark.cli import main

ROOT = Path(__file__).resolve().parents[1]


class DetectTests(unittest.TestCase):
    def test_detect_prints_a_list(self) -> None:
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            code = main(["detect", str(ROOT / "examples/corpus/problem-01-canal-then-lot.txt")])
        finally:
            sys.stdout = old
        self.assertEqual(code, 0)
        out = buf.getvalue().strip()
        self.assertTrue(out.startswith("[") and out.endswith("]"))

    def test_split_counts(self) -> None:
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            code = main(["split", str(ROOT / "examples/corpus/problem-01-canal-then-lot.txt")])
        finally:
            sys.stdout = old
        self.assertEqual(code, 0)
        self.assertIn("7 units, 6 hinges", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
