#!/usr/bin/env python3
"""Train the pooled pairwise logistic baseline and score each band.

Prints:
  * pair counts and the positive (change) rate
  * majority-0 macro F1 as the first comparison
  * trained macro F1 and mean per-document F1 per band
  * the largest-magnitude coefficients (the readable story)

This is the script behind docs/04-baselines-and-models.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scd.evaluate import evaluate_directory, macro_f1
from scd.generate import TRAIN_ID_MAX
from scd.models import collect_training_pairs, majority_predict, predict_directory, train_logreg

DATA = ROOT / "examples" / "data"
MODELS = ROOT / "models"
BANDS = ("easy", "medium", "hard")
HOLD_MIN = TRAIN_ID_MAX + 1


def majority_score(scores) -> float:
    y_true: list[int] = []
    y_pred: list[int] = []
    for doc in scores.per_document:
        y_true.extend(doc.y_true)
        y_pred.extend(majority_predict(doc.n_pairs, 0))
    return macro_f1(y_true, y_pred)


def main() -> int:
    x, y = collect_training_pairs(DATA, id_min=1, id_max=TRAIN_ID_MAX)
    print(f"train ids 1–{TRAIN_ID_MAX}   pairs: {len(y)}   positive rate: {y.mean():.3f}")
    print(f"holdout ids {HOLD_MIN}–18")
    print()

    model = train_logreg(DATA, seed=0, id_min=1, id_max=TRAIN_ID_MAX)
    MODELS.mkdir(exist_ok=True)
    dest = MODELS / "baseline.joblib"
    model.save(dest)
    print(f"saved {dest.relative_to(ROOT)}")
    print()
    print("largest |weights| (pooled model)")
    for name, weight in model.fitted.top_weights(12):
        print(f"  {weight:+7.3f}  {name}")
    print()

    print(f"{'band':<8} {'pairs':>6} {'pos':>6} {'maj0':>6} {'F1':>6} {'mean-doc':>8}")
    for band in BANDS:
        pred_dir = MODELS / f"pred-{band}"
        predict_directory(model, DATA / band, pred_dir, id_min=HOLD_MIN)
        scores = evaluate_directory(pred_dir, DATA / band, id_min=HOLD_MIN)
        print(
            f"{band:<8} {scores.n_pairs:6d} {scores.positive_rate:6.3f} "
            f"{majority_score(scores):6.3f} {scores.macro_f1:6.3f} "
            f"{scores.mean_doc_macro_f1:8.3f}"
        )
    print()
    print("Read the weights against docs/03-stylometric-features.md.")
    print("Holdout bands are ~20–30 pairs; quote the 3×3 table in")
    print("examples/04_compare_difficulties.py, not a single F1.")
    print("If Jaccard dominates the weights, the pooled mix is still too easy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
