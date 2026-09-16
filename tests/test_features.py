from stylechange.distance import cosine_similarity, pair_distance, relative_difference
from stylechange.features import extract_profile
from stylechange.tokenize import char_ngrams, sentences, words


def test_words_keep_contractions_and_lower():
    assert words("I can't Even 42 times.") == ["i", "can't", "even", "42", "times"]


def test_sentences_split_on_punct():
    assert sentences("Hello there. Next? Wow!") == ["Hello there.", "Next?", "Wow!"]


def test_char_ngrams_are_letter_spaces_only():
    grams = char_ngrams("Hi, Bob", n=3)
    assert "hi " in grams or " hi" in grams
    assert all("," not in g for g in grams)


def test_casual_versus_formal_profiles_diverge():
    casual = extract_profile(
        "I can't even pretend I measured this. It's just leftover pasta and I ate it cold!"
    )
    formal = extract_profile(
        "Municipal street design is often treated as an engineering problem; "
        "the distribution of shade and seating has measurable effects on access."
    )
    assert casual.scalars["contraction_ratio"] > formal.scalars["contraction_ratio"]
    assert casual.scalars["first_person_sg_rate"] > formal.scalars["first_person_sg_rate"]
    assert formal.scalars["avg_word_len"] > casual.scalars["avg_word_len"]
    assert pair_distance(casual, formal)["combined"] > 0.35


def test_identical_text_has_near_zero_distance():
    text = "A moderate increase in volume is more reliable than a fixed number of hours."
    dist = pair_distance(extract_profile(text), extract_profile(text))
    assert dist["combined"] < 1e-9
    assert cosine_similarity({"the": 0.5, "of": 0.5}, {"the": 0.5, "of": 0.5}) == 1.0


def test_relative_difference_is_symmetric_and_bounded():
    assert relative_difference(2, 2) < 1e-9
    assert relative_difference(0, 4) == relative_difference(4, 0)
    assert 0 <= relative_difference(1, 100) <= 1
