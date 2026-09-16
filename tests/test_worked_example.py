"""Yule's K and the tiny cosine from docs/05-worked-example.md."""

from __future__ import annotations

import math
import unittest
from collections import Counter

from scarfjoint.distances import cosine, cosine_distance, jensen_shannon
from scarfjoint.features import extract_features
from scarfjoint.richness import richness

P1 = (
    "I think we should take the late boat. I cannot stand the morning "
    "crowd on the pier."
)
P2 = (
    "The analysis suggests that tidal delay should be treated as a "
    "structural constraint rather than a residual error."
)


class WorkedExampleTests(unittest.TestCase):
    def test_yule_k_toy_bag(self) -> None:
        stats = richness(("the", "the", "boat", "the", "pier"))
        self.assertEqual(stats.n_tokens, 5)
        self.assertEqual(stats.n_types, 3)
        self.assertAlmostEqual(stats.yule_k, 2400.0)

    def test_token_counts(self) -> None:
        f1 = extract_features(P1)
        f2 = extract_features(P2)
        self.assertEqual(f1.n_words, 17)
        self.assertEqual(f2.n_words, 18)
        self.assertEqual(f1.tokens.words_lower.count("i"), 2)
        self.assertEqual(f1.tokens.words_lower.count("the"), 3)
        self.assertEqual(f2.tokens.words_lower.count("a"), 2)

    def test_full_basis_cosine(self) -> None:
        f1 = extract_features(P1)
        f2 = extract_features(P2)
        self.assertAlmostEqual(cosine(f1.function_word_rel, f2.function_word_rel), 0.293, places=3)
        self.assertAlmostEqual(
            cosine_distance(f1.function_word_rel, f2.function_word_rel), 0.707, places=3
        )
        self.assertAlmostEqual(
            jensen_shannon(f1.function_word_rel, f2.function_word_rel), 0.491, places=3
        )

    def test_six_word_subset_cosine(self) -> None:
        f1 = extract_features(P1)
        f2 = extract_features(P2)
        subset = ["i", "the", "that", "should", "a", "as"]

        def vec(feat) -> list[float]:
            n = feat.n_words
            counts = Counter(feat.tokens.words_lower)
            return [counts[w] / n for w in subset]

        a, b = vec(f1), vec(f2)
        dot = sum(x * y for x, y in zip(a, b, strict=True))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        self.assertAlmostEqual(dot / (na * nb), 0.378, places=3)

    def test_register_contrast(self) -> None:
        f1 = extract_features(P1)
        f2 = extract_features(P2)
        self.assertGreater(f1.first_person_rate, 0.15)
        self.assertEqual(f2.first_person_rate, 0.0)
        self.assertGreater(f2.academic_rate, f1.academic_rate)
        self.assertGreater(f2.mean_sent_len, f1.mean_sent_len)
        self.assertGreater(f1.flesch_proxy, f2.flesch_proxy)


if __name__ == "__main__":
    unittest.main()
