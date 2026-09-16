"""Smoke the detector on files I can defend without looking at holdout."""

from isogloss.detect import detect_problem
from isogloss.evaluate import macro_f1, never_fire
from isogloss.io import iter_problems, read_problem


def test_control_01_quiet() -> None:
    problem = read_problem("examples/corpus/problem-01-skiff-eel-control.txt")
    assert detect_problem(problem).changes == [0, 0, 0]


def test_easy_07_fires_the_join() -> None:
    problem = read_problem("examples/corpus/problem-07-skiff-eel-then-roll-hop.txt")
    pred = detect_problem(problem).changes
    assert pred[1] == 1


def test_trap_25_quiet() -> None:
    problem = read_problem("examples/corpus/problem-25-skiff-eel-then-skiff-hop.txt")
    assert sum(detect_problem(problem).changes) == 0


def test_beats_never_fire_on_non_holdout() -> None:
    holdout = {"4", "04", "10", "16", "22", "26", "30"}
    gold: list[int] = []
    pred: list[int] = []
    for problem in iter_problems("examples/corpus"):
        if problem.ident.lstrip("0") in {h.lstrip("0") for h in holdout}:
            continue
        if problem.gold is None:
            continue
        gold.extend(problem.gold)
        pred.extend(detect_problem(problem).changes)
    assert gold
    assert macro_f1(gold, pred) > macro_f1(gold, never_fire(len(gold)))
