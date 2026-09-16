"""HingeMark: personal exam lab for sentence-level style-change detection.

A *hinge* is the joint between two consecutive units (sentences by default).
The exam question is binary: did the hinge hold (same writer) or snap
(style change)? Nothing here is trained on shared-task dumps or company
text. The bundled documents are original teaching prose.
"""

from .calibrate import grid_thresholds, leave_one_out
from .cusum import cusum_trace
from .delta import adjacent_delta
from .detectors import (
    DetectorResult,
    adaptive_detect,
    always_change,
    ensemble_detect,
    never_change,
    threshold_detect,
)
from .evaluate import (
    AccuracyTrap,
    CorpusScores,
    PairScores,
    accuracy_trap,
    score_corpus,
    score_pairs,
)
from .explain import explain_document
from .features import UnitFeatures, extract
from .io import Problem, Truth, read_problem, read_truth, write_solution
from .pairwise import Hinge, score_hinges
from .tokenize import split_units

__version__ = "0.1.0"
__all__ = [
    "AccuracyTrap",
    "CorpusScores",
    "DetectorResult",
    "Hinge",
    "PairScores",
    "Problem",
    "Truth",
    "UnitFeatures",
    "accuracy_trap",
    "adaptive_detect",
    "adjacent_delta",
    "always_change",
    "cusum_trace",
    "ensemble_detect",
    "explain_document",
    "extract",
    "grid_thresholds",
    "leave_one_out",
    "never_change",
    "read_problem",
    "read_truth",
    "score_corpus",
    "score_hinges",
    "score_pairs",
    "split_units",
    "threshold_detect",
    "write_solution",
]
