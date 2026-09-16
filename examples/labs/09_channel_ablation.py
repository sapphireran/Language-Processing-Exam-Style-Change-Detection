"""Drop person / deontic / digit channels and watch macro-F1 move."""

from dataclasses import replace

import _paths  # noqa: F401

from isogloss.detect import detect_paragraphs
from isogloss.evaluate import macro_f1
from isogloss.features import FeatureRow
from isogloss.io import iter_problems
from _paths import CORPUS

DROPS = {
    "no-person": ("i_rate", "we_rate", "you_rate", "one_rate"),
    "no-deontic": ("deontic_rate", "past_copula_rate"),
    "no-digit": ("digit_rate",),
    "no-shape": ("mean_word_len", "n_words", "question_rate"),
}


def zeroed(row: FeatureRow, names: tuple[str, ...]) -> FeatureRow:
    return replace(row, **{name: 0.0 for name in names})


def score_with(drop: tuple[str, ...] | None) -> float:
    gold: list[int] = []
    pred: list[int] = []
    for problem in iter_problems(CORPUS):
        if problem.gold is None:
            continue
        detection = detect_paragraphs(problem.units)
        if drop:
            detection.features = [zeroed(row, drop) for row in detection.features]
            from isogloss.detect import inspect_hinges

            views = inspect_hinges(detection.features)
            pred.extend([1 if v.fires else 0 for v in views])
        else:
            pred.extend(detection.changes)
        gold.extend(problem.gold)
    return macro_f1(gold, pred)


if __name__ == "__main__":
    print(f"{'ablation':<12} macro-F1")
    print(f"{'full':<12} {score_with(None):.3f}")
    for name, drop in DROPS.items():
        print(f"{name:<12} {score_with(drop):.3f}")
