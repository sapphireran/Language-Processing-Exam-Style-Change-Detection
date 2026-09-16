import json
from pathlib import Path

from kerf.io import paired_files, read_problem, read_truth, write_prediction


def test_roundtrip_prediction(tmp_path: Path) -> None:
    out = tmp_path / "pred.json"
    write_prediction(out, [0, 1, 0], authors=2)
    raw = json.loads(out.read_text())
    assert raw == {"changes": [0, 1, 0], "authors": 2}


def test_corpus_pairs_exist() -> None:
    pairs = paired_files("examples/corpus")
    assert len(pairs) == 28
    problem, truth = pairs[0]
    p = read_problem(problem)
    t = read_truth(truth)
    assert p.n_hinges == len(t.changes)
    assert p.n_hinges == len(p.paragraphs) - 1
