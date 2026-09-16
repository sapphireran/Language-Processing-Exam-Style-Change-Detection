"""Scarfjoint: a personal exam lab for paragraph-level style-change detection.

A scarf joint is the end-to-end splice that hides a join in timber. The
lab's job is to find the analogous splice in a document: the blank line
where one author's habits stop and another author's habits begin.

Nothing here is a PAN submission, a course official, or company code.
The bundled documents are original teaching prose. Thresholds were set
on those documents. Do not quote the collection score as a shared-task
result.
"""

from .detectors import DetectedBoundary, Detection, ScarfDetector
from .evaluate import MetricBundle, binary_f1, document_scores, macro_f1
from .features import ParagraphFeatures, extract_features
from .io import ProblemDocument, iter_corpus, load_problem, load_truth, write_solution
from .paragraphs import split_paragraphs

__all__ = [
    "DetectedBoundary",
    "Detection",
    "MetricBundle",
    "ParagraphFeatures",
    "ProblemDocument",
    "ScarfDetector",
    "binary_f1",
    "document_scores",
    "extract_features",
    "iter_corpus",
    "load_problem",
    "load_truth",
    "macro_f1",
    "split_paragraphs",
    "write_solution",
]

__version__ = "0.1.0"
