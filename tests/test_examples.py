from pathlib import Path

from style_change.detectors import StyleChangeDetector
from style_change.evaluate import evaluate_document
from style_change.io import load_document, load_labels

ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = ROOT / "examples" / "documents"
LABEL_DIR = DOC_DIR / "labels"


def _run(name: str):
    labels = load_labels(LABEL_DIR / f"{name}.json")
    document = load_document(DOC_DIR / labels["document"])
    table, result = StyleChangeDetector().detect_document(document)
    report = evaluate_document(
        result,
        gold_authors=labels["authors"],
        gold_multi=labels["multi_author"],
        gold_changes=labels.get("changes"),
    )
    return labels, result, report, table


def test_single_author_documents_stay_unmixed() -> None:
    for name in ("single_author_formal", "single_author_casual"):
        labels, result, report, _table = _run(name)
        assert result.multi_author is False, name
        assert report.task1.accuracy == 1.0
        assert report.task1.f1 == 1.0
        assert report.task2.f1 == 1.0
        assert not any(result.changes), name
        assert labels["multi_author"] is False


def test_mixed_formal_casual_finds_the_one_cut() -> None:
    labels, result, report, _table = _run("mixed_formal_casual")
    assert result.multi_author is True
    assert report.task1.f1 == 1.0
    assert result.changes == labels["changes"]
    assert len(set(result.authors[:3])) == 1
    assert len(set(result.authors[3:])) == 1
    assert result.authors[0] != result.authors[3]


def test_three_author_document_has_two_boundaries() -> None:
    labels, result, report, _table = _run("mixed_three_authors")
    assert result.multi_author is True
    assert result.changes == labels["changes"]
    assert report.task2.f1 == 1.0
    assert len(set(result.authors)) == 3


def test_returning_author_reuses_first_id() -> None:
    labels, result, report, _table = _run("mixed_return_author")
    assert result.multi_author is True
    assert result.changes == labels["changes"]
    assert result.authors[0] == result.authors[-1]
    assert result.authors[0] != result.authors[2]
    assert report.ari == 1.0
