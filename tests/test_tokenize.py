from examscd.tokenize import split_paragraphs, split_sentences, split_units


def test_line_sentences_win_over_wrapped_prose() -> None:
    text = "Preheat the oven to 180 C.\nChop two yellow onions.\nWarm a thin film of oil in the pan.\n"
    assert split_sentences(text) == [
        "Preheat the oven to 180 C.",
        "Chop two yellow onions.",
        "Warm a thin film of oil in the pan.",
    ]


def test_regex_fallback_on_wrapped_prose() -> None:
    text = "The chair opened the meeting. Apologies were recorded. The minutes were approved."
    assert split_sentences(text) == [
        "The chair opened the meeting.",
        "Apologies were recorded.",
        "The minutes were approved.",
    ]


def test_paragraphs_split_on_blank_lines() -> None:
    text = "First block.\nStill first.\n\nSecond block.\n"
    assert split_paragraphs(text) == ["First block.\nStill first.", "Second block."]


def test_split_units_rejects_unknown_grain() -> None:
    try:
        split_units("Hello.", "chapter")
    except ValueError as exc:
        assert "unknown granularity" in str(exc)
    else:
        raise AssertionError("expected ValueError")
