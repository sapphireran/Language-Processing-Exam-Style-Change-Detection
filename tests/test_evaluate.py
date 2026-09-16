import pytest

from stylechange.evaluate import score_changes, score_corpus


def test_perfect_and_all_negative_conventions():
    perfect = score_changes([0, 1, 0], [0, 1, 0])
    assert perfect.f1 == 1.0
    assert perfect.accuracy == 1.0

    all_neg = score_changes([0, 0, 0], [0, 0, 0])
    assert all_neg.precision == 1.0
    assert all_neg.recall == 1.0
    assert all_neg.f1 == 1.0


def test_false_positives_crush_precision():
    score = score_changes([0, 0, 0], [1, 1, 1])
    assert score.precision == 0.0
    assert score.recall == 1.0
    assert score.f1 == 0.0


def test_constant_zero_looks_accurate_but_misses_changes():
    score = score_changes([0, 0, 1, 0, 0], [0, 0, 0, 0, 0])
    assert score.accuracy == 0.8
    assert score.recall == 0.0
    assert score.f1 == 0.0


def test_length_mismatch_and_bad_labels():
    with pytest.raises(ValueError, match="length mismatch"):
        score_changes([0, 1], [0])
    with pytest.raises(ValueError, match="labels must be 0 or 1"):
        score_changes([0, 2], [0, 1])


def test_corpus_macro_and_micro():
    summary = score_corpus(
        [
            ("a", [1, 0], [1, 0]),
            ("b", [1, 1], [0, 0]),
        ]
    )
    assert summary["per_document"]["a"].f1 == 1.0
    assert summary["per_document"]["b"].f1 == 0.0
    assert summary["macro_f1"] == 0.5
    assert summary["micro"].true_positives == 1
    assert summary["micro"].false_negatives == 2
