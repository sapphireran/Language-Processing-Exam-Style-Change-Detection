from stylechange.tokenize import segment, split_paragraphs, split_sentences


def test_one_sentence_per_line():
    text = "Hello there, this is a full sentence.\nA second sentence follows it.\nNotes: S -> NP\n"
    assert segment(text) == [
        "Hello there, this is a full sentence.",
        "A second sentence follows it.",
        "Notes: S -> NP",
    ]


def test_blank_lines_select_paragraphs_in_auto():
    text = "First paragraph with two sentences. Still the same block.\n\nSecond paragraph is alone.\n"
    units = segment(text, "auto")
    assert len(units) == 2
    assert units[0].startswith("First paragraph")
    assert units[1].startswith("Second paragraph")


def test_explicit_sentence_splits_wrapped_prose():
    text = "The cat sat on the mat. The dog sat on the log."
    assert split_sentences(text) == [
        "The cat sat on the mat.",
        "The dog sat on the log.",
    ]


def test_paragraph_split_strips_chunks():
    assert split_paragraphs("A\n\n\nB\n") == ["A", "B"]
