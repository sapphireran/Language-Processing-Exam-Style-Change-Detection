import json
from pathlib import Path

from quoin.evaluate import accuracy, macro_f1, micro_f1, precision_recall, safe_f1
from quoin.io import read_problem, read_solution, validate_pair, write_solution, solution_from_changes


def test_read_problem_roundtrip(tmp_path: Path):
    path = tmp_path / "problem.txt"
    path.write_text("alpha.\n\nbeta gamma.\n\ngamma.\n", encoding="utf-8")
    problem = read_problem(path)
    assert problem.n_paragraphs == 3
    assert problem.n_boundaries == 2


def test_solution_roundtrip(tmp_path: Path):
    path = tmp_path / "truth.json"
    write_solution(path, solution_from_changes([0, 1, 0]))
    solution = read_solution(path)
    assert solution.changes == [0, 1, 0]


def test_validate_pair_accepts_matching_lengths(tmp_path: Path):
    problem_path = tmp_path / "p.txt"
    problem_path.write_text("a\n\nb\n\nc\n", encoding="utf-8")
    truth_path = tmp_path / "t.json"
    truth_path.write_text(json.dumps({"changes": [0, 1], "authors": ["x", "x", "y"]}), encoding="utf-8")
    problem = read_problem(problem_path)
    solution = read_solution(truth_path)
    validate_pair(problem, solution)


def test_safe_f1_all_zero_is_perfect():
    assert safe_f1([0, 0, 0], [0, 0, 0]) == 1.0
    assert precision_recall([0, 0, 0], [0, 0, 0]) == (1.0, 1.0)


def test_safe_f1_false_positive_on_control():
    assert safe_f1([0, 0, 0], [0, 1, 0]) == 0.0


def test_safe_f1_typical_pair():
    gold = [0, 1, 0, 1]
    pred = [0, 1, 1, 1]
    assert 0.7 < safe_f1(gold, pred) < 0.9


def test_macro_and_micro_disagree_when_one_doc_is_easy():
    pairs = [([0, 0, 0], [0, 0, 0]), ([1, 1, 1], [1, 0, 0])]
    # first doc F1=1, second is weak; macro is pulled up, micro sees the misses
    assert macro_f1(pairs) > micro_f1(pairs)


def test_accuracy_of_never_fire_on_sparse_gold():
    gold = [0, 0, 0, 1]
    pred = [0, 0, 0, 0]
    assert accuracy(gold, pred) == 0.75
    assert safe_f1(gold, pred) == 0.0
