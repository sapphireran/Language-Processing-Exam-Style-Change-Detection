"""Kerf: treat a document as a walk, then saw it at a change-point.

This is a personal exam toolkit, not a shared-task submission.
The oral thesis is in ``docs/01-a-saw-not-a-classifier.md``.
"""

from .changepoint import binary_segment, split_scores
from .detect import Detection, detect_document, detect_path
from .features import FeatureVector, extract
from .io import Problem, Truth, read_problem, read_truth, write_prediction
from .metrics import hinge_macro_f1, score_directory

__all__ = [
    "Detection",
    "FeatureVector",
    "Problem",
    "Truth",
    "binary_segment",
    "detect_document",
    "detect_path",
    "extract",
    "hinge_macro_f1",
    "read_problem",
    "read_truth",
    "score_directory",
    "split_scores",
    "write_prediction",
]

__version__ = "0.1.0"
