import json
from pathlib import Path

from stylechange.evaluate import evaluate_changes, evaluate_dataset
from stylechange.io import Solution, iter_problems, load_problem, write_solution


def test_load_problem_attaches_sibling_truth(tmp_path: Path):
    text = tmp_path / "problem-demo.txt"
    gold = tmp_path / "truth-problem-demo.json"
    text.write_text("A.\nB.\n", encoding="utf-8")
    gold.write_text(json.dumps({"changes": [1], "authors": 2}), encoding="utf-8")
    problem = load_problem(text)
    assert problem.problem_id == "demo"
    assert problem.truth is not None
    assert problem.truth.changes == [1]
    assert problem.truth.authors == 2


def test_write_and_evaluate_roundtrip(tmp_path: Path):
    inp = tmp_path / "in"
    out = tmp_path / "out"
    inp.mkdir()
    (inp / "problem-1.txt").write_text("one.\ntwo.\nthree.\n", encoding="utf-8")
    (inp / "truth-problem-1.json").write_text(
        json.dumps({"changes": [0, 1], "authors": 2, "note": "ignored"}),
        encoding="utf-8",
    )
    write_solution(out / "solution-problem-1.json", Solution(changes=[0, 1], authors=2))
    result = evaluate_dataset(inp, out)
    assert result.macro_f1 == 1.0
    assert result.pairs == 2
    assert result.skipped == 0


def test_length_mismatch_is_skipped():
    result = evaluate_changes([[0, 1, 0]], [[0, 1]])
    assert result.skipped == 1
    assert result.documents == 0
    assert result.pairs == 0


def test_macro_f1_is_mean_of_both_classes():
    # one error: predicted change where gold is same
    result = evaluate_changes([[0, 0, 1]], [[0, 1, 1]])
    assert result.pairs == 3
    assert 0.0 < result.macro_f1 < 1.0


def test_iter_problems_sorted(tmp_path: Path):
    (tmp_path / "problem-b.txt").write_text("B.\n", encoding="utf-8")
    (tmp_path / "problem-a.txt").write_text("A.\n", encoding="utf-8")
    ids = [p.problem_id for p in iter_problems(tmp_path)]
    assert ids == ["a", "b"]
