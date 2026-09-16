"""Quoin: personal exam lab for intrinsic style-change detection."""

from .calibrate import grid_search_threshold
from .corpus import Corpus, load_corpus
from .detectors import QuoinDetector, always_fire, never_fire
from .evaluate import DocumentScore, corpus_report, macro_f1, micro_f1, safe_f1
from .explain import explain_document
from .features import FeatureVector, pairwise_feature_distance, vectorize
from .io import Problem, Solution, read_problem, read_solution, write_solution
from .ncd import compressed_len, cross_gain, ncd
from .tokenize import paragraphs, sentences, words

__version__ = "0.1.0"

__all__ = [
    "Corpus",
    "DocumentScore",
    "FeatureVector",
    "Problem",
    "QuoinDetector",
    "Solution",
    "__version__",
    "always_fire",
    "compressed_len",
    "corpus_report",
    "cross_gain",
    "explain_document",
    "grid_search_threshold",
    "load_corpus",
    "macro_f1",
    "micro_f1",
    "ncd",
    "never_fire",
    "pairwise_feature_distance",
    "paragraphs",
    "read_problem",
    "read_solution",
    "safe_f1",
    "sentences",
    "vectorize",
    "words",
    "write_solution",
]
