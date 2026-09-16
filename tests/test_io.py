from pathlib import Path

import pytest

from scd.io import (
    FormatError,
    check_alignment,
    list_problems,
    problem_id,
    read_solution,
    read_truth,
    reconstruct_authors,
    write_problem,
    write_solution,
    write_truth,
)


def test_problem_id_accepts_all_three_shapes():
    assert problem_id("problem-12.txt") == "12"
    assert problem_id("truth-problem-12.json") == "12"
    assert problem_id(Path("/tmp/solution-problem-12.json")) == "12"


def test_problem_id_rejects_noise():
    with pytest.raises(FormatError):
        problem_id("readme.txt")


def test_truth_consistency_rules(tmp_path: Path):
    path = tmp_path / "truth-problem-1.json"
    write_truth(path, 2, [0, 1, 0])
    truth = read_truth(path)
    assert truth.authors == 2
    assert truth.changes == [0, 1, 0]

    with pytest.raises(FormatError):
        write_truth(path, 1, [0, 1])
    with pytest.raises(FormatError):
        write_truth(path, 3, [0, 0, 0])


def test_solution_roundtrip(tmp_path: Path):
    path = tmp_path / "solution-problem-7.json"
    write_solution(path, [0, 1, 1, 0])
    assert read_solution(path) == [0, 1, 1, 0]


def test_alignment_off_by_one():
    check_alignment(4, [0, 1, 0], path="x")
    with pytest.raises(FormatError):
        check_alignment(4, [0, 1, 0, 0], path="x")
    with pytest.raises(FormatError):
        check_alignment(1, [0], path="x")


def test_reconstruct_authors_increments_only_on_changes():
    assert reconstruct_authors([0, 0, 1, 0, 1]) == [1, 1, 1, 2, 2, 3]


def test_list_problems_is_sorted(tmp_path: Path):
    write_problem(tmp_path / "problem-2.txt", ["One.", "Two."])
    write_problem(tmp_path / "problem-10.txt", ["One."])
    write_problem(tmp_path / "problem-1.txt", ["One."])
    names = [path.name for path in list_problems(tmp_path)]
    assert names == ["problem-1.txt", "problem-10.txt", "problem-2.txt"]
