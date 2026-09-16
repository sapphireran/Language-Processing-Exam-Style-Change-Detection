"""The bundled example documents are the acceptance tests for the baseline."""

from pathlib import Path

import pytest

from stylechange import StyleChangeDetector, evaluate_changes
from stylechange.generate import generate_document, generate_split
from stylechange.io import iter_problems

DOC_DIR = Path(__file__).resolve().parents[1] / "examples" / "documents"


def _prediction(problem):
    granularity = "sentence"
    if problem.truth and problem.truth.extra.get("granularity") == "paragraph":
        granularity = "paragraph"
    detector = StyleChangeDetector(granularity=granularity)
    return detector.predict(problem.text)


@pytest.mark.parametrize(
    "problem_id",
    [
        "easy-mixed-topics",
        "medium-one-topic",
        "hard-close-register",
        "exam-answer-shift",
        "single-author",
        "paragraph-gift-authorship",
    ],
)
def test_each_bundled_example_matches_gold(problem_id):
    problem = next(p for p in iter_problems(DOC_DIR) if p.problem_id == problem_id)
    assert problem.truth is not None
    prediction = _prediction(problem)
    assert prediction.changes == problem.truth.changes
    assert len(prediction.changes) == len(prediction.units) - 1


def test_collection_macro_f1_is_perfect():
    gold = []
    pred = []
    for problem in iter_problems(DOC_DIR):
        gold.append(problem.truth.changes)
        pred.append(_prediction(problem).changes)
    result = evaluate_changes(gold, pred)
    assert result.macro_f1 == 1.0
    assert result.skipped == 0


def test_generated_single_author_has_no_changes():
    document = generate_document(difficulty="single", seed=3)
    assert document.truth.changes == [0] * (len(document.units) - 1)
    assert set(document.authors) == {document.authors[0]}


def test_generated_easy_has_two_voice_changes():
    document = generate_document(difficulty="easy", seed=11)
    assert sum(document.truth.changes) == 2
    assert document.truth.authors == 3


def test_generate_split_sizes():
    documents = generate_split(n_per_level=2, seed=1)
    assert len(documents) == 8
    assert {d.difficulty for d in documents} == {"easy", "medium", "hard", "single"}


def test_explain_has_register_axes():
    problem = next(p for p in iter_problems(DOC_DIR) if p.problem_id == "exam-answer-shift")
    prediction = StyleChangeDetector().predict(problem.text, explain=True)
    assert len(prediction.explanations) == len(prediction.changes)
    changed = [item for item in prediction.explanations if item.change]
    assert changed
    assert "personal" in changed[0].register_left
    assert changed[0].score > 0
