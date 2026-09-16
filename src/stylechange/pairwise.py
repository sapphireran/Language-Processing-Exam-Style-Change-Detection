"""Sentence pairs → model matrices."""

from __future__ import annotations

from typing import Literal

import numpy as np

PairMode = Literal["absdiff", "signed", "stack", "cosine"]


def pair_matrix(vectors: np.ndarray, mode: PairMode = "absdiff") -> np.ndarray:
    if len(vectors) < 2:
        return np.zeros((0, vectors.shape[1] if vectors.ndim == 2 else 0), dtype=float)
    left, right = vectors[:-1], vectors[1:]
    if mode == "absdiff":
        return np.abs(left - right)
    if mode == "signed":
        return left - right
    if mode == "stack":
        return np.hstack([left, right, np.abs(left - right)])
    if mode == "cosine":
        return cosine_distance(left, right).reshape(-1, 1)
    raise ValueError(f"unknown pair mode: {mode!r}")


def cosine_distance(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    num = np.sum(left * right, axis=1)
    denom = np.linalg.norm(left, axis=1) * np.linalg.norm(right, axis=1)
    denom = np.where(denom == 0, 1.0, denom)
    return 1.0 - np.clip(num / denom, -1.0, 1.0)


def l1_distance(vectors: np.ndarray) -> np.ndarray:
    if len(vectors) < 2:
        return np.zeros(0, dtype=float)
    return np.sum(np.abs(vectors[1:] - vectors[:-1]), axis=1)
