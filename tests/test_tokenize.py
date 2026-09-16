from splicefind.tokenize import (
    estimate_syllables,
    split_paragraphs,
    split_sentences,
    tokenize_words,
)


def test_split_paragraphs_skips_blank_lines():
    text = "First block.\n\n\nSecond block.\n\nThird."
    assert split_paragraphs(text) == ["First block.", "Second block.", "Third."]


def test_tokenize_keeps_contractions():
    assert tokenize_words("I don't think it's late.") == [
        "i",
        "don't",
        "think",
        "it's",
        "late",
    ]


def test_sentence_split_on_punct():
    sentences = split_sentences("One. Two? Three!")
    assert sentences == ["One.", "Two?", "Three!"]


def test_syllable_estimate_is_positive():
    assert estimate_syllables("banana") >= 2
    assert estimate_syllables("a") == 1
