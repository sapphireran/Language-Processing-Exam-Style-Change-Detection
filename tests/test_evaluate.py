"""Macro-F1 and the worked booklet example."""

from __future__ import annotations

import unittest

from style_change.evaluate import confusion, evaluate_changes, macro_f1, precision_recall_f1


class EvaluateTests(unittest.TestCase):
    def test_perfect_score(self) -> None:
        gold = [0, 1, 0, 1]
        self.assertEqual(macro_f1(gold, gold), 1.0)

    def test_all_zero_on_mixed(self) -> None:
        gold = [0, 1, 0, 1]
        pred = [0, 0, 0, 0]
        self.assertLess(macro_f1(gold, pred), 0.5)

    def test_empty_is_perfect(self) -> None:
        self.assertEqual(macro_f1([], []), 1.0)

    def test_booklet_example(self) -> None:
        gold = [0, 0, 1, 0]
        pred = [0, 1, 1, 0]
        counts = confusion(gold, pred)
        self.assertEqual((counts.tp, counts.fp, counts.tn, counts.fn), (1, 1, 2, 0))
        f1_pos = precision_recall_f1(counts, 1)[2]
        f1_neg = precision_recall_f1(counts, 0)[2]
        self.assertAlmostEqual(f1_pos, 2 / 3)
        self.assertAlmostEqual(f1_neg, 0.8)
        self.assertAlmostEqual(macro_f1(gold, pred), (0.8 + 2 / 3) / 2)

    def test_length_mismatch_raises(self) -> None:
        with self.assertRaises(ValueError):
            macro_f1([0, 1], [0])

    def test_evaluate_changes_mean(self) -> None:
        result = evaluate_changes(
            {"a": [0, 1], "b": [1, 1]},
            {"a": [0, 1], "b": [1, 1]},
        )
        self.assertEqual(result.mean_macro_f1, 1.0)
        self.assertEqual(result.pooled_macro_f1, 1.0)

    def test_missing_prediction_raises(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_changes({"a": [0]}, {})


if __name__ == "__main__":
    unittest.main()
