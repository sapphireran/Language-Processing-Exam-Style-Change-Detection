"""Intrinsic writing-style change detection.

This package is a personal exam / study project. It implements a
dependency-free baseline that:

1. splits a document into sentences or paragraphs
2. extracts a stylometric profile for each unit
3. scores every boundary between consecutive units
4. emits PAN-style binary ``changes`` labels
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
