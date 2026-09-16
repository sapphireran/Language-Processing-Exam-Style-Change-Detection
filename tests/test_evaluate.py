from seamtrace.evaluate import macro_f1, score_pairs
from seamtrace.handcalc import macro_f1_from_cells


def test_perfect() -> None:
    gold = [0, 1, 0, 1]
    assert score_pairs(gold, gold).macro_f1 == 1.0


def test_never_fire_matches_notes() -> None:
    gold = [0] * 16 + [1] * 4
    pred = [0] * 20
    metrics = score_pairs(gold, pred)
    assert abs(metrics.macro_f1 - 0.444444) < 1e-3
    assert abs(metrics.accuracy - 0.8) < 1e-9
    assert abs(metrics.macro_f1 - macro_f1_from_cells(0, 0, 16, 4)) < 1e-9


def test_length_mismatch() -> None:
    try:
        score_pairs([0], [0, 1])
    except ValueError as exc:
        assert "length" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_macro_f1_wrapper() -> None:
    assert macro_f1([1, 0], [1, 0]) == 1.0
