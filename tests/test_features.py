from __future__ import annotations

import unittest

from stylechange.features import FEATURE_NAMES, as_dict, extract_document, extract_sentence


class FeatureTests(unittest.TestCase):
    def test_dimension_and_determinism(self) -> None:
        text = "However, I don't think 15.0 g is relatively decisive!"
        first = extract_sentence(text)
        second = extract_sentence(text)
        self.assertEqual(first.shape, (len(FEATURE_NAMES),))
        self.assertTrue((first == second).all())

    def test_jules_tells(self) -> None:
        vector = as_dict(extract_sentence("I don't wait that long; I just go for it!"))
        self.assertGreater(vector["contraction_rate"], 0.0)
        self.assertGreater(vector["first_person_rate"], 0.0)
        self.assertGreater(vector["exclamation_rate"], 0.0)

    def test_apostrophe_s_counts_as_contraction(self) -> None:
        vector = as_dict(extract_sentence("That's the water's fault and I'm late."))
        self.assertGreaterEqual(vector["contraction_rate"], 2 / 7)

    def test_mira_tells(self) -> None:
        vector = as_dict(
            extract_sentence(
                "However, the bloom remains relatively unstable although the pour is slow."
            )
        )
        self.assertGreater(vector["hedge_rate"], 0.0)
        self.assertEqual(vector["contraction_rate"], 0.0)
        self.assertEqual(vector["first_person_rate"], 0.0)

    def test_hale_digits(self) -> None:
        vector = as_dict(extract_sentence("Water mass was 15.0 g and bloom time was 45 s."))
        self.assertGreater(vector["digit_rate"], 0.0)

    def test_nell_semicolon(self) -> None:
        vector = as_dict(
            extract_sentence("The kettle ticked; the filter breathed a faint paper sweetness.")
        )
        self.assertGreater(vector["semicolon_rate"], 0.0)
        self.assertEqual(vector["digit_rate"], 0.0)

    def test_document_stack(self) -> None:
        matrix = extract_document(["Short one.", "A somewhat longer academic sentence appears here."])
        self.assertEqual(matrix.shape, (2, len(FEATURE_NAMES)))

    def test_empty_sentence(self) -> None:
        vector = extract_sentence("")
        self.assertEqual(vector.shape, (len(FEATURE_NAMES),))
        self.assertEqual(float(vector[FEATURE_NAMES.index("word_count")]), 0.0)


if __name__ == "__main__":
    unittest.main()
