"""Pairwise baselines and a readable logistic-regression style model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from scd.features import document_pair_matrix, pairwise_feature_names
from scd.io import (
    FormatError,
    check_alignment,
    paired_paths,
    read_problem,
    read_truth,
    write_solution,
)
from scd.sentences import split_units


def majority_predict(n_pairs: int, label: int) -> list[int]:
    if label not in (0, 1):
        raise ValueError("label must be 0 or 1")
    return [label] * n_pairs


def random_predict(n_pairs: int, p_change: float, rng: np.random.Generator) -> list[int]:
    if n_pairs == 0:
        return []
    return rng.binomial(1, p_change, size=n_pairs).tolist()


def length_threshold_predict(units: Sequence[str], threshold: float) -> list[int]:
    bits = []
    for left, right in zip(units, units[1:]):
        gap = abs(len(left.split()) - len(right.split()))
        bits.append(int(gap >= threshold))
    return bits


@dataclass
class FittedLogReg:
    scaler: StandardScaler
    clf: LogisticRegression
    feature_names: list[str]
    mode: str

    def predict_proba_matrix(self, matrix: np.ndarray) -> np.ndarray:
        if matrix.size == 0:
            return np.zeros((0, 2), dtype=float)
        return self.clf.predict_proba(self.scaler.transform(matrix))

    def predict_matrix(self, matrix: np.ndarray, *, threshold: float = 0.5) -> list[int]:
        if matrix.size == 0:
            return []
        proba = self.predict_proba_matrix(matrix)[:, 1]
        return (proba >= threshold).astype(int).tolist()

    def top_weights(self, k: int = 12) -> list[tuple[str, float]]:
        coef = self.clf.coef_[0]
        order = np.argsort(np.abs(coef))[::-1]
        return [(self.feature_names[i], float(coef[i])) for i in order[:k]]


class StyleChangeModel:
    """Train / predict pairwise style changes for a directory of problems."""

    def __init__(self, fitted: FittedLogReg, *, threshold: float = 0.5) -> None:
        self.fitted = fitted
        self.threshold = threshold

    @property
    def mode(self) -> str:
        return self.fitted.mode

    def predict_units(self, units: Sequence[str]) -> list[int]:
        matrix = document_pair_matrix(units)
        return self.fitted.predict_matrix(matrix, threshold=self.threshold)

    def predict_proba_units(self, units: Sequence[str]) -> np.ndarray:
        return self.fitted.predict_proba_matrix(document_pair_matrix(units))[:, 1]

    def predict_text(self, text: str) -> list[int]:
        units = split_units(text, mode=self.mode)
        if not units:
            raise FormatError("document produced no units")
        return self.predict_units(units)

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"fitted": self.fitted, "threshold": self.threshold}, path)

    @classmethod
    def load(cls, path: str | Path) -> "StyleChangeModel":
        payload = joblib.load(path)
        return cls(payload["fitted"], threshold=payload.get("threshold", 0.5))


def collect_training_pairs(
    data_root: str | Path,
    *,
    mode: str = "line",
    bands: Sequence[str] | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Stack pairwise features and labels from one root or its band folders."""
    matrices: list[np.ndarray] = []
    labels: list[int] = []
    for directory in iter_band_dirs(data_root, bands=bands):
        for problem, truth_path in paired_paths(directory):
            units = split_units(read_problem(problem), mode=mode)
            changes = read_truth(truth_path).changes
            check_alignment(len(units), changes, path=truth_path)
            if len(units) < 2:
                continue
            matrices.append(document_pair_matrix(units))
            labels.extend(changes)
    if not matrices:
        raise FormatError(f"no training pairs under {data_root}")
    return np.vstack(matrices), np.array(labels, dtype=int)


def iter_band_dirs(
    data_root: str | Path,
    *,
    bands: Sequence[str] | None = None,
) -> Iterable[Path]:
    root = Path(data_root)
    if not root.exists():
        raise FormatError(f"data root does not exist: {root}")
    candidates = [root / name for name in (bands or ("easy", "medium", "hard"))]
    existing = [path for path in candidates if path.is_dir()]
    if existing:
        return existing
    if any(root.glob("problem-*.txt")):
        return [root]
    raise FormatError(f"no band folders or problem files under {root}")


def train_logreg(
    data_root: str | Path,
    *,
    mode: str = "line",
    bands: Sequence[str] | None = None,
    c: float = 0.7,
    seed: int = 0,
) -> StyleChangeModel:
    x, y = collect_training_pairs(data_root, mode=mode, bands=bands)
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    clf = LogisticRegression(
        C=c,
        class_weight="balanced",
        max_iter=500,
        solver="lbfgs",
        random_state=seed,
    )
    clf.fit(x_scaled, y)
    fitted = FittedLogReg(
        scaler=scaler,
        clf=clf,
        feature_names=pairwise_feature_names(),
        mode=mode,
    )
    return StyleChangeModel(fitted)


def predict_directory(
    model: StyleChangeModel,
    input_dir: str | Path,
    output_dir: str | Path,
) -> int:
    """Write one solution file per problem. Returns the number of files written."""
    written = 0
    for problem in sorted(Path(input_dir).glob("problem-*.txt")):
        from scd.io import problem_id

        units = split_units(read_problem(problem), mode=model.mode)
        changes = model.predict_units(units)
        dest = Path(output_dir) / f"solution-problem-{problem_id(problem)}.json"
        write_solution(dest, changes)
        written += 1
    if written == 0:
        raise FormatError(f"no problem-*.txt files in {input_dir}")
    return written
