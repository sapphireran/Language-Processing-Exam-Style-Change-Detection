from seamtrace.tokenize import char_ngrams, sentences_from_prose, words


def test_words_keep_internal_apostrophes() -> None:
    assert words("Don't say it's easy.") == ["don't", "say", "it's", "easy"]


def test_abbrev_does_not_split_dr() -> None:
    parts = sentences_from_prose("I met Dr. Hansen yesterday. He waved.")
    assert parts == ["I met Dr. Hansen yesterday.", "He waved."]


def test_trigrams_squeeze_space() -> None:
    grams = char_ngrams("Hi  there", 3)
    assert "hi " in grams or "i t" in grams
    assert all(len(g) == 3 for g in grams)
