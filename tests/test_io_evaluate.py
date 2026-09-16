import json
from pathlib import Path

from splicefind.evaluate import score_document
from splicefind.io import load_collection, load_truth, write_solution, write_truth
from splicefind.io import Truth


def test_score_perfect_and_empty():
    gold = [0, 1, 0, 1]
    perfect = score_document(gold, gold, "demo")
    assert perfect.f1 == 1.0
    assert perfect.accuracy == 1.0
    never = score_document(gold, [0, 0, 0, 0], "demo")
    assert never.recall == 0.0
    assert never.true_negatives == 2


def test_pan_roundtrip(tmp_path: Path):
    problem = tmp_path / "problem-7.txt"
    problem.write_text("Alpha paragraph.\n\nBeta paragraph.\n\nGamma.\n", encoding="utf-8")
    truth = Truth(problem_id="7", changes=[1, 0], authors=2, difficulty="easy", title="toy")
    write_truth(tmp_path / "truth-problem-7.json", truth)
    write_solution(tmp_path / "solution-problem-7.json", [1, 0])
    collection = load_collection(tmp_path)
    assert len(collection) == 1
    problem_obj, loaded = next(collection.pairs())
    assert problem_obj.n_boundaries == 2
    assert loaded is not None
    assert loaded.changes == [1, 0]
    payload = json.loads((tmp_path / "solution-problem-7.json").read_text(encoding="utf-8"))
    assert payload == {"changes": [1, 0]}
    assert load_truth(tmp_path / "truth-problem-7.json").title == "toy"
