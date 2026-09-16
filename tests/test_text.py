from isogloss.text import split_units, words


def test_blank_line_units() -> None:
    text = "First block.\n\nSecond block.\n\nThird."
    assert split_units(text) == ["First block.", "Second block.", "Third."]


def test_sentence_fallback() -> None:
    text = "One sentence. Two sentence. Three."
    assert len(split_units(text)) == 3


def test_words_keep_contractions() -> None:
    assert "don't" in [w.lower() for w in words("I don't mind.")]
    assert "12" in words("Wind 12 kn")
