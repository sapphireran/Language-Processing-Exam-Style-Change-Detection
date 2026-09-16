"""Intrinsic writing-style change detection.

Personal exam / study baseline. The default model:

1. splits a document into sentences or paragraphs
2. extracts a stylometric profile for each unit
3. projects those profiles onto personal / academic / telegram axes
4. binary-segments contiguous author blocks
5. emits PAN-style binary ``changes`` labels
"""

from .detector import StyleChangeDetector, StyleChangePrediction
from .evaluate import EvaluationResult, evaluate_changes, evaluate_dataset
from .features import FeatureVector, extract_features
from .register import register_axes
from .io import Problem, Solution, load_problem, write_solution
from .tokenize import split_paragraphs, split_sentences, split_units

__all__ = [
    "EvaluationResult",
    "FeatureVector",
    "Problem",
    "Solution",
    "StyleChangeDetector",
    "StyleChangePrediction",
    "evaluate_changes",
    "evaluate_dataset",
    "extract_features",
    "load_problem",
    "register_axes",
    "split_paragraphs",
    "split_sentences",
    "split_units",
    "write_solution",
]

__version__ = "0.2.0"
