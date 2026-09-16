"""inkfold: personal exam lab for style-change detection.

A document is a sheet. A style change is a fold. Counting folds is not
the same as counting authors if the sheet is folded back onto an earlier
voice (the return-author trap).

Everything here is stdlib-only and written for a language-processing
exam, not for a shared task submission.
"""

from .detectors import (
    AdaptiveDetector,
    EnsembleDetector,
    ThresholdDetector,
    default_detector,
)
from .evaluate import score_document, score_folder
from .explain import explain_document
from .features import RegisterVector, extract_register, extract_unit
from .io import read_problem, read_truth, write_prediction

__all__ = [
    "AdaptiveDetector",
    "EnsembleDetector",
    "RegisterVector",
    "ThresholdDetector",
    "default_detector",
    "explain_document",
    "extract_register",
    "extract_unit",
    "read_problem",
    "read_truth",
    "score_document",
    "score_folder",
    "write_prediction",
]

__version__ = "0.1.0"
