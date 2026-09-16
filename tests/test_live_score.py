from isogloss.detect import detect_problem
from isogloss.evaluate import macro_f1
from isogloss.io import iter_problems


def test_bank_is_clean() -> None:
    gold: list[int] = []
    pred: list[int] = []
    for problem in iter_problems("examples/corpus"):
        assert problem.gold is not None
        gold.extend(problem.gold)
        pred.extend(detect_problem(problem).changes)
    assert gold.count(1) == 23
    assert macro_f1(gold, pred) == 1.0


def test_holdout_is_clean() -> None:
    keep = {"4", "10", "16", "22", "26", "30"}
    gold: list[int] = []
    pred: list[int] = []
    for problem in iter_problems("examples/corpus"):
        if (problem.ident.lstrip("0") or "0") not in keep:
            continue
        assert problem.gold is not None
        gold.extend(problem.gold)
        pred.extend(detect_problem(problem).changes)
    assert gold
    assert pred == gold
