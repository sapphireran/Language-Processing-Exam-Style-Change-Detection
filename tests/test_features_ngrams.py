from examscd.features import FUNCTION_WORDS, function_word_l1, style_dict
from examscd.ngrams import char_ngram_distance, char_ngrams, cosine, kl_divergence


def test_function_word_list_is_closed_and_sorted_enough() -> None:
    assert "the" in FUNCTION_WORDS
    assert "tokenise" not in FUNCTION_WORDS
    assert "pasta" not in FUNCTION_WORDS
    assert FUNCTION_WORDS == tuple(sorted(set(FUNCTION_WORDS)))


def test_function_word_l1_grows_when_glue_changes() -> None:
    we = "We like this method because we can inspect the merges."
    one = "One may regard the procedure as a constrained compression of the vocabulary."
    same = "We like this method because we can inspect the merges too."
    assert function_word_l1(we, one) > function_word_l1(we, same)


def test_style_vector_marks_imperatives_and_first_person() -> None:
    recipe = "Preheat the oven. Chop two onions. Stir the pan."
    diary = "I leave the flat at seven and I still have not found gloves."
    r, d = style_dict(recipe), style_dict(diary)
    assert r["imperative_rate"] > d["imperative_rate"]
    assert d["first_person"] > r["first_person"]


def test_char_ngrams_are_lowercase_and_padded() -> None:
    grams = char_ngrams("Add", n=3)
    assert " ad" in grams
    assert "add" in grams
    assert "dd " in grams


def test_char_ngram_distance_is_small_for_near_copies() -> None:
    a = "The chair opened the meeting at 14:05 and noted that a quorum was present."
    b = "The chair opened the meeting at 14:05 and noted that a quorum was present today."
    c = "omg my laptop just died mid raid and i lost the drop lol"
    assert char_ngram_distance(a, b) < char_ngram_distance(a, c)
    assert cosine(char_ngrams(a), char_ngrams(a)) > 0.99


def test_kl_is_zero_on_identical_counters() -> None:
    grams = char_ngrams("however therefore thus", n=3)
    assert kl_divergence(grams, grams) < 1e-9
