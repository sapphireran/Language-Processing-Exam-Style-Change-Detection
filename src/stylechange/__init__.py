"""Intrinsic style-change detection utilities for a personal language-processing exam.

The package is intentionally small and dependency-free. It implements the
paragraph-level PAN-style task: given a document, emit a binary label for
every boundary between consecutive paragraphs.
"""

from stylechange.detectors import AdaptiveDetector, ThresholdDetector
from stylechange.evaluate import score_changes, score_corpus
from stylechange.features import StyleProfile, extract_profile
from stylechange.io import load_problem, load_truth, write_solution
from stylechange.paragraphs import split_paragraphs

__version__ = "0.1.0"
__all__ = [
    "AdaptiveDetector",
    "StyleProfile",
    "ThresholdDetector",
    "extract_profile",
    "load_problem",
    "load_truth",
    "score_changes",
    "score_corpus",
    "split_paragraphs",
    "write_solution",
]
