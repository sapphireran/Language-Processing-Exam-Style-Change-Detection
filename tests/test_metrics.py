import pytest

from kerf.metrics import hinge_macro_f1


def test_perfect() -> None:
    s = hinge_macro_f1([0, 1, 0], [0, 1, 0])
    assert s.macro_f1 == 1.0
    assert s.accuracy == 1.0


def test_never_fire_on_imbalance() -> None:
    gold = [0, 0, 0, 1]
    s = hinge_macro_f1([0, 0, 0, 0], gold)
    assert s.accuracy == 0.75
    assert s.f1_change == 0.0
    assert s.macro_f1 < 0.6


def test_length_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        hinge_macro_f1([0, 1], [0, 1, 0])
