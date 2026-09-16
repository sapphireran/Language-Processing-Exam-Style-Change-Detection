from __future__ import annotations

import unittest

from hingemark.delta import adjacent_delta
from hingemark.detectors import adaptive_detect, never_change, threshold_detect
from hingemark.evaluate import accuracy_trap, score_pairs
from hingemark.features import extract
from hingemark.handcalc import trap_numbers, type_token_ratio
from hingemark.ngrams import char_ngrams, cosine_distance
from hingemark.pairwise import score_unit_hinges
from hingemark.tokenize import split_sentences, split_units, word_tokens


class TokenizeTests(unittest.TestCase):
    def test_lines_skip_blanks(self) -> None:
        text = "One sentence.\n\nTwo sentence.\n"
        self.assertEqual(split_units(text, "lines"), ["One sentence.", "Two sentence."])

    def test_paragraphs(self) -> None:
        text = "First block.\nStill first.\n\nSecond block."
        units = split_units(text, "paragraphs")
        self.assertEqual(len(units), 2)
        self.assertIn("Still first.", units[0])

    def test_sentences_keep_abbrev(self) -> None:
        text = "Dr. Vale noted the pulse. The next hour was quiet."
        units = split_sentences(text)
        self.assertEqual(len(units), 2)
        self.assertTrue(units[0].startswith("Dr."))

    def test_word_tokens_contraction(self) -> None:
        self.assertIn("don't", word_tokens("I don't mind."))


class FeatureTests(unittest.TestCase):
    def test_person_flags(self) -> None:
        river = extract("I walked the towpath and I counted the gates.")
        spark = extract("you should've seen it! we're gonna be late.")
        quill = extract("It was subsequently noted that the proposal had been deferred.")
        self.assertGreater(river.i_rate, 0.2)
        self.assertGreater(spark.you_rate, 0.0)
        self.assertGreater(spark.contraction_rate, 0.0)
        self.assertGreater(quill.hedge_rate + quill.passive_rate, 0.1)
        self.assertEqual(quill.i_rate, 0.0)

    def test_function_vector_length(self) -> None:
        feat = extract("The lock was opened and the barge moved through.")
        self.assertEqual(len(feat.function_vector()), len(feat.function_counts))
        self.assertGreater(sum(feat.function_vector()), 0)


class PairwiseTests(unittest.TestCase):
    def test_register_gap_fires_on_easy_pair(self) -> None:
        units = [
            "I walked the towpath and I counted eight gates before noon.",
            "I sat on the coping stone and ate the last plum.",
            "Lot 14: oak lock-gate leaf, 3.2 m by 0.48 m; iron strap hinges, c. 1891.",
            "The object retains original pintles; surface salt 12 g/kg.",
        ]
        hinges = score_unit_hinges(units)
        self.assertEqual(len(hinges), 3)
        # The voice change is hinge 1 (index 1).
        self.assertGreater(hinges[1].blend, hinges[0].blend)
        self.assertGreater(hinges[1].register_gap, hinges[0].register_gap)

    def test_threshold_can_cut_the_loud_hinge(self) -> None:
        units = [
            "I walked the towpath and I counted eight gates before noon.",
            "Lot 14: oak lock-gate leaf, 3.2 m by 0.48 m; iron strap hinges, c. 1891.",
        ]
        hinges = score_unit_hinges(units)
        result = threshold_detect(hinges, threshold=0.18)
        self.assertEqual(result.changes, (1,))

    def test_never_change_is_all_zeros(self) -> None:
        hinges = score_unit_hinges(["Alpha sentence here.", "Beta sentence there."])
        self.assertTrue(all(c == 0 for c in never_change(hinges).changes))

    def test_adaptive_quiet_on_flat_control(self) -> None:
        units = [
            "I checked the greenhouse vents and I wrote the humidity down.",
            "I turned the quince jars and I wiped the shelf.",
            "I caught the night bus and I counted the bridges.",
        ]
        hinges = score_unit_hinges(units)
        result = adaptive_detect(hinges)
        self.assertEqual(sum(result.changes), 0)


class MetricTests(unittest.TestCase):
    def test_accuracy_trap(self) -> None:
        trap = accuracy_trap()
        self.assertAlmostEqual(trap.accuracy, 0.8)
        self.assertAlmostEqual(trap.macro_f1, 0.4444444444, places=6)
        nums = trap_numbers()
        self.assertEqual(nums["tn"], 16)
        self.assertEqual(nums["fn"], 4)
        self.assertEqual(nums["tp"], 0)
        self.assertAlmostEqual(nums["hold_f1"], 2 * 0.8 * 1 / 1.8)

    def test_perfect_pairs(self) -> None:
        report = score_pairs([0, 1, 0], [0, 1, 0])
        self.assertEqual(report.accuracy, 1.0)
        self.assertEqual(report.macro_f1, 1.0)

    def test_length_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            score_pairs([0, 1], [0])


class SupportTests(unittest.TestCase):
    def test_ttr(self) -> None:
        self.assertEqual(type_token_ratio(["the", "cat", "the"]), 2 / 3)

    def test_char_ngrams(self) -> None:
        a = char_ngrams("lock gate oak")
        b = char_ngrams("lock gate pine")
        c = char_ngrams("yeah we're late lol")
        self.assertLess(cosine_distance(a, b), cosine_distance(a, c))

    def test_delta_runs(self) -> None:
        from hingemark.features import extract_many

        feats = extract_many(
            [
                "I walked the path and I sat down.",
                "The committee subsequently deferred the proposal.",
            ]
        )
        deltas = adjacent_delta(feats)
        self.assertEqual(len(deltas), 1)
        self.assertGreater(deltas[0], 0)


if __name__ == "__main__":
    unittest.main()
