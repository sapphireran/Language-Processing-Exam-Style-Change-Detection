"""Isogloss: style change as a bundle of closed-class boundaries.

A dialect atlas does not declare a new dialect because one word
changes. It waits for a *bundle* of isoglosses to coincide. This
package treats a document the same way: each closed-class rate draws
its own 1-D map, and a hinge fires only when several of those maps
agree.

Nouns never enter the map. Topic is not a dialect.

This is a personal exam lab. It is not a PAN submission and it does
not ship shared-task data.
"""

from .detect import Detection, detect_paragraphs, detect_text
from .evaluate import Confusion, macro_f1, score_changes
from .features import CHANNELS, FeatureRow, extract, extract_many
from .io import Problem, iter_problems, read_problem, write_solution

__all__ = [
    "CHANNELS",
    "Confusion",
    "Detection",
    "FeatureRow",
    "Problem",
    "detect_paragraphs",
    "detect_text",
    "extract",
    "extract_many",
    "iter_problems",
    "macro_f1",
    "read_problem",
    "score_changes",
    "write_solution",
]

__version__ = "0.1.0"
