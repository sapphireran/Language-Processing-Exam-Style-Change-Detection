"""Personal exam lab: intrinsic paragraph-level style-change detection.

This package is a study kit, not a PAN submission. It implements the
classical stylometric story you can still defend at an oral exam:

1. Split a document into paragraphs (one author per paragraph).
2. Build a style fingerprint for each paragraph.
3. Score every adjacent pair.
4. Emit a binary ``changes`` vector of length ``n_paragraphs - 1``.

The default detector is an unsupervised ensemble of function-word Delta,
character n-gram cosine, register jumps, and a robust CUSUM channel.
"""

from .detect import Detection, detect_changes, explain_document
from .evaluate import (
    CollectionScore,
    binary_scores,
    evaluate_collection,
    macro_f1,
)
from .features import ParagraphFeatures, extract_features
from .io import (
    dump_truth,
    load_document,
    load_truth,
    write_prediction,
)
from .tokenize import split_paragraphs, split_sentences, split_words

__all__ = [
    "CollectionScore",
    "Detection",
    "ParagraphFeatures",
    "binary_scores",
    "detect_changes",
    "dump_truth",
    "evaluate_collection",
    "explain_document",
    "extract_features",
    "load_document",
    "load_truth",
    "macro_f1",
    "split_paragraphs",
    "split_sentences",
    "split_words",
    "write_prediction",
]

__version__ = "0.1.0"
