"""Vector distances and z-scoring."""

from __future__ import annotations

import unittest

from style_change.distances import cosine_distance, cosine_similarity, jensen_shannon, zscore_columns
from style_change.ngrams import aligned_vectors, char_ngrams, normalized_profile


class DistanceTests(unittest.TestCase):
    def test_identical_cosine(self) -> None:
        self.assertAlmostEqual(cosine_similarity([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0)
        self.assertAlmostEqual(cosine_distance([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 0.0)

    def test_orthogonal_cosine(self) -> None:
        self.assertAlmostEqual(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)

    def test_zero_vector_cosine(self) -> None:
        self.assertEqual(cosine_similarity([0.0, 0.0], [1.0, 2.0]), 0.0)

    def test_js_identical(self) -> None:
        self.assertAlmostEqual(jensen_shannon([0.2, 0.8], [0.2, 0.8]), 0.0)

    def test_js_disjoint(self) -> None:
        self.assertGreater(jensen_shannon([1.0, 0.0], [0.0, 1.0]), 0.5)

    def test_zscore_columns_zero_mean_unit_var(self) -> None:
        scaled = zscore_columns([[1.0, 10.0], [3.0, 30.0], [5.0, 50.0]])
        col0 = [row[0] for row in scaled]
        self.assertAlmostEqual(sum(col0) / 3, 0.0)
        self.assertAlmostEqual(sum(v * v for v in col0) / 3, 1.0)

    def test_zscore_constant_column_stays_zero(self) -> None:
        scaled = zscore_columns([[2.0, 1.0], [2.0, 3.0]])
        self.assertEqual([row[0] for row in scaled], [0.0, 0.0])

    def test_char_ngrams_and_align(self) -> None:
        left = normalized_profile(char_ngrams("the cat", n=3))
        right = normalized_profile(char_ngrams("the bat", n=3))
        a, b = aligned_vectors(left, right)
        self.assertEqual(len(a), len(b))
        self.assertGreater(len(a), 0)
        self.assertLess(cosine_distance(a, b), 1.0)


if __name__ == "__main__":
    unittest.main()
