from scdkit.evaluate import (
    authors_from_changes,
    binary_scores,
    gold_from_authors,
    macro_f1,
)


def test_mixed_error_f1() -> None:
    score = binary_scores([1, 0, 1], [1, 1, 0])
    assert score.tp == 1 and score.fp == 1 and score.fn == 1
    assert score.precision == 0.5
    assert score.recall == 0.5
    assert score.f1 == 0.5


def test_all_zero_convention() -> None:
    score = binary_scores([0, 0, 0], [0, 0, 0])
    assert score.f1 == 1.0
    assert score.precision == 1.0


def test_missed_change_is_zero() -> None:
    score = binary_scores([1, 0, 1], [0, 0, 0])
    assert score.recall == 0.0
    assert score.f1 == 0.0


def test_macro_averages_documents() -> None:
    value = macro_f1([([0, 0], [0, 0]), ([1], [0])])
    assert value == 0.5


def test_author_roundtrip_without_return() -> None:
    authors = [1, 1, 2, 2, 3]
    changes = gold_from_authors(authors)
    assert changes == [0, 1, 0, 1]
    assert authors_from_changes(changes) == authors
