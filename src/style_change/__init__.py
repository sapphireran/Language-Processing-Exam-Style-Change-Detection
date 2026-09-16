"""Stylometric style-change detection for personal exam study.

The public surface is intentionally small: tokenize a document, extract
paragraph-level features, detect changes, and score a prediction against
gold labels.
"""

from style_change.detectors import (
    DetectionResult,
    StyleChangeDetector,
    detect_style_changes,
)
from style_change.evaluate import EvaluationReport, evaluate_document
from style_change.features import (
    DETECTION_FEATURES,
    STYLE_AXIS_NAMES,
    FeatureExtractor,
    FeatureTable,
    style_axes,
)
from style_change.tokenize import Document, Paragraph, split_paragraphs

__all__ = [
    "DETECTION_FEATURES",
    "STYLE_AXIS_NAMES",
    "DetectionResult",
    "Document",
    "EvaluationReport",
    "FeatureExtractor",
    "FeatureTable",
    "Paragraph",
    "StyleChangeDetector",
    "detect_style_changes",
    "evaluate_document",
    "split_paragraphs",
    "style_axes",
]

__version__ = "0.1.0"
