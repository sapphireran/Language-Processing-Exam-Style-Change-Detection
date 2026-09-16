#!/usr/bin/env python3
"""Lab 6: drop one ensemble channel at a time."""

from __future__ import annotations

from _paths import CORPUS, require_corpus
from splicefind.detect import ensemble_scores
from splicefind.evaluate import collection_report, score_document
from splicefind.features import extract_document
from splicefind.io import load_collection


CHANNELS = {
    "full": (3.00, 0.15, 0.40, 0.05),
    "no_delta": (3.00, 0.00, 0.50, 0.05),
    "no_ngram": (3.20, 0.25, 0.00, 0.05),
    "no_register": (0.00, 0.55, 0.80, 0.05),
    "register_only": (1.00, 0.00, 0.00, 0.00),
    "delta_only": (0.00, 1.00, 0.00, 0.00),
    "ngram_only": (0.00, 0.00, 1.00, 0.00),
}


def predict(text: str, weights: tuple[float, float, float, float], threshold: float) -> list[int]:
    from splicefind.detect import relative_flags

    blended, *_ = ensemble_scores(
        extract_document(text),
        weight_feature=weights[0],
        weight_delta=weights[1],
        weight_ngram=weights[2],
        weight_cusum=weights[3],
    )
    return relative_flags(blended, abs_min=threshold)


def main() -> None:
    require_corpus()
    collection = load_collection(CORPUS)
    threshold = 0.55
    print(f"{'channel':<14} macroF1  microF1  acc")
    for name, weights in CHANNELS.items():
        scores = []
        for problem, truth in collection.pairs():
            if truth is None:
                continue
            pred = predict(problem.text, weights, threshold)
            scores.append(score_document(truth.changes, pred, problem.problem_id))
        summary = collection_report(scores)
        print(
            f"{name:<14} {summary['macro_f1']:.3f}    {summary['micro_f1']:.3f}    "
            f"{summary['mean_accuracy']:.3f}"
        )
    print()
    print("If ngram_only wins the easy band in your head, check the hard band.")


if __name__ == "__main__":
    main()
