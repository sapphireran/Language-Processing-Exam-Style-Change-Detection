"""Numbers in docs/06-worked-features.md should match the tokenizer."""

from __future__ import annotations

import unittest

from style_change.distances import cosine_distance, cosine_similarity
from style_change.features import extract_profile
from style_change.tokenize import words


P1 = "I don't want to wait. It's late."
P2 = "The committee therefore declines the proposal."


class WorkedExampleTests(unittest.TestCase):
    def test_token_lists(self) -> None:
        self.assertEqual(
            words(P1),
            ["i", "don't", "want", "to", "wait", "it's", "late"],
        )
        self.assertEqual(
            words(P2),
            ["the", "committee", "therefore", "declines", "the", "proposal"],
        )

    def test_rates_in_the_note(self) -> None:
        a = extract_profile(P1)
        b = extract_profile(P2)
        self.assertAlmostEqual(a.type_token_ratio, 1.0)
        self.assertAlmostEqual(b.type_token_ratio, 5 / 6)
        self.assertAlmostEqual(a.contraction_rate, 2 / 7)
        self.assertAlmostEqual(b.contraction_rate, 0.0)
        self.assertAlmostEqual(a.connective_rate, 0.0)
        self.assertAlmostEqual(b.connective_rate, 1 / 6)

    def test_two_d_cartoon_is_orthogonal(self) -> None:
        sim = cosine_similarity([2 / 7, 0.0], [0.0, 1 / 6])
        self.assertAlmostEqual(sim, 0.0)
        self.assertAlmostEqual(cosine_distance([2 / 7, 0.0], [0.0, 1 / 6]), 1.0)


if __name__ == "__main__":
    unittest.main()
