from scdkit.tokenize import split_paragraphs, split_sentences, split_words


def test_blank_line_paragraphs() -> None:
    text = "First block.\n\nSecond block.\n\n\nThird."
    assert split_paragraphs(text) == ["First block.", "Second block.", "Third."]


def test_single_newlines_are_paragraphs_when_no_blank_lines() -> None:
    text = "Line one.\nLine two.\nLine three."
    assert len(split_paragraphs(text)) == 3


def test_words_keep_contractions() -> None:
    assert "don't" in [w.lower() for w in split_words("I don't know.")]
    assert "16" in split_words("below 16 C overnight")


def test_sentences_keep_abbreviation() -> None:
    sents = split_sentences("Dr. Jones arrived. The room was cold.")
    assert len(sents) == 2
    assert sents[0].startswith("Dr.")
