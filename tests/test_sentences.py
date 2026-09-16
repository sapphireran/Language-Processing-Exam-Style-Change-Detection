from __future__ import annotations

import unittest

from stylechange.sentences import split_sentences


class SentenceSplitTests(unittest.TestCase):
    def test_line_segmented_synthetic_style(self) -> None:
        text = "First sentence stays here.\nSecond sentence follows.\nThird one ends here.\n"
        self.assertEqual(len(split_sentences(text)), 3)

    def test_running_prose_abbreviations(self) -> None:
        text = (
            "Dr. Hale recorded 15.0 g. The bloom lasted 45 s. "
            "Nell watched the kettle. I.e. nothing exploded."
        )
        sentences = split_sentences(text, prefer_lines=False)
        self.assertGreaterEqual(len(sentences), 3)
        self.assertTrue(any("Hale" in sentence for sentence in sentences))
        joined = " ".join(sentences)
        self.assertIn("15.0", joined)

    def test_empty(self) -> None:
        self.assertEqual(split_sentences(""), [])
        self.assertEqual(split_sentences("   \n"), [])

    def test_single_line_is_not_forced_to_lines(self) -> None:
        text = "Only one line lives here and it still needs a split. Here is the second."
        sentences = split_sentences(text)
        self.assertEqual(len(sentences), 2)


if __name__ == "__main__":
    unittest.main()
