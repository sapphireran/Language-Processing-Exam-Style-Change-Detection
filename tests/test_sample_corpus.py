"""The synthetic sample corpus is internally consistent and solvable."""

from __future__ import annotations

import unittest
from pathlib import Path

from style_change.detectors import EnsembleDetector
from style_change.evaluate import evaluate_changes, macro_f1
from style_change.io import load_problem_dir

ROOT = Path(__file__).resolve().parents[1] / "examples" / "sample_problems"
SPLITS = ("easy", "medium", "hard", "single_author")


class SampleCorpusTests(unittest.TestCase):
    def test_gold_lengths_and_labels(self) -> None:
        for split in SPLITS:
            problems = load_problem_dir(ROOT / split)
            self.assertGreaterEqual(len(problems), 2, split)
            for problem in problems:
                self.assertIsNotNone(problem.gold_changes)
                self.assertEqual(len(problem.gold_changes), problem.n_boundaries)
                self.assertTrue(all(v in (0, 1) for v in problem.gold_changes))
                if problem.authors == 1:
                    self.assertTrue(all(v == 0 for v in problem.gold_changes))

    def test_easy_001_recovers_both_author_changes(self) -> None:
        problem = next(p for p in load_problem_dir(ROOT / "easy") if p.problem_id == "001")
        pred = EnsembleDetector().predict(problem.paragraphs)
        self.assertEqual(len(pred), 4)
        # Same-author hike pair and same-author memo pair should stay 0.
        self.assertEqual(pred[0], 0)
        self.assertEqual(pred[2], 0)
        # Hiking → memo and memo → recipe should fire.
        self.assertEqual(pred[1], 1)
        self.assertEqual(pred[3], 1)

    def test_single_author_stays_all_zero(self) -> None:
        problems = load_problem_dir(ROOT / "single_author")
        detector = EnsembleDetector()
        for problem in problems:
            pred = detector.predict(problem.paragraphs)
            self.assertEqual(pred, problem.gold_changes)

    def test_easy_split_beats_always_zero(self) -> None:
        problems = load_problem_dir(ROOT / "easy")
        detector = EnsembleDetector()
        gold = {p.problem_id: p.gold_changes for p in problems}
        pred = {p.problem_id: detector.predict(p.paragraphs) for p in problems}
        zeros = {p.problem_id: [0] * p.n_boundaries for p in problems}
        model = evaluate_changes(gold, pred)
        baseline = evaluate_changes(gold, zeros)
        self.assertGreater(model.mean_macro_f1, baseline.mean_macro_f1)

    def test_medium_001_marks_the_register_seam(self) -> None:
        problem = next(
            p for p in load_problem_dir(ROOT / "medium") if p.problem_id == "001"
        )
        pred = EnsembleDetector().predict(problem.paragraphs)
        self.assertEqual(len(pred), 3)
        self.assertEqual(pred[1], 1)
        self.assertGreaterEqual(macro_f1(problem.gold_changes, pred), 0.5)


if __name__ == "__main__":
    unittest.main()
