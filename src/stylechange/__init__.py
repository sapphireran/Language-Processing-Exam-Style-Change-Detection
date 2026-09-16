"""Intrinsic style-change detection for a personal language-processing exam.

The public surface is small on purpose: segment a document, score each unit,
assign a coarse writing voice, then mark the boundaries where that voice
(or a stylometric span) jumps.

Nothing here is trained. Nothing here talks to a network. The point is to
have an inspectable baseline you can defend in an oral exam.
"""

from .detector import Detection, detect
from .evaluate import CollectionScore, evaluate_collection, macro_f1
from .features import FeatureVector, extract
from .generate import Block, mix_blocks
from .io import load_problem, write_solution
from .tokenize import segment
from .voices import VOICES, classify_voice

__all__ = [
    "Block",
    "CollectionScore",
    "Detection",
    "FeatureVector",
    "VOICES",
    "classify_voice",
    "detect",
    "evaluate_collection",
    "extract",
    "load_problem",
    "macro_f1",
    "mix_blocks",
    "segment",
    "write_solution",
]

__version__ = "0.1.0"
