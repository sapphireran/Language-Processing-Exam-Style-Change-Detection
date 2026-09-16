"""Pencil-and-paper counts that should match ``inkfold explain``."""

from __future__ import annotations

from typing import Sequence

from . import lexicon
from .features import LENGTH_SCALE, extract_register
from .tokenize import word_tokens


def count_row(text: str) -> dict[str, int | float | str]:
    tokens = word_tokens(text)
    return {
        "text": text,
        "tokens": len(tokens),
        "first_person": sum(t in lexicon.FIRST_PERSON for t in tokens),
        "second_person": sum(t in lexicon.SECOND_PERSON for t in tokens),
        "contraction": sum(t in lexicon.CONTRACTIONS for t in tokens),
        "formal": sum(t in lexicon.FORMAL for t in tokens),
        "hedge": sum(t in lexicon.HEDGES for t in tokens),
        "we_person": sum(t in lexicon.WE_PERSON for t in tokens),
    }


def table(units: Sequence[str]) -> list[dict[str, int | float | str]]:
    return [count_row(u) for u in units]


def span_rates(units: Sequence[str]) -> dict[str, float]:
    reg = extract_register(units)
    return {
        "tokens": float(reg.tokens),
        "units": float(reg.units),
        "first_person": reg.first_person,
        "second_person": reg.second_person,
        "contraction": reg.contraction,
        "formal": reg.formal,
        "hedge": reg.hedge,
        "we_person": reg.we_person,
        "length": reg.length,
        "mean_unit_tokens": (reg.tokens / reg.units) if reg.units else 0.0,
        "length_scale": LENGTH_SCALE,
    }


def format_table(units: Sequence[str]) -> str:
    rows = table(units)
    header = (
        f"{'#':>3} {'tok':>4} {'I':>3} {'you':>3} {'ctr':>3} {'frm':>3} {'hdg':>3} {'we':>3}  text"
    )
    lines = [header, "-" * 88]
    totals = {"tokens": 0, "first_person": 0, "second_person": 0, "contraction": 0, "formal": 0, "hedge": 0, "we_person": 0}
    for i, row in enumerate(rows, start=1):
        lines.append(
            f"{i:3d} {row['tokens']:4d} {row['first_person']:3d} {row['second_person']:3d} "
            f"{row['contraction']:3d} {row['formal']:3d} {row['hedge']:3d} {row['we_person']:3d}  "
            f"{row['text']}"
        )
        for key in totals:
            totals[key] += int(row[key])
    lines.append("-" * 88)
    lines.append(
        f"{'Σ':>3} {totals['tokens']:4d} {totals['first_person']:3d} {totals['second_person']:3d} "
        f"{totals['contraction']:3d} {totals['formal']:3d} {totals['hedge']:3d} {totals['we_person']:3d}"
    )
    rates = span_rates(units)
    lines.append("")
    lines.append("exam rates (count / tokens). length is shown but not in L1:")
    for key in ("first_person", "second_person", "contraction", "formal", "hedge", "we_person", "length"):
        lines.append(f"  {key:16s} {rates[key]:.4f}")
    return "\n".join(lines)
