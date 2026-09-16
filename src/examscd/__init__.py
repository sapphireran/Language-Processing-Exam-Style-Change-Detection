"""Personal exam study kit for intrinsic style-change detection.

This package is a closed, dependency-free baseline I can actually explain
in an oral exam. It is not a PAN submission and it does not load any
shared-task dump.

The public surface is intentionally small:

- split a document into sentences or paragraphs
- score adjacent units with character n-grams, function words, and a
  tiny closed stylometric vector
- draw a CUSUM on sentence length
- emit PAN-shaped ``changes`` / ``authors`` JSON
- score predictions with macro-F1 and a from-scratch ARI
"""

from examscd.cusum import cusum_points, cusum_series, sentence_lengths
from examscd.detect import (
    authors_from_labels,
    detect_document,
    pair_distance,
    threshold_distances,
)
from examscd.evaluate import (
    adjusted_rand_index,
    boundary_report,
    macro_f1,
)
from examscd.io import read_truth, write_solution
from examscd.tokenize import split_paragraphs, split_sentences, split_units

__all__ = [
    "adjusted_rand_index",
    "authors_from_labels",
    "boundary_report",
    "cusum_points",
    "cusum_series",
    "detect_document",
    "macro_f1",
    "pair_distance",
    "read_truth",
    "sentence_lengths",
    "split_paragraphs",
    "split_sentences",
    "split_units",
    "threshold_distances",
    "write_solution",
]

__version__ = "0.1.0"
