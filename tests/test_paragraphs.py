from stylechange.paragraphs import pair_boundaries, split_paragraphs


def test_split_blank_lines_and_wrap():
    text = "First line\ncontinued here.\n\nSecond paragraph.\n\n\nThird.\n"
    assert split_paragraphs(text) == [
        "First line continued here.",
        "Second paragraph.",
        "Third.",
    ]


def test_crlf_and_empty_document():
    assert split_paragraphs("") == []
    assert split_paragraphs("A\r\n\r\nB\r\n") == ["A", "B"]


def test_pair_boundaries():
    assert pair_boundaries(["a", "b", "c"]) == [("a", "b"), ("b", "c")]
    assert pair_boundaries(["only"]) == []
