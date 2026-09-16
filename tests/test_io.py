"""I/O helpers and PAN-shaped names."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scarfjoint.io import load_problem, solution_name_for, truth_path_for, write_solution

CORPUS = Path(__file__).resolve().parents[1] / "examples" / "corpus"


class IoTests(unittest.TestCase):
    def test_truth_path(self) -> None:
        problem = CORPUS / "easy" / "problem-01-ferry-marsh-knit.txt"
        self.assertEqual(
            truth_path_for(problem).name,
            "truth-problem-01-ferry-marsh-knit.json",
        )
        self.assertEqual(
            solution_name_for(problem),
            "solution-problem-01-ferry-marsh-knit.json",
        )

    def test_load_uses_newline_flag_and_splits(self) -> None:
        doc = load_problem(CORPUS / "easy" / "problem-01-ferry-marsh-knit.txt")
        self.assertEqual(len(doc.paragraphs), 6)
        self.assertEqual(doc.problem_id, "01-ferry-marsh-knit")

    def test_write_solution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "solution-problem-9.json"
            write_solution(dest, [0, 1, 0])
            payload = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(payload, {"changes": [0, 1, 0]})


if __name__ == "__main__":
    unittest.main()
