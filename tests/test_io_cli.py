import json
from pathlib import Path

from isogloss.cli import main
from isogloss.io import iter_problems, read_problem, write_solution


def test_corpus_loads() -> None:
    problems = list(iter_problems("examples/corpus"))
    assert len(problems) == 30
    for problem in problems:
        assert problem.gold is not None
        assert len(problem.gold) == problem.n_hinges
        assert problem.n_units >= 2


def test_write_solution(tmp_path: Path) -> None:
    path = tmp_path / "solution-problem-1.json"
    write_solution(path, [0, 1, 0])
    payload = json.loads(path.read_text())
    assert payload == {"changes": [0, 1, 0]}


def test_read_extra_keys_ignored_by_gold() -> None:
    problem = read_problem("examples/corpus/problem-01-skiff-eel-control.txt")
    assert problem.truth is not None
    assert "houses" in problem.truth
    assert problem.gold == [0, 0, 0]


def test_cli_inspect() -> None:
    assert (
        main(["inspect", "examples/corpus/problem-19-skiff-then-vellum-eel.txt"]) == 0
    )


def test_cli_predict(tmp_path: Path) -> None:
    assert main(["predict", "-i", "examples/corpus", "-o", str(tmp_path)]) == 0
    assert len(list(tmp_path.glob("solution-problem-*.json"))) == 30
