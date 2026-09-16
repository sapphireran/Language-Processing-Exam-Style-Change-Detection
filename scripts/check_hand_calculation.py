#!/usr/bin/env python3
"""Recompute the paper-and-pencil examples from docs/06 and examples/hand_calculation."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stylechange.distance import cosine_similarity  # noqa: E402
from stylechange.features import extract_profile  # noqa: E402
from stylechange.tokenize import words  # noqa: E402


def main() -> int:
    a = extract_profile("The cat sat on the mat. The cat was sad.")
    b = extract_profile("I can't even. This is just wild, honestly.")
    print("Q3 TTR")
    print(f"  A tokens={a.n_tokens} ttr={a.scalars['type_token_ratio']:.2f}  (expect 10 / 0.70)")
    print(f"  B tokens={b.n_tokens} ttr={b.scalars['type_token_ratio']:.2f}  (expect  8 / 1.00)")
    assert a.n_tokens == 10 and abs(a.scalars["type_token_ratio"] - 0.70) < 1e-9
    assert b.n_tokens == 8 and abs(b.scalars["type_token_ratio"] - 1.00) < 1e-9

    p_text = "I saw the cat of the neighbour."
    q_text = "The theory of the aether was a curiosity and a myth."
    vocab = ("the", "a", "i", "of")
    p_counts = {key: words(p_text).count(key) for key in vocab}
    q_counts = {key: words(q_text).count(key) for key in vocab}
    cos = cosine_similarity(p_counts, q_counts)
    print("Q4 function-word cosine")
    print(f"  P counts={p_counts}")
    print(f"  Q counts={q_counts}")
    print(f"  cos={cos:.3f}  distance={1 - cos:.3f}  (expect ~0.680 / ~0.320)")
    expected = 5 / (3 * math.sqrt(6))
    assert abs(cos - expected) < 1e-9
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
