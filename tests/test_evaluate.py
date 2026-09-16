from __future__ import annotations

import unittest

from stylechange.evaluate import evaluate_aligned, macro_f1, score_pairs


class EvaluateTests(unittest.TestCase):
    def test_perfect(self) -> None:
        gold = [0, 1, 0, 1]
        self.assertEqual(macro_f1(gold, gold), 1.0)
        self.assertEqual(score_pairs(gold, gold)["accuracy"], 1.0)

    def test_always_zero_on_one_third_changes(self) -> None:
        gold = [0, 0, 1, 0, 1, 0]
        pred = [0, 0, 0, 0, 0, 0]
        scores = score_pairs(gold, pred)
        self.assertAlmostEqual(scores["accuracy"], 4 / 6)
        self.assertEqual(scores["f1_1"], 0.0)
        self.assertAlmostEqual(scores["macro_f1"], 0.4, places=5)

    def test_length_mismatch_is_io_failure(self) -> None:
        result = evaluate_aligned({"001": [0, 1, 0]}, {"001": [0, 1]})
        self.assertEqual(result.io_failures, ["001"])
        self.assertEqual(result.pooled["n_pairs"], 0.0)

    def test_missing_prediction(self) -> None:
        result = evaluate_aligned({"001": [0, 1], "002": [1]}, {"001": [0, 1]})
        self.assertEqual(result.io_failures, ["002"])
        self.assertEqual(result.per_document["001"]["macro_f1"], 1.0)


if __name__ == "__main__":
    unittest.main()
