import numpy as np

from scd.features import (
    UNIT_FEATURE_NAMES,
    pairwise_feature_map,
    pairwise_feature_names,
    pairwise_features,
    unit_feature_map,
    unit_features,
    words,
)


FORMAL = "The souffle requires a precise fold of the egg whites into the batter."
CASUAL = "Yeah I'm just gonna chuck the frozen pizza in and hope for the best!"


def test_tokenizer_keeps_contractions():
    assert "I'm" in words("Yeah I'm just gonna go.")


def test_unit_vector_is_finite_and_named():
    vector = unit_features(FORMAL)
    assert vector.shape == (len(UNIT_FEATURE_NAMES),)
    assert np.isfinite(vector).all()
    mapped = unit_feature_map(FORMAL)
    assert list(mapped)[:3] == ["n_chars", "n_words", "avg_word_len"]


def test_casual_sentence_has_contractions_and_first_person():
    casual = unit_feature_map(CASUAL)
    formal = unit_feature_map(FORMAL)
    assert casual["contraction_rate"] > formal["contraction_rate"]
    assert casual["first_person_rate"] > formal["first_person_rate"]
    assert casual["exclaim"] > formal["exclaim"]


def test_empty_unit_is_zero_not_nan():
    vector = unit_features("")
    assert vector.shape == (len(UNIT_FEATURE_NAMES),)
    assert np.isfinite(vector).all()
    assert float(vector.sum()) == 0.0


def test_pairwise_dimension_matches_name_list():
    names = pairwise_feature_names()
    vector = pairwise_features(FORMAL, CASUAL)
    assert vector.shape == (len(names),)
    assert names[0].startswith("abs_")
    assert "fw_cosine" in names
    assert "jaccard" in names


def test_same_sentence_is_more_similar_than_register_flip():
    same = pairwise_feature_map(FORMAL, FORMAL)
    flipped = pairwise_feature_map(FORMAL, CASUAL)
    assert same["char_tri_cosine"] > flipped["char_tri_cosine"]
    assert same["jaccard"] > flipped["jaccard"]
    assert flipped["abs_contraction_rate"] > same["abs_contraction_rate"]
