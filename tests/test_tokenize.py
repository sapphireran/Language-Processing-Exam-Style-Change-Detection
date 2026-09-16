from style_change.tokenize import split_paragraphs, split_sentences, tokenize_words


def test_blank_line_paragraphs() -> None:
    doc = split_paragraphs("First block.\n\nSecond block.\n\nThird block.")
    assert [p.text for p in doc.paragraphs] == ["First block.", "Second block.", "Third block."]


def test_one_paragraph_per_line_without_blank_lines() -> None:
    doc = split_paragraphs("Alpha sits here.\nBeta sits there.\nGamma sits too.")
    assert len(doc.paragraphs) == 3
    assert doc.paragraphs[1].text == "Beta sits there."


def test_blank_lines_win_over_single_newlines() -> None:
    text = "Line one.\nStill paragraph one.\n\nParagraph two."
    doc = split_paragraphs(text)
    assert len(doc.paragraphs) == 2
    assert "Still paragraph one." in doc.paragraphs[0].text


def test_empty_and_whitespace_only() -> None:
    assert len(split_paragraphs("").paragraphs) == 0
    assert len(split_paragraphs("   \n\n  ").paragraphs) == 0


def test_sentence_and_word_boundaries() -> None:
    sentences = split_sentences('He arrived. "Did you wait?" I had not.')
    assert len(sentences) == 3
    words = tokenize_words("Don't collapse I'll, please.")
    assert words == ("Don't", "collapse", "I'll", "please")
