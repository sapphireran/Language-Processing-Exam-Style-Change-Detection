"""The notes quote easy/problem-1. Keep the committed corpus in lockstep."""

from pathlib import Path

from scd.generate import DEFAULT_SEED, PINNED_EASY_PROBLEM_1_UNITS, write_corpus
from scd.io import read_problem
from scd.sentences import split_units

REPO = Path(__file__).resolve().parents[1]
COMMITTED = REPO / "examples" / "data"


def test_committed_easy_problem_1_is_the_worked_example():
    units = split_units(read_problem(COMMITTED / "easy" / "problem-1.txt"), mode="line")
    assert units == list(PINNED_EASY_PROBLEM_1_UNITS)


def test_committed_corpus_matches_generator(tmp_path: Path):
    write_corpus(tmp_path, seed=DEFAULT_SEED)
    for band in ("easy", "medium", "hard"):
        generated = sorted((tmp_path / band).iterdir())
        committed = sorted((COMMITTED / band).iterdir())
        assert [path.name for path in generated] == [path.name for path in committed]
        for left, right in zip(generated, committed):
            assert left.read_bytes() == right.read_bytes(), left.name
