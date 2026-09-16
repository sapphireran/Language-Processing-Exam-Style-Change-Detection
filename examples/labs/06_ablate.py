#!/usr/bin/env python3
"""Drop one channel at a time and watch macro-F1 move."""

from __future__ import annotations

from _paths import CORPUS  # noqa: E402

from quoin.corpus import load_corpus  # noqa: E402
from quoin.detectors import QuoinDetector  # noqa: E402
from quoin.evaluate import corpus_report  # noqa: E402
from quoin.report import score_corpus  # noqa: E402


def main() -> None:
    corpus = load_corpus(CORPUS)
    variants = {
        "full": QuoinDetector(),
        "no-char": QuoinDetector(w_char=0.0, w_function=0.20, w_shape=0.30, w_register=0.50),
        "no-func": QuoinDetector(w_function=0.0, w_char=0.25, w_shape=0.30, w_register=0.45),
        "no-shape": QuoinDetector(w_shape=0.0, w_char=0.25, w_function=0.20, w_register=0.55),
        "no-reg": QuoinDetector(w_register=0.0, w_char=0.35, w_function=0.25, w_shape=0.40),
        "ncd-only": QuoinDetector(w_ncd=1.0, w_char=0.0, w_function=0.0, w_shape=0.0, w_register=0.0),
        "reg-only": QuoinDetector(w_ncd=0.0, w_char=0.0, w_function=0.0, w_shape=0.0, w_register=1.0),
    }
    print(f"{'variant':<12} {'macro-F1':>9} {'micro-F1':>9} {'acc':>7}")
    print("-" * 40)
    for name, detector in variants.items():
        summary = corpus_report(score_corpus(corpus, detector))
        print(
            f"{name:<12} {summary['macro_f1']:9.3f} {summary['micro_f1']:9.3f} "
            f"{summary['mean_accuracy']:7.3f}"
        )
    print()
    print("If ncd-only collapses, that is the short-paragraph warning.")
    print("If no-func rises on traps, I have started scoring topic.")


if __name__ == "__main__":
    main()
