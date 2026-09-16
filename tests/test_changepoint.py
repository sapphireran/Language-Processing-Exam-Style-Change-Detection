from kerf.changepoint import adjacent_absolute, binary_segment, split_scores
from kerf.features import FeatureVector, SAW_WEIGHTS


def _fake(**rates: float) -> FeatureVector:
    filled = {name: 0.0 for name, _ in SAW_WEIGHTS}
    filled.update(rates)
    return FeatureVector(rates=filled, n_words=50, n_sentences=3)


def test_balanced_cut_wins_on_aabb() -> None:
    a = _fake(first_person=0.1)
    b = _fake(second_person=0.1)
    scores = split_scores([a, a, b, b])
    assert scores[1] == max(scores)


def test_quiet_walk_does_not_cut() -> None:
    a = _fake(first_person=0.08)
    cuts = binary_segment([a, a, a, a], penalty=0.22)
    assert cuts == []


def test_adjacent_floor_ignores_quiet_steps() -> None:
    a = _fake(first_person=0.08)
    b = _fake(first_person=0.09)
    assert adjacent_absolute([a, b, a], floor=0.40) == []
