"""Detector registry and JSON model I/O."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import Detector
from .baseline import AlwaysZeroDetector, RandomDetector
from .ensemble import EnsembleDetector
from .logistic import LogisticDetector
from .threshold import ThresholdDetector
from .unsupervised import UnsupervisedDetector

DETECTORS: dict[str, type[Detector]] = {
    AlwaysZeroDetector.name: AlwaysZeroDetector,
    RandomDetector.name: RandomDetector,
    UnsupervisedDetector.name: UnsupervisedDetector,
    ThresholdDetector.name: ThresholdDetector,
    LogisticDetector.name: LogisticDetector,
    EnsembleDetector.name: EnsembleDetector,
}


def build(name: str, **kwargs: Any) -> Detector:
    if name not in DETECTORS:
        known = ", ".join(sorted(DETECTORS))
        raise KeyError(f"unknown detector {name!r}; expected one of: {known}")
    return DETECTORS[name](**kwargs)


def save_model(detector: Detector, path: str | Path) -> None:
    payload = detector.to_dict()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def load_model(path: str | Path) -> Detector:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    name = payload.get("name")
    if name not in DETECTORS:
        raise KeyError(f"model {path} has unknown detector name {name!r}")
    detector = DETECTORS[name]()
    detector.from_dict(payload)
    return detector


__all__ = [
    "DETECTORS",
    "AlwaysZeroDetector",
    "Detector",
    "EnsembleDetector",
    "LogisticDetector",
    "RandomDetector",
    "ThresholdDetector",
    "UnsupervisedDetector",
    "build",
    "load_model",
    "save_model",
]
