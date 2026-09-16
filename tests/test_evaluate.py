"""Locked evaluation arithmetic from docs/04-evaluation.md."""

from __future__ import annotations

import unittest

from scarfjoint.evaluate import binary_f1, document_scores, macro_f1


class EvaluateTests(unittest.TestCase):
    def test_worked_confusion_matrix(self) -> None:
        gold = [0, 1, 0, 1]
        pred = [0, 1, 1, 1]
        bundle = document_scores(gold, pred)
        self.assertEqual(bundle.tp, 2)
        self.assertEqual(bundle.fp, 1)
        self.assertEqual(bundle.tn, 1)
        self.assertEqual(bundle.fn, 0)
        self.assertAlmostEqual(bundle.precision, 2 / 3)
        self.assertAlmostEqual(bundle.recall, 1.0)
        self.assertAlmostEqual(bundle.f1, 0.8)
        self.assertAlmostEqual(bundle.accuracy, 0.75)
        self.assertAlmostEqual(bundle.macro_f1, 0.5 * (0.8 + 2 / 3))
        self.assertFalse(bundle.exact)

    def test_all_zeros_single_author(self) -> None:
        gold = [0, 0, 0, 0, 0]
        pred = [0, 0, 0, 0, 0]
        bundle = document_scores(gold, pred)
        self.assertEqual(bundle.f1, 0.0)  # no positive class predicted or present
        self.assertAlmostEqual(bundle.accuracy, 1.0)
        self.assertTrue(bundle.exact)
        # class-0 F1 is 1, so macro is 0.5
        self.assertAlmostEqual(bundle.macro_f1, 0.5)

    def test_helpers_match_bundle(self) -> None:
        gold = [0, 1, 0, 1]
        pred = [0, 1, 1, 1]
        self.assertAlmostEqual(binary_f1(gold, pred), 0.8)
        self.assertAlmostEqual(macro_f1(gold, pred), 0.5 * (0.8 + 2 / 3))

    def test_length_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            document_scores([0, 1], [0])


if __name__ == "__main__":
    unittest.main()
