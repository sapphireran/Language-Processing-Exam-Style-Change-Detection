import unittest

from inkfold.features import extract_register
from inkfold.handcalc import count_row, span_rates
from inkfold.lexicon import N_FUNCTION_WORDS


class FeatureTests(unittest.TestCase):
    def test_function_word_list_is_stable(self):
        # Formula card cites this length. Do not change it quietly.
        self.assertEqual(N_FUNCTION_WORDS, 108)

    def test_notice_is_formal_and_stall_is_not(self):
        stall = ["I'm telling you the kiln's too hot tonight."]
        notice = ["Vendors shall maintain a probe thermometer at the point of sale."]
        s = extract_register(stall)
        n = extract_register(notice)
        self.assertGreater(s.first_person, 0.0)
        self.assertGreater(s.contraction, 0.0)
        self.assertGreater(n.formal, 0.0)
        self.assertEqual(s.formal, 0.0)
        self.assertGreater(s.l1(n), 0.3)

    def test_handcalc_matches_register(self):
        units = ["I can't believe you shall perhaps wait."]
        rates = span_rates(units)
        reg = extract_register(units)
        self.assertAlmostEqual(rates["first_person"], reg.first_person)
        self.assertAlmostEqual(rates["second_person"], reg.second_person)
        self.assertAlmostEqual(rates["contraction"], reg.contraction)
        self.assertAlmostEqual(rates["formal"], reg.formal)
        self.assertAlmostEqual(rates["hedge"], reg.hedge)
        row = count_row(units[0])
        self.assertEqual(row["first_person"], 1)
        self.assertEqual(row["second_person"], 1)
        self.assertEqual(row["contraction"], 1)  # can't
        self.assertEqual(row["formal"], 1)  # shall
        self.assertEqual(row["hedge"], 1)  # perhaps


if __name__ == "__main__":
    unittest.main()
