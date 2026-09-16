from seamtrace.corpus import load_teaching_corpus
from seamtrace.detectors import AdaptiveDetector, EnsembleDetector, ThresholdDetector
from seamtrace.evaluate import score_pairs
from seamtrace.features import FeatureTable


def _doc(stem: str):
    return next(d for d in load_teaching_corpus() if d.stem == stem)


def test_output_length() -> None:
    doc = _doc("problem-02-bikes-vellum")
    table = doc.table()
    for det in (ThresholdDetector(), AdaptiveDetector(), EnsembleDetector()):
        pred = det.predict(table)
        assert len(pred) == len(doc.changes)
        assert set(pred) <= {0, 1}


def test_empty_and_single_unit() -> None:
    empty = FeatureTable.from_units([])
    one = FeatureTable.from_units(["Only one unit."])
    assert ThresholdDetector().predict(empty) == []
    assert ThresholdDetector().predict(one) == []


def test_easy_topic_aligned_seam_is_recoverable() -> None:
    from seamtrace.pairwise import score_document

    doc = _doc("problem-02-bikes-vellum")
    rows = score_document(doc.table())
    pred = ThresholdDetector().predict(doc.table())
    seam = doc.changes.index(1)
    assert pred[seam] == 1
    stay = [row.combined for i, row in enumerate(rows) if doc.changes[i] == 0]
    assert rows[seam].combined >= max(stay)


def test_never_worse_than_always_on_change_f1_is_not_required() -> None:
    # Smoke: scoring the whole corpus does not crash and returns [0, 1].
    gold: list[int] = []
    pred: list[int] = []
    det = ThresholdDetector()
    for doc in load_teaching_corpus():
        gold.extend(doc.changes)
        pred.extend(det.predict(doc.table()))
    metrics = score_pairs(gold, pred)
    assert 0.0 <= metrics.macro_f1 <= 1.0
    assert metrics.support_0 + metrics.support_1 == len(gold)
