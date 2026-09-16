import json
from pathlib import Path

from stylechange.io import load_problem, load_split, load_truth, write_solution


def test_round_trip_problem_and_truth(tmp_path: Path):
    problem_path = tmp_path / "problem-007.txt"
    problem_path.write_text("Alpha paragraph.\n\nBeta paragraph.\n", encoding="utf-8", newline="")
    truth_path = tmp_path / "truth-problem-007.json"
    truth_path.write_text(json.dumps({"authors": 2, "changes": [1]}), encoding="utf-8")

    problem = load_problem(problem_path)
    truth = load_truth(truth_path)
    assert problem.problem_id == "007"
    assert problem.paragraphs == ["Alpha paragraph.", "Beta paragraph."]
    assert truth.authors == 2
    assert truth.changes == [1]

    dest = tmp_path / "out" / "solution-problem-007.json"
    write_solution(dest, [1])
    assert json.loads(dest.read_text(encoding="utf-8")) == {"changes": [1]}


def test_load_split_pairs_optional_truth(tmp_path: Path):
    (tmp_path / "problem-001.txt").write_text("One.\n\nTwo.\n", encoding="utf-8")
    (tmp_path / "problem-002.txt").write_text("Only.\n", encoding="utf-8")
    (tmp_path / "truth-problem-001.json").write_text(
        json.dumps({"authors": 1, "changes": [0]}), encoding="utf-8"
    )
    rows = load_split(tmp_path)
    assert [p.problem_id for p, _ in rows] == ["001", "002"]
    assert rows[0][1] is not None
    assert rows[1][1] is None
