"""Personal style-change detection toolkit for exam study notes."""

from scd.evaluate import bootstrap_doc_f1, evaluate_directory, macro_f1
from scd.features import pairwise_feature_names, pairwise_features, unit_features
from scd.io import list_problems, read_problem, read_truth, write_solution
from scd.models import StyleChangeModel
from scd.sentences import split_units

__all__ = [
    "StyleChangeModel",
    "bootstrap_doc_f1",
    "evaluate_directory",
    "list_problems",
    "macro_f1",
    "pairwise_feature_names",
    "pairwise_features",
    "read_problem",
    "read_truth",
    "split_units",
    "unit_features",
    "write_solution",
]

__version__ = "0.1.0"
