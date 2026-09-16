"""A four-point walk I can recompute on paper."""

from __future__ import annotations

from kerf.changepoint import split_scores
from kerf.features import FeatureVector, SAW_WEIGHTS


def fake(first: float, second: float, shall: float) -> FeatureVector:
    rates = {name: 0.0 for name, _ in SAW_WEIGHTS}
    rates["first_person"] = first
    rates["second_person"] = second
    rates["fw:shall"] = shall
    return FeatureVector(rates=rates, n_words=80, n_sentences=4)


def main() -> None:
    # A A B B on a 3-d fingerprint.
    vecs = [
        fake(0.08, 0.00, 0.00),
        fake(0.07, 0.00, 0.00),
        fake(0.00, 0.09, 0.04),
        fake(0.00, 0.08, 0.05),
    ]
    scores = split_scores(vecs)
    print("split scores for A,A,B,B:")
    for i, s in enumerate(scores):
        print(f"  after paragraph {i}: {s:.3f}")
    print(f"best cut after paragraph {max(range(len(scores)), key=lambda i: scores[i])}")
    print("The balanced cut (after 1, i.e. between the two houses) should win.")


if __name__ == "__main__":
    main()
