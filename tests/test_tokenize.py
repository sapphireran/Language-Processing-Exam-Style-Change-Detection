import unittest

from inkfold.tokenize import char_ngrams, units_from_text, word_tokens


class TokenizeTests(unittest.TestCase):
    def test_line_units_win(self):
        text = "First line.\nSecond line!\n\nThird.\n"
        self.assertEqual(units_from_text(text), ["First line.", "Second line!", "Third."])

    def test_single_paragraph_falls_back(self):
        text = "One sentence. Two sentences? Three!"
        self.assertEqual(units_from_text(text), ["One sentence.", "Two sentences?", "Three!"])

    def test_contraction_stays_one_token(self):
        self.assertEqual(word_tokens("I'm not sure she'll go."), ["i'm", "not", "sure", "she'll", "go"])

    def test_char_trigrams_keep_spaces(self):
        grams = char_ngrams("Ab C", 3)
        self.assertIn("ab ", grams)
        self.assertIn("b c", grams)


if __name__ == "__main__":
    unittest.main()
