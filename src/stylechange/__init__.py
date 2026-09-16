"""Personal exam-style toolkit for intrinsic style-change detection."""

from .evaluate import EvaluationResult, macro_f1, score_pairs
from .features import FEATURE_NAMES, extract_document, extract_sentence
from .io import load_document, load_problem_dir, write_solution
from .sentences import split_sentences

__all__ = [
    "FEATURE_NAMES",
    "EvaluationResult",
    "extract_document",
    "extract_sentence",
    "load_document",
    "load_problem_dir",
    "macro_f1",
    "score_pairs",
    "split_sentences",
    "write_solution",
]

__version__ = "0.2.0"
