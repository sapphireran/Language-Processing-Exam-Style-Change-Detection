"""Every bundled problem has gold of the right length; easy/single bands hold."""

from __future__ import annotations

import unittest
from collections import defaultdict
from pathlib import Path

from scarfjoint.detectors import ScarfDetector
from scarfjoint.evaluate import document_scores
from scarfjoint.io import iter_corpus

CORPUS = Path(__file__).resolve().parents[1] / "examples" / "corpus"


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.docs = iter_corpus(CORPUS)
        cls.detector = ScarfDetector()

    def test_twelve_documents(self) -> None:
        self.assertEqual(len(self.docs), 12)

    def test_gold_length_matches_paragraphs(self) -> None:
        for doc in self.docs:
            gold = doc.gold_changes
            self.assertIsNotNone(gold, doc.path)
            self.assertEqual(len(gold), len(doc.paragraphs) - 1, doc.path)
            self.assertGreaterEqual(len(doc.paragraphs), 4, doc.path)
            for para in doc.paragraphs:
                self.assertGreater(len(para.split()), 40, doc.path)

    def test_easy_band_is_exact(self) -> None:
        for doc in self.docs:
            if doc.truth and doc.truth.get("band") == "easy":
                pred = self.detector.detect(doc.paragraphs).changes
                self.assertEqual(pred, doc.gold_changes, doc.path)

    def test_single_author_is_quiet(self) -> None:
        for doc in self.docs:
            if doc.truth and doc.truth.get("band") == "single_author":
                pred = self.detector.detect(doc.paragraphs).changes
                self.assertEqual(pred, doc.gold_changes, doc.path)
                self.assertTrue(all(bit == 0 for bit in pred), doc.path)

    def test_hard_is_not_trivial(self) -> None:
        """Hard pages must remain a place the baseline can fail."""
        scores = []
        for doc in self.docs:
            if doc.truth and doc.truth.get("band") == "hard":
                pred = self.detector.detect(doc.paragraphs).changes
                bundle = document_scores(doc.gold_changes, pred)
                scores.append(bundle.exact)
        self.assertTrue(any(not exact for exact in scores))

    def test_topic_does_not_secretly_vote(self) -> None:
        doc = next(d for d in self.docs if d.path.name.startswith("problem-01"))
        plain = self.detector.detect(doc.paragraphs)
        self.assertTrue(any("not a vote" in note or "diagnostic" in note for note in plain.notes))
        leaked = ScarfDetector(use_topic=True).detect(doc.paragraphs)
        self.assertNotEqual(leaked.notes, plain.notes)

    def test_bands_present(self) -> None:
        bands = defaultdict(int)
        for doc in self.docs:
            bands[str(doc.truth.get("band"))] += 1
        self.assertEqual(bands["easy"], 3)
        self.assertEqual(bands["medium"], 3)
        self.assertEqual(bands["hard"], 3)
        self.assertEqual(bands["single_author"], 3)


if __name__ == "__main__":
    unittest.main()
