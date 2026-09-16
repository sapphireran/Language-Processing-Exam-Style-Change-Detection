from quoin.tokenize import paragraphs, sentence_lengths, sentences, word_count, words


def test_paragraphs_split_on_blank_lines():
    text = "one\n\ntwo\n\n\nthree\n"
    assert paragraphs(text) == ["one", "two", "three"]


def test_paragraphs_ignore_wrapped_lines_inside_a_block():
    text = "line a\nline b\n\nsecond"
    assert paragraphs(text) == ["line a\nline b", "second"]


def test_words_keep_contractions_and_fold_case():
    assert words("I don't Think so") == ["i", "don't", "think", "so"]


def test_sentence_split_and_lengths():
    text = "One two three. Four five! Six?"
    assert sentences(text) == ["One two three.", "Four five!", "Six?"]
    assert sentence_lengths(text) == [3, 2, 1]
    assert word_count(text) == 6
