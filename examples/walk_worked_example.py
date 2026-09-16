#!/usr/bin/env python3
"""Print the locked numbers from docs/05-worked-example.md."""

from __future__ import annotations

import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scarfjoint.distances import cosine, cosine_distance, jensen_shannon  # noqa: E402
from scarfjoint.evaluate import document_scores  # noqa: E402
from scarfjoint.features import extract_features  # noqa: E402
from scarfjoint.lexicons import FUNCTION_WORDS  # noqa: E402
from scarfjoint.richness import richness  # noqa: E402

P1 = (
    "I think we should take the late boat. I cannot stand the morning "
    "crowd on the pier."
)
P2 = (
    "The analysis suggests that tidal delay should be treated as a "
    "structural constraint rather than a residual error."
)
SUBSET = ["i", "the", "that", "should", "a", "as"]
YULE_TOY = ("the", "the", "boat", "the", "pier")


def _subset_vec(words_lower: tuple[str, ...]) -> list[float]:
    n = len(words_lower)
    counts = Counter(words_lower)
    return [counts[w] / n for w in SUBSET]


def main() -> int:
    f1 = extract_features(P1)
    f2 = extract_features(P2)
    print("P1 tokens:", " ".join(f1.tokens.words_lower))
    print("P2 tokens:", " ".join(f2.tokens.words_lower))
    print(f"n1={f1.n_words}  n2={f2.n_words}")
    print()
    print("function-word cosine (full basis): "
          f"{cosine(f1.function_word_rel, f2.function_word_rel):.3f}")
    print("function-word cosine distance: "
          f"{cosine_distance(f1.function_word_rel, f2.function_word_rel):.3f}")
    print(f"Jensen-Shannon: {jensen_shannon(f1.function_word_rel, f2.function_word_rel):.3f}")
    print()
    a, b = _subset_vec(f1.tokens.words_lower), _subset_vec(f2.tokens.words_lower)
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    print(f"subset {SUBSET}")
    print("P1", [round(x, 4) for x in a])
    print("P2", [round(x, 4) for x in b])
    print(f"hand cosine ≈ {dot / (na * nb):.3f}  (dot={dot:.5f}, |P1|={na:.4f}, |P2|={nb:.4f})")
    print()
    print(f"first-person  P1={f1.first_person_rate:.3f}  P2={f2.first_person_rate:.3f}")
    print(f"academic      P1={f1.academic_rate:.3f}  P2={f2.academic_rate:.3f}")
    print(f"mean sent len P1={f1.mean_sent_len:.1f}  P2={f2.mean_sent_len:.1f}")
    print(f"Flesch proxy  P1={f1.flesch_proxy:.1f}  P2={f2.flesch_proxy:.1f}")
    print()
    toy = richness(YULE_TOY)
    print(f"Yule K on {YULE_TOY}: {toy.yule_k:.1f}  (hand target 2400)")
    print()
    bundle = document_scores([0, 1, 0, 1], [0, 1, 1, 1])
    print(
        f"confusion demo  F1={bundle.f1:.3f}  macro-F1={bundle.macro_f1:.3f}  "
        f"acc={bundle.accuracy:.3f}  tp={bundle.tp} fp={bundle.fp} tn={bundle.tn} fn={bundle.fn}"
    )
    nonzero = []
    index = {w: i for i, w in enumerate(FUNCTION_WORDS)}
    for word, i in index.items():
        if f1.function_word_rel[i] or f2.function_word_rel[i]:
            nonzero.append(
                f"{word:8s}  {f1.function_word_rel[i]:.4f}  {f2.function_word_rel[i]:.4f}"
            )
    print("\nnon-zero function words (P1, P2):")
    print("\n".join(nonzero))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
