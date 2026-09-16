"""Personal exam toolkit for paragraph-level style-change detection.

This package is original study material for a Language Processing exam
built around the PAN multi-author writing-style analysis task. It is not
a competition submission and does not include any third-party corpus.
"""

from .evaluate import DocumentScore, collection_report, score_document
from .features import FeatureVector, extract_document, pairwise_feature_distance
from .io import (
    Collection,
    Problem,
    Truth,
    load_collection,
    load_problem,
    load_truth,
    write_solution,
)
from .detect import Detection, detect_document, detect_text

__all__ = [
    "Collection",
    "Detection",
    "DocumentScore",
    "FeatureVector",
    "Problem",
    "Truth",
    "collection_report",
    "detect_document",
    "detect_text",
    "extract_document",
    "load_collection",
    "load_problem",
    "load_truth",
    "pairwise_feature_distance",
    "score_document",
    "write_solution",
]

__version__ = "0.1.0"
