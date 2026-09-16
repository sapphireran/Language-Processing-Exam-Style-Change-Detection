from pathlib import Path

from scd.generate import (
    DEFAULT_SEED,
    DOCS_PER_BAND,
    PINNED_EASY_PROBLEM_1_CHANGES,
    PINNED_EASY_PROBLEM_1_UNITS,
    write_corpus,
)
from scd.io import read_problem, read_truth
from scd.sentences import split_units


def test_pinned_easy_problem_is_stable(tmp_path: Path):
    write_corpus(tmp_path, seed=DEFAULT_SEED)
    units = split_units(read_problem(tmp_path / "easy" / "problem-1.txt"), mode="line")
    truth = read_truth(tmp_path / "easy" / "truth-problem-1.json")
    assert units == list(PINNED_EASY_PROBLEM_1_UNITS)
    assert truth.changes == list(PINNED_EASY_PROBLEM_1_CHANGES)
    assert truth.authors == 2


def test_each_band_has_the_promised_count_and_aligned_labels(tmp_path: Path):
    write_corpus(tmp_path, seed=DEFAULT_SEED)
    for band in ("easy", "medium", "hard"):
        problems = sorted((tmp_path / band).glob("problem-*.txt"))
        assert len(problems) == DOCS_PER_BAND
        for problem in problems:
            units = split_units(read_problem(problem), mode="line")
            pid = problem.name.removeprefix("problem-").removesuffix(".txt")
            truth = read_truth(tmp_path / band / f"truth-problem-{pid}.json")
            assert len(truth.changes) == len(units) - 1
            assert all(unit.strip() for unit in units)


def test_same_seed_is_byte_identical(tmp_path: Path):
    first = tmp_path / "a"
    second = tmp_path / "b"
    write_corpus(first, seed=DEFAULT_SEED)
    write_corpus(second, seed=DEFAULT_SEED)
    for band in ("easy", "medium", "hard"):
        for name in ("problem-3.txt", "truth-problem-3.json"):
            left = (first / band / name).read_bytes()
            right = (second / band / name).read_bytes()
            assert left == right
