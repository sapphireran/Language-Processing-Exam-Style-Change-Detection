"""Blank-line splitting, including wrapped paragraphs and CR leftovers."""

from __future__ import annotations

import unittest

from scarfjoint.paragraphs import split_paragraphs


class ParagraphSplitTests(unittest.TestCase):
    def test_blank_line_boundaries(self) -> None:
        text = "alpha sits here.\n\nbeta follows.\n\ngamma closes."
        self.assertEqual(split_paragraphs(text), ["alpha sits here.", "beta follows.", "gamma closes."])

    def test_wrapped_lines_join(self) -> None:
        text = "alpha sits\nhere still.\n\nbeta follows."
        self.assertEqual(split_paragraphs(text), ["alpha sits here still.", "beta follows."])

    def test_crlf(self) -> None:
        text = "alpha.\r\n\r\nbeta."
        self.assertEqual(split_paragraphs(text), ["alpha.", "beta."])

    def test_leading_trailing_blank(self) -> None:
        text = "\n\nalpha.\n\nbeta.\n\n"
        self.assertEqual(split_paragraphs(text), ["alpha.", "beta."])

    def test_empty(self) -> None:
        self.assertEqual(split_paragraphs(""), [])


if __name__ == "__main__":
    unittest.main()
