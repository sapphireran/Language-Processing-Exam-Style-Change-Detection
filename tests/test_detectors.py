from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from stylechange.detectors import (
    AlwaysZeroDetector,
    LogisticDetector,
    ThresholdDetector,
    UnsupervisedDetector,
    load_model,
    save_model,
)
from stylechange.io import Problem


def _problem(pid: str, sentences: list[str], authors: list[str]) -> Problem:
    changes = [0 if left == right else 1 for left, right in zip(authors, authors[1:])]
    return Problem(pid=pid, path=Path(f"{pid}.txt"), sentences=sentences, changes=changes)


class DetectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mira = [
            "However, the bloom remains relatively unstable although the pour is slow.",
            "A modest observation suggests that degassing appears somewhat active.",
            "These kitchen notes are generally treated as provisional associations.",
        ]
        self.jules = [
            "I don't wait that long, I just go for it!",
            "I'm not running a cafe, that's the whole method.",
            "Don't follow my kettle notes if you want pretty numbers.",
        ]
        self.train = [
            _problem("a", self.mira + self.jules, ["mira"] * 3 + ["jules"] * 3),
            _problem(
                "b",
                [
                    "Water mass was 15.0 g and bloom time was 45 s.",
                    "Dose was 15.0 g. Yield was 220 g.",
                    "The kettle ticked; the filter breathed a faint paper sweetness.",
                    "Oil starred the surface; bitterness arrived late.",
                ],
                ["hale", "hale", "nell", "nell"],
            ),
        ]

    def test_always_zero_length(self) -> None:
        pred = AlwaysZeroDetector().predict_document(self.mira + self.jules)
        self.assertEqual(pred, [0] * 5)

    def test_unsupervised_finds_large_jump(self) -> None:
        sentences = self.mira + self.jules
        pred = UnsupervisedDetector(k=0.4).predict_document(sentences)
        self.assertEqual(len(pred), 5)
        # The Mira/Jules seam is pair index 2.
        self.assertIn(1, pred)

    def test_logistic_learns_and_roundtrips(self) -> None:
        detector = LogisticDetector(epochs=400)
        detector.fit(self.train)
        pred = detector.predict_document(self.mira + self.jules)
        self.assertEqual(len(pred), 5)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "logistic.json"
            save_model(detector, path)
            restored = load_model(path)
            self.assertEqual(restored.predict_document(self.mira + self.jules), pred)

    def test_threshold_fit_sets_k(self) -> None:
        detector = ThresholdDetector()
        detector.fit(self.train)
        self.assertTrue(detector.fitted_)
        pred = detector.predict_document(self.mira + self.jules)
        self.assertEqual(len(pred), 5)


if __name__ == "__main__":
    unittest.main()
