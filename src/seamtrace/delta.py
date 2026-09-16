"""Burrows' Delta on a shared function-word space.

Classic Delta (Burrows 2002) z-scores each closed-class frequency
across the units being compared, then takes the mean absolute
difference of those z-scores. It is a *distance*, not a similarity:
larger means more unlike.

For a two-unit pair we z-score using the document's whole table so a
pair inherits a stable scale. Exam answers should mention that Delta
needs a closed-class list and a comparison sample; it is not magic.
"""

from __future__ import annotations

from .features import FeatureTable, UnitFeatures
from .vector import pop_std


def _column_z(table: FeatureTable, index: int, value: float) -> float:
    col = [unit.function_words[index] for unit in table.units]
    s = pop_std(col)
    if s == 0.0:
        return 0.0
    m = sum(col) / len(col)
    return (value - m) / s


def burrows_delta(left: UnitFeatures, right: UnitFeatures, table: FeatureTable) -> float:
    if not table.units:
        return 0.0
    n = len(left.function_words)
    if n == 0:
        return 0.0
    total = 0.0
    for i in range(n):
        z_l = _column_z(table, i, left.function_words[i])
        z_r = _column_z(table, i, right.function_words[i])
        total += abs(z_l - z_r)
    return total / n
