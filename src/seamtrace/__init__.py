"""Seamtrace: personal exam toolkit for intrinsic style-change detection.

The package is intentionally small and dependency-free. It exists so exam
notes can cite live numbers from original teaching documents rather than
hand-waving about stylometry.
"""

from .cusum import cusum_scores
from .delta import burrows_delta
from .detectors import AdaptiveDetector, EnsembleDetector, ThresholdDetector
from .evaluate import PairMetrics, macro_f1, score_pairs
from .features import FeatureTable, extract_unit_features
from .io import Problem, load_problem, load_truth, write_solution
from .pairwise import pair_score, score_document
from .units import split_units

__all__ = [
    "AdaptiveDetector",
    "EnsembleDetector",
    "FeatureTable",
    "PairMetrics",
    "Problem",
    "ThresholdDetector",
    "burrows_delta",
    "cusum_scores",
    "extract_unit_features",
    "load_problem",
    "load_truth",
    "macro_f1",
    "pair_score",
    "score_document",
    "score_pairs",
    "split_units",
    "write_solution",
]

__version__ = "0.1.0"
