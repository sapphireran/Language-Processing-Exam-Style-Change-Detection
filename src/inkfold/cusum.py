"""CUSUM sketch on one register rate. Oral card: slope change ≠ topic change."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from .features import extract_register


RateFn = Callable[[str], float]


def first_person_rate(text: str) -> float:
    return extract_register([text]).first_person


def contraction_rate(text: str) -> float:
    return extract_register([text]).contraction


def formal_rate(text: str) -> float:
    return extract_register([text]).formal


@dataclass
class CusumTrace:
    values: list[float]
    mean: float
    centered: list[float]
    cusum: list[float]
    peak_after: int  # unit index (1-based left side) where |cusum| is max


def cusum(units: Sequence[str], rate: RateFn = first_person_rate) -> CusumTrace:
    values = [rate(u) for u in units]
    mean = sum(values) / len(values) if values else 0.0
    centered = [v - mean for v in values]
    running = 0.0
    trail = []
    for c in centered:
        running += c
        trail.append(running)
    if not trail:
        peak = 0
    else:
        peak = max(range(len(trail)), key=lambda i: abs(trail[i])) + 1
    return CusumTrace(values=values, mean=mean, centered=centered, cusum=trail, peak_after=peak)


def format_cusum(units: Sequence[str], rate: RateFn = first_person_rate, name: str = "first_person") -> str:
    tr = cusum(units, rate)
    lines = [f"CUSUM on {name}  (mean={tr.mean:.3f}, peak after unit {tr.peak_after})", ""]
    lines.append(f"{'#':>3} {name:>12} {'c':>8} {'S':>8}  text")
    for i, (unit, v, c, s) in enumerate(zip(units, tr.values, tr.centered, tr.cusum), start=1):
        mark = " <—" if i == tr.peak_after else ""
        lines.append(f"{i:3d} {v:12.3f} {c:8.3f} {s:8.3f}  {unit}{mark}")
    return "\n".join(lines)
