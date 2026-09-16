"""I/O round trips against a temporary problem directory."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from style_change.io import load_problem, load_problem_dir, load_solution, write_solution


class IoTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "problem-toy.txt").write_text("aaaa\n\nbbbb\n\ncccc\n", encoding="utf-8")
            (root / "truth-problem-toy.json").write_text(
                json.dumps({"authors": 2, "changes": [0, 1]}),
                encoding="utf-8",
            )
            problem = load_problem(root / "problem-toy.txt")
            self.assertEqual(problem.problem_id, "toy")
            self.assertEqual(problem.paragraphs, ["aaaa", "bbbb", "cccc"])
            self.assertEqual(problem.gold_changes, [0, 1])
            self.assertEqual(problem.authors, 2)

            dest = write_solution(root / "out", "toy", [0, 1])
            self.assertEqual(dest.name, "solution-problem-toy.json")
            self.assertEqual(load_solution(dest), [0, 1])

            loaded = load_problem_dir(root)
            self.assertEqual(len(loaded), 1)

    def test_rejects_wrong_filename(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "not-a-problem.txt"
            path.write_text("hello", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_problem(path)

    def test_gold_length_must_match_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "problem-x.txt").write_text("one\n\ntwo\n", encoding="utf-8")
            (root / "truth-problem-x.json").write_text(
                json.dumps({"changes": [0, 1]}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_problem(root / "problem-x.txt")


if __name__ == "__main__":
    unittest.main()
