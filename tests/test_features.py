"""Stylometric features stay finite and move with obvious register shifts."""

from __future__ import annotations

import math
import unittest

from style_change.features import FEATURE_SCALES, StylometricProfile, extract_profile
from style_change.tokenize import sentences, words


CASUAL = (
    "I don't think we should wait. It's late, you're tired, and I'm not "
    "going to pretend this is fun. Really, we can just go home."
)
FORMAL = (
    "The committee therefore recommends that the proposal be declined. "
    "Moreover, the available measurements are insufficient to support "
    "the claimed improvement in downstream reliability."
)


class FeatureTests(unittest.TestCase):
    def test_profile_length_matches_names(self) -> None:
        profile = extract_profile(CASUAL)
        self.assertEqual(len(profile.vector()), len(StylometricProfile.names()))
        self.assertEqual(set(FEATURE_SCALES), set(StylometricProfile.names()))
        self.assertEqual(len(profile.scaled_vector()), len(profile.vector()))

    def test_all_values_finite(self) -> None:
        for text in (CASUAL, FORMAL, "Hi.", ""):
            for value in extract_profile(text).vector():
                self.assertTrue(math.isfinite(value), msg=text)

    def test_contractions_higher_in_casual(self) -> None:
        casual = extract_profile(CASUAL)
        formal = extract_profile(FORMAL)
        self.assertGreater(casual.contraction_rate, formal.contraction_rate)

    def test_connectives_higher_in_formal(self) -> None:
        casual = extract_profile(CASUAL)
        formal = extract_profile(FORMAL)
        self.assertGreater(formal.connective_rate, casual.connective_rate)

    def test_first_person_higher_in_casual(self) -> None:
        self.assertGreater(
            extract_profile(CASUAL).first_person_rate,
            extract_profile(FORMAL).first_person_rate,
        )

    def test_empty_text_does_not_crash(self) -> None:
        profile = extract_profile("")
        self.assertEqual(profile.type_token_ratio, 0.0)

    def test_sentence_split_keeps_final_fragment(self) -> None:
        self.assertGreaterEqual(len(sentences("Hello. Still going")), 2)

    def test_words_lowercases(self) -> None:
        self.assertEqual(words("Hello DON'T"), ["hello", "don't"])


if __name__ == "__main__":
    unittest.main()
