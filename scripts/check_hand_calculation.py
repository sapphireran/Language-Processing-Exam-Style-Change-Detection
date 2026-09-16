#!/usr/bin/env python3
"""Recompute the closed-form examples quoted in the exam notes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seamtrace.handcalc import cosine_from_counts, macro_f1_from_cells, type_token_ratio
from seamtrace.tokenize import words


def main() -> int:
    tokens = words("I think we should probably go.")
    ttr = type_token_ratio(tokens)
    print(f"TTR('I think we should probably go.') = {ttr:.3f}  tokens={tokens}")
    if abs(ttr - 1.0) > 1e-9:
        raise SystemExit("expected all unique tokens")

    a = {"the": 2, "of": 1, "you": 0}
    b = {"the": 1, "of": 1, "you": 2}
    cos = cosine_from_counts(a, b)
    print(f"cosine(function-word toy) = {cos:.3f}")
    if not 0.4 < cos < 0.8:
        raise SystemExit(f"unexpected cosine {cos}")

    f1 = macro_f1_from_cells(0, 0, 16, 4)
    print(f"never-fire 16/4 macro-F1 = {f1:.3f}")
    if abs(f1 - 0.444444) > 1e-3:
        raise SystemExit(f"expected ~0.444, got {f1}")
    print("hand calculations ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
