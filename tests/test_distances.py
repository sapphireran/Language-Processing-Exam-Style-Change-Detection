"""Distances and richness edge cases."""

from __future__ import annotations

import unittest

from scarfjoint.distances import cosine, euclidean, jaccard, jensen_shannon
from scarfjoint.features import extract_features
from scarfjoint.richness import richness


class DistanceTests(unittest.TestCase):
    def test_identical_cosine(self) -> None:
        v = (0.2, 0.3, 0.5)
        self.assertAlmostEqual(cosine(v, v), 1.0)

    def test_orthogonal_cosine(self) -> None:
        self.assertAlmostEqual(cosine((1.0, 0.0), (0.0, 1.0)), 0.0)

    def test_js_identical_is_zero(self) -> None:
        self.assertAlmostEqual(jensen_shannon((0.2, 0.8), (0.2, 0.8)), 0.0, places=6)

    def test_jaccard_empty(self) -> None:
        self.assertEqual(jaccard(set(), set()), 1.0)
        self.assertEqual(jaccard({"a"}, set()), 0.0)

    def test_euclidean(self) -> None:
        self.assertAlmostEqual(euclidean((0.0, 0.0), (3.0, 4.0)), 5.0)

    def test_features_are_deterministic(self) -> None:
        text = "I cannot stand the morning boat, and I will not pretend otherwise."
        a = extract_features(text)
        b = extract_features(text)
        self.assertEqual(a.function_word_rel, b.function_word_rel)
        self.assertEqual(a.dense, b.dense)
        self.assertGreater(a.contraction_rate, 0.0)

    def test_empty_richness(self) -> None:
        empty = richness(())
        self.assertEqual(empty.n_tokens, 0)
        self.assertEqual(empty.yule_k, 0.0)


if __name__ == "__main__":
    unittest.main()
