"""Detectors and adaptive thresholds."""

from __future__ import annotations

import unittest

from style_change.detectors import (
    EnsembleDetector,
    adaptive_threshold,
    apply_threshold,
    build_detector,
    char3_distances,
    function_word_distances,
    stylometric_distances,
)


CASUAL = (
    "I'm honestly not sure we should keep going. It's late and you're "
    "already tired. We can grab soup and call it. I don't care about the plan."
)
FORMAL = (
    "The analysis therefore finds insufficient evidence for the claimed "
    "effect. Moreover, the measurement protocol cannot separate seasonal "
    "drift from the intervention. Further study is required before adoption."
)
CASUAL_2 = (
    "Yeah, soup is fine. I'll text you when I get off the bus. Don't wait "
    "up if I'm slow. I'm grabbing headphones and a pastry."
)


class DetectorTests(unittest.TestCase):
    def test_build_unknown_name(self) -> None:
        with self.assertRaises(ValueError):
            build_detector("nope")

    def test_distances_match_boundary_count(self) -> None:
        paras = [CASUAL, CASUAL_2, FORMAL]
        self.assertEqual(len(stylometric_distances(paras)), 2)
        self.assertEqual(len(char3_distances(paras)), 2)
        self.assertEqual(len(function_word_distances(paras)), 2)

    def test_ensemble_finds_the_formal_switch(self) -> None:
        paras = [CASUAL, CASUAL_2, FORMAL]
        scores = EnsembleDetector().distances(paras)
        self.assertGreater(scores[1], scores[0])
        pred = EnsembleDetector().predict(paras)
        self.assertEqual(pred[1], 1)

    def test_single_paragraph_predicts_nothing(self) -> None:
        self.assertEqual(EnsembleDetector().predict(["only one"]), [])

    def test_adaptive_threshold_homogoneous_is_above_max(self) -> None:
        distances = [0.11, 0.12, 0.13]
        cut = adaptive_threshold(distances)
        self.assertGreater(cut, max(distances))
        self.assertEqual(apply_threshold(distances, cut), [0, 0, 0])

    def test_adaptive_threshold_wide_range_splits(self) -> None:
        distances = [0.10, 0.80]
        cut = adaptive_threshold(distances)
        labels = apply_threshold(distances, cut)
        self.assertEqual(labels, [0, 1])

    def test_named_detectors_run(self) -> None:
        paras = [CASUAL, FORMAL]
        for name in ("ensemble", "stylometric", "char3", "function_word"):
            pred = build_detector(name).predict(paras)
            self.assertEqual(len(pred), 1)
            self.assertIn(pred[0], (0, 1))


if __name__ == "__main__":
    unittest.main()
