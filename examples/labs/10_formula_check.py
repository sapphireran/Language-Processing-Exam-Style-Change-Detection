"""Check the size weight on a two-house walk I fully control."""

from __future__ import annotations

import math

from kerf.changepoint import split_scores
from kerf.distance import euclidean
from kerf.features import FeatureVector, SAW_WEIGHTS


def fake(second: float) -> FeatureVector:
    rates = {name: 0.0 for name, _ in SAW_WEIGHTS}
    rates["second_person"] = second
    return FeatureVector(rates=rates, n_words=40, n_sentences=3)


def main() -> None:
    left = fake(0.0)
    right = fake(0.2)
    vecs = [left, left, right, right]
    scores = split_scores(vecs)
    mu_l = left.saw_values()
    mu_r = right.saw_values()
    sep = euclidean(mu_l, mu_r)
    expected = []
    n = 4
    for k in (1, 2, 3):
        # k=1: left is one A, right is A+B+B — not computed here;
        # k=2: left two A, right two B — this we can compute exactly.
        weight = math.sqrt(k * (n - k) / n)
        expected.append((k, weight))
    print("size weights for n=4:")
    for k, w in expected:
        print(f"  k={k}  sqrt(k(n-k)/n) = {w:.4f}")
    print(f"||μA − μB|| = {sep:.4f}")
    print(f"score at k=2 (balanced) = {sep * math.sqrt(2 * 2 / 4):.4f}")
    print(f"kerf scores: {[round(s, 4) for s in scores]}")
    assert abs(scores[1] - sep * math.sqrt(1.0)) < 1e-9
    print("balanced cut matches the paper formula.")


if __name__ == "__main__":
    main()
