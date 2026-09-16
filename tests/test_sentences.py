from scd.sentences import split_paragraphs, split_sentences, split_units


def test_line_mode_skips_blank_lines():
    text = "First unit.\n\nSecond unit.\n"
    assert split_units(text, mode="line") == ["First unit.", "Second unit."]


def test_sentence_mode_splits_on_boundaries():
    text = "Hello there. Is this two? Yes!"
    assert split_sentences(text) == ["Hello there.", "Is this two?", "Yes!"]


def test_paragraph_mode_joins_wrapped_lines():
    text = "Line one\nstill the same.\n\nNext block."
    assert split_paragraphs(text) == ["Line one still the same.", "Next block."]


def test_windows_newlines_do_not_create_ghost_units():
    text = "Alpha.\r\nBeta.\r\n"
    assert split_units(text, mode="line") == ["Alpha.", "Beta."]
