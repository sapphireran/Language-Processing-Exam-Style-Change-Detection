from style_change.detectors import (
    StyleChangeDetector,
    agglomerative_labels,
    cosine_distance,
    knee_threshold,
)
from style_change.tokenize import split_paragraphs

import numpy as np


def test_cosine_identical_and_orthogonal() -> None:
    assert cosine_distance(np.array([1.0, 0.0]), np.array([1.0, 0.0])) == 0.0
    assert cosine_distance(np.array([1.0, 0.0]), np.array([0.0, 1.0])) == 1.0
    assert cosine_distance(np.zeros(3), np.array([1.0, 2.0, 3.0])) == 1.0


def test_agglomerative_recovers_two_blobs() -> None:
    matrix = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.95, 0.05, 0.0],
            [0.0, 0.0, 1.0],
            [0.05, 0.0, 0.95],
        ]
    )
    labels = agglomerative_labels(matrix, threshold=0.3)
    assert labels[0] == labels[1]
    assert labels[2] == labels[3]
    assert labels[0] != labels[2]


def test_knee_uses_first_small_to_large_gap() -> None:
    values = np.array([0.28, 1.76, 0.16, 2.20, 0.33])
    tau = knee_threshold(values, floor=0.75, min_gap=0.45)
    assert 0.75 <= tau < 1.76
    assert 1.76 >= tau
    # a later giant gap must not lift the threshold past the weaker cut
    assert tau < 2.0


def test_knee_unimodal_stays_at_floor() -> None:
    values = np.array([0.31, 0.20, 0.03, 0.15])
    assert knee_threshold(values, floor=0.75) == 0.75


def test_single_paragraph_is_not_multi() -> None:
    detector = StyleChangeDetector(min_words=1)
    _table, result = detector.detect_document(split_paragraphs("Only one paragraph appears here."))
    assert result.multi_author is False
    assert result.authors == [0]
    assert result.changes == []
