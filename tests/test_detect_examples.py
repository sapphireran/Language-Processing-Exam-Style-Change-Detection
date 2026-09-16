"""Lock the bundled study texts to their gold change vectors."""

from scdkit.detect import explain_document
from scdkit.evaluate import evaluate_collection
from scdkit.io import iter_collection


def test_every_bundled_document_matches_gold(doc_dir, truth_dir) -> None:
    mismatches = []
    for path, text, truth in iter_collection(doc_dir, truth_dir):
        pred = list(explain_document(text).changes)
        gold = list(truth.changes)
        if pred != gold:
            mismatches.append(f"{path.name}: gold={gold} pred={pred}")
    assert mismatches == []


def test_collection_macro_f1_is_perfect_on_toys(doc_dir, truth_dir) -> None:
    score = evaluate_collection(doc_dir, truth_dir, method="ensemble")
    assert score.macro_f1 == 1.0
    assert score.micro.f1 == 1.0
    assert len(score.documents) == 14


def test_single_author_documents_are_all_zero(doc_dir, truth_dir) -> None:
    singles = {"01_single_ferns.txt", "12_landlord_letter.txt"}
    for path, text, truth in iter_collection(doc_dir, truth_dir):
        if path.name not in singles:
            continue
        assert set(truth.changes) == {0}
        assert list(explain_document(text).changes) == list(truth.changes)


def test_hard_circadian_uses_person_channel(doc_dir) -> None:
    text = (doc_dir / "04_hard_circadian.txt").read_text(encoding="utf-8")
    detection = explain_document(text)
    assert detection.changes == (1, 1, 1)
    assert all(pair.person >= 2 for pair in detection.pairs)
