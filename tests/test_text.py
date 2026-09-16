from kerf.text import contraction_count, split_paragraphs, split_sentences, words


def test_blank_line_paragraphs() -> None:
    text = "One para.\n\nTwo para.\n\n\nThree para."
    assert split_paragraphs(text) == ["One para.", "Two para.", "Three para."]


def test_sentences_keep_abbreviation() -> None:
    sents = split_sentences("See Fig. 2 in the annex. Then stop.")
    assert len(sents) == 2
    assert sents[0].startswith("See Fig.")


def test_possessive_is_not_a_contraction() -> None:
    assert contraction_count("The observer's book was filed.") == 0
    assert contraction_count("It's probably fine. Don't ask.") == 2


def test_words_keep_digits() -> None:
    assert "0.86" in words("The staff read 0.86 metres.")
