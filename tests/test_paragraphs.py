"""Paragraph segmentation."""

from __future__ import annotations

import unittest

from style_change.paragraphs import adjacent_pairs, split_paragraphs


class SplitParagraphsTests(unittest.TestCase):
    def test_blank_line_split(self) -> None:
        text = "first block\n\nsecond block\n\nthird"
        self.assertEqual(split_paragraphs(text), ["first block", "second block", "third"])

    def test_single_newline_fallback(self) -> None:
        text = "alpha\nbeta\ngamma"
        self.assertEqual(split_paragraphs(text), ["alpha", "beta", "gamma"])

    def test_prefers_blank_lines_when_both_exist(self) -> None:
        text = "line a\nstill a\n\nline b"
        self.assertEqual(split_paragraphs(text), ["line a still a", "line b"])

    def test_skips_empty_chunks(self) -> None:
        text = "\n\nhello\n\n\n\nworld\n"
        self.assertEqual(split_paragraphs(text), ["hello", "world"])

    def test_normalizes_windows_newlines(self) -> None:
        text = "one\r\n\r\ntwo"
        self.assertEqual(split_paragraphs(text), ["one", "two"])

    def test_adjacent_pairs(self) -> None:
        pairs = adjacent_pairs(["a", "b", "c"])
        self.assertEqual(pairs, [("a", "b"), ("b", "c")])


if __name__ == "__main__":
    unittest.main()
