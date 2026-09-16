"""Keep the worked-example moral aligned with the pinned document."""

from pathlib import Path

from scd.features import unit_feature_map
from scd.generate import PINNED_EASY_PROBLEM_1_CHANGES, PINNED_EASY_PROBLEM_1_UNITS
from scd.io import read_problem, read_truth
from scd.sentences import split_units

REPO = Path(__file__).resolve().parents[1]


def test_length_gap_is_not_the_style_change():
    units = list(PINNED_EASY_PROBLEM_1_UNITS)
    changes = list(PINNED_EASY_PROBLEM_1_CHANGES)
    maps = [unit_feature_map(unit) for unit in units]
    length_pair = max(
        range(len(changes)),
        key=lambda i: abs(maps[i]["n_words"] - maps[i + 1]["n_words"]),
    )
    onset = [
        i
        for i in range(len(changes))
        if _casual(maps[i]) != _casual(maps[i + 1])
    ]
    assert changes[onset[0]] == 1
    assert changes[length_pair] == 0
    assert onset == [1]


def test_committed_file_matches_pin():
    units = split_units(
        read_problem(REPO / "examples" / "data" / "easy" / "problem-1.txt"),
        mode="line",
    )
    truth = read_truth(REPO / "examples" / "data" / "easy" / "truth-problem-1.json")
    assert units == list(PINNED_EASY_PROBLEM_1_UNITS)
    assert truth.changes == list(PINNED_EASY_PROBLEM_1_CHANGES)


def _casual(feats: dict[str, float]) -> bool:
    return feats["contraction_rate"] > 0 or feats["first_person_rate"] > 0
