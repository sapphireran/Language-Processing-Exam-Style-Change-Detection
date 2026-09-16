from pathlib import Path

import json

from splicefind.detect import detect_text
from splicefind.evaluate import score_document
from splicefind.io import load_collection


CORPUS = Path(__file__).resolve().parents[1] / "examples" / "corpus"


def test_corpus_truth_lengths_match_boundaries():
    collection = load_collection(CORPUS)
    assert len(collection) == 18
    for problem, truth in collection.pairs():
        assert truth is not None, problem.problem_id
        assert len(truth.changes) == problem.n_boundaries
        assert truth.authors is not None
        assert 1 + sum(truth.changes) >= truth.authors or truth.authors == 1


def test_manifest_lists_every_problem():
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    ids = {item["id"] for item in manifest["documents"]}
    collection = load_collection(CORPUS)
    on_disk = {problem.problem_id for problem in collection.problems}
    assert ids == on_disk


def test_single_author_allotment_is_not_all_changes():
    collection = load_collection(CORPUS)
    problem = next(p for p in collection.problems if p.problem_id == "01-allotment")
    truth = collection.truths["01-allotment"]
    detection = detect_text(problem.text)
    score = score_document(truth.changes, detection.changes, problem.problem_id)
    assert truth.changes == [0, 0, 0]
    assert score.false_positives <= 1


def test_grandma_landlord_recovers_the_middle_cut():
    collection = load_collection(CORPUS)
    problem = next(p for p in collection.problems if p.problem_id.endswith("grandma-and-landlord"))
    truth = collection.truths[problem.problem_id]
    detection = detect_text(problem.text)
    assert truth.changes == [0, 1, 0]
    assert detection.changes[1] == 1
