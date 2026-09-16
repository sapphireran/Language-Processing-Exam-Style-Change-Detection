from pathlib import Path

from stylechange.detectors import ThresholdDetector
from stylechange.evaluate import score_changes
from stylechange.io import load_split
from stylechange.topic import topic_distance

ROOT = Path(__file__).resolve().parents[1] / "examples" / "data"


def _pairs(split: str):
    return load_split(ROOT / split)


def test_easy_corpus_is_well_formed():
    rows = _pairs("easy")
    assert [problem.problem_id for problem, _ in rows] == ["001", "002", "003"]
    for problem, truth in rows:
        assert truth is not None
        assert len(truth.changes) == len(problem.paragraphs) - 1
        assert all(label in (0, 1) for label in truth.changes)


def test_easy_change_boundaries_are_stylistically_larger():
    detector = ThresholdDetector(threshold=1.0)  # distances only
    same, changed = [], []
    for problem, truth in _pairs("easy"):
        assert truth is not None
        detection = detector.predict_paragraphs(problem.paragraphs)
        for label, dist in zip(truth.changes, detection.distances, strict=True):
            (changed if label else same).append(dist)
    assert same and changed
    assert min(changed) > max(same)


def test_easy_001_topic_tracks_the_known_shift():
    problem, truth = _pairs("easy")[0]
    assert truth is not None and truth.changes == [0, 1, 0]
    topic = [
        topic_distance(problem.paragraphs[i], problem.paragraphs[i + 1])
        for i in range(len(problem.paragraphs) - 1)
    ]
    assert topic[1] > topic[0]
    assert topic[1] >= 0.85
    assert topic[2] < topic[1]


def test_control_documents_are_single_author():
    for problem, truth in _pairs("control"):
        assert truth is not None
        assert truth.authors == 1
        assert truth.changes == [0] * (len(problem.paragraphs) - 1)


def test_default_threshold_is_sane_on_easy_and_control():
    detector = ThresholdDetector()
    easy_f1 = []
    for problem, truth in _pairs("easy"):
        pred = detector.predict_paragraphs(problem.paragraphs).changes
        easy_f1.append(score_changes(truth.changes, pred).f1)
    assert sum(easy_f1) / len(easy_f1) >= 0.75

    for problem, truth in _pairs("control"):
        pred = detector.predict_paragraphs(problem.paragraphs).changes
        # Single-author controls should not be sprayed with false changes.
        assert pred.count(1) <= 1
