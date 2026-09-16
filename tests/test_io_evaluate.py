import json
from pathlib import Path

from stylechange.evaluate import evaluate_collection, macro_f1, pair_accuracy
from stylechange.io import iter_problems, load_json, problem_id, write_solution


def test_macro_f1_perfect_and_never_fires():
    gold = [0, 0, 1, 0]
    assert macro_f1(gold, gold) == 1.0
    # Always predicting 0: class-0 F1 is high, class-1 F1 is 0.
    never = [0, 0, 0, 0]
    score = macro_f1(gold, never)
    assert 0.3 < score < 0.9
    assert pair_accuracy(gold, never) == 0.75


def test_macro_f1_both_empty_classes():
    assert macro_f1([], []) == 1.0


def test_evaluate_writes_pan_solutions(tmp_path: Path):
    docs = Path(__file__).resolve().parents[1] / "examples" / "documents"
    score = evaluate_collection(docs, output_dir=tmp_path)
    assert score.macro_f1 == 1.0
    written = sorted(tmp_path.glob("solution-problem-*.json"))
    problems = list(iter_problems(docs))
    assert len(written) == len(problems)
    for problem in problems:
        payload = load_json(tmp_path / f"solution-problem-{problem_id(problem)}.json")
        assert "changes" in payload
        assert all(item in (0, 1) for item in payload["changes"])


def test_write_solution_shape(tmp_path: Path):
    path = tmp_path / "solution-problem-demo.json"
    write_solution(path, [0, 1, 0])
    assert json.loads(path.read_text()) == {"changes": [0, 1, 0]}
