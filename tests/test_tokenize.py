from stylechange.tokenize import split_paragraphs, split_sentences, split_units


def test_abbreviation_does_not_split():
    text = "We use e.g. add-one smoothing. We then report perplexity."
    assert split_sentences(text) == [
        "We use e.g. add-one smoothing.",
        "We then report perplexity.",
    ]


def test_initials_and_question():
    text = "Dr. Lee asked: is this a DP? Prof. Ng disagreed."
    sentences = split_sentences(text)
    assert len(sentences) == 2
    assert sentences[0].endswith("DP?")


def test_line_segmented_file():
    text = "First sentence.\nSecond sentence!\nThird sentence?"
    assert split_sentences(text) == [
        "First sentence.",
        "Second sentence!",
        "Third sentence?",
    ]


def test_paragraphs_need_a_blank_line():
    text = "Paragraph one stays together\neven with a wrap.\n\nParagraph two is new."
    assert split_paragraphs(text) == [
        "Paragraph one stays together even with a wrap.",
        "Paragraph two is new.",
    ]


def test_split_units_dispatches():
    text = "A.\nB.\n\nC.\nD."
    assert len(split_units(text, "sentence")) == 4
    assert len(split_units(text, "paragraph")) == 2
