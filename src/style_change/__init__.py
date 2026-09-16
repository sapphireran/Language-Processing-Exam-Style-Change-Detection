"""Intrinsic style-change detection study toolkit."""

from .detectors import DETECTORS, EnsembleDetector, StyleChangeDetector
from .evaluate import EvaluationResult, evaluate_changes, macro_f1
from .features import StylometricProfile, extract_profile
from .io import Problem, load_problem, load_problem_dir, write_solution
from .paragraphs import split_paragraphs

__all__ = [
    "DETECTORS",
    "EnsembleDetector",
    "EvaluationResult",
    "Problem",
    "StyleChangeDetector",
    "StylometricProfile",
    "evaluate_changes",
    "extract_profile",
    "load_problem",
    "load_problem_dir",
    "macro_f1",
    "split_paragraphs",
    "write_solution",
]

__version__ = "0.1.0"
