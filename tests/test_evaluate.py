from pathlib import Path

import pytest

from scd.evaluate import evaluate_directory, macro_f1
from scd.io import write_problem, write_solution, write_truth


def test_worked_confusion_matrix_from_the_notes():
    # docs/05-evaluation.md: truth [0,0,1,0] vs pred [0,1,1,0]
    score = macro_f1([0, 0, 1, 0], [0, 1, 1, 0])
    assert score == pytest.approx(0.733, abs=0.005)


def test_majority_zero_is_not_a_perfect_score():
    truth = [0, 0, 0, 1]
    pred = [0, 0, 0, 0]
    assert macro_f1(truth, pred) < 0.7
    assert macro_f1(truth, truth) == pytest.approx(1.0)


def test_empty_labels_score_zero():
    assert macro_f1([], []) == 0.0


def test_directory_eval_reports_both_poolings(tmp_path: Path):
    write_problem(tmp_path / "problem-1.txt", ["A.", "B.", "C."])
    write_truth(tmp_path / "truth-problem-1.json", 2, [0, 1])
    write_solution(tmp_path / "solution-problem-1.json", [0, 1])
    write_problem(tmp_path / "problem-2.txt", ["A.", "B."])
    write_truth(tmp_path / "truth-problem-2.json", 1, [0])
    write_solution(tmp_path / "solution-problem-2.json", [0])

    scores = evaluate_directory(tmp_path, tmp_path, mode="line")
    assert scores.n_docs == 2
    assert scores.n_pairs == 3
    assert scores.macro_f1 == pytest.approx(1.0)
    # Document 2 is a single "no change" pair. Forcing both classes in
    # macro F1 gives that document 0.5 (perfect class 0, undefined class 1).
    assert scores.mean_doc_macro_f1 == pytest.approx(0.75)
