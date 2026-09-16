from quoin.calibrate import best_threshold, grid_search_threshold
from quoin.features import cosine_distance, pairwise_feature_distance, vectorize
from quoin.lexicon import FUNCTION_WORDS


def test_vectorize_counts_function_words_in_stable_order():
    vec = vectorize("The of the of shall must gonna")
    assert len(vec.function) == len(FUNCTION_WORDS)
    assert vec.function[FUNCTION_WORDS.index("the")] > 0
    assert vec.shape["formal"] > 0
    assert vec.shape["informal"] > 0


def test_cosine_distance_identical_is_zero():
    vec = vectorize("one must feel the give in the tympan rather than trust the marks")
    assert cosine_distance(vec.ngrams, vec.ngrams) == 0.0


def test_pairwise_distance_grows_across_houses():
    press = vectorize(
        "I locked the forme before dawn. One must feel the give in the tympan. "
        "I have found that a hurried rule shows in the guest's hand."
    )
    notice = vectorize(
        "Members of the public are advised that operation shall be prohibited. "
        "Complaints shall be lodged. Permits shall be produced without delay."
    )
    near = pairwise_feature_distance(press, press)
    far = pairwise_feature_distance(press, notice)
    assert far["function_l1"] > near["function_l1"]
    assert far["char_cosine"] > near["char_cosine"]


def test_grid_search_picks_a_separating_threshold():
    documents = [
        ([0, 1, 0], [0.10, 0.50, 0.12]),
        ([0, 0, 0], [0.11, 0.09, 0.13]),
        ([1, 1], [0.55, 0.60]),
    ]
    rows = grid_search_threshold(documents, start=0.20, stop=0.40, step=0.10)
    winner = best_threshold(rows)
    assert 0.20 <= winner.threshold <= 0.40
    assert winner.macro_f1 >= 0.9
