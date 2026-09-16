import json

from scdkit.io import dump_truth, load_document, load_truth, pair_problems
from scdkit.tokenize import split_paragraphs


def test_truth_roundtrip(tmp_path) -> None:
    path = tmp_path / "truth.json"
    dump_truth(
        path,
        {
            "changes": [0, 1],
            "authors": 2,
            "paragraph_authors": [1, 1, 2],
            "title": "toy",
        },
    )
    truth = load_truth(path)
    assert truth.changes == (0, 1)
    assert truth.authors == 2
    assert truth.paragraph_authors == (1, 1, 2)


def test_rejects_non_binary(tmp_path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"changes": [0, 2]}), encoding="utf-8")
    try:
        load_truth(path)
    except ValueError as exc:
        assert "0/1" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_collection_pairs_match_paragraphs(doc_dir, truth_dir) -> None:
    pairs = pair_problems(doc_dir, truth_dir)
    assert len(pairs) >= 14
    for doc, gold in pairs:
        n = len(split_paragraphs(load_document(doc)))
        truth = load_truth(gold)
        assert len(truth.changes) == n - 1, doc.name
