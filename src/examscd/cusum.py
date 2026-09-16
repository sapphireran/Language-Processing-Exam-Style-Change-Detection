"""Forensic CUSUM on a one-dimensional series (usually sentence length).

The QSUM / CUSUM idea I need in the oral: subtract the document mean
from each observation and accumulate. A writer who prefers short units
drives the cumulative sum down; a writer who prefers long units drives
it up. A slope reversal is the visual cue. It is *not* a full authorship
proof — it is a one-feature sketch I can compute by hand.
"""

from __future__ import annotations

from examscd.tokenize import split_sentences


def sentence_lengths(text: str) -> list[int]:
    """Word counts per sentence. Empty input yields an empty series."""
    return [len(sent.split()) for sent in split_sentences(text)]


def mean(values: list[float] | list[int]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def cusum_series(values: list[float] | list[int]) -> list[float]:
    """S_0 = 0, S_i = S_{i-1} + (x_i - mean). Length is ``len(values) + 1``."""
    if not values:
        return [0.0]
    mu = mean(values)
    running = 0.0
    out = [0.0]
    for value in values:
        running += float(value) - mu
        out.append(running)
    return out


def cusum_points(
    values: list[float] | list[int],
    min_run: int = 2,
    min_swing: float | None = None,
) -> list[int]:
    """Return indices *between* observations where the CUSUM slope reverses.

    Index ``i`` means "the change is after observation i" (0-based), so it
    lines up with a PAN ``changes[i]`` slot. A reversal has to be sustained
    for ``min_run`` steps and travel at least ``min_swing`` (default: 20%
    of the CUSUM range) so a single noisy sentence does not count.
    """
    series = cusum_series(values)
    if len(series) < 4:
        return []
    deltas = [series[i + 1] - series[i] for i in range(len(series) - 1)]
    signs = [1 if d > 0 else -1 if d < 0 else 0 for d in deltas]
    # Carry zeros with the previous non-zero sign so plateaus do not split a run.
    last = 0
    filled: list[int] = []
    for sign in signs:
        if sign == 0:
            filled.append(last if last != 0 else 0)
        else:
            last = sign
            filled.append(sign)
    if min_swing is None:
        lo, hi = min(series), max(series)
        min_swing = 0.20 * (hi - lo) if hi > lo else 0.0

    points: list[int] = []
    i = 0
    n = len(filled)
    while i < n:
        j = i
        while j < n and filled[j] == filled[i]:
            j += 1
        run_travel = abs(series[j] - series[i])
        if j - i >= min_run and run_travel + 1e-12 >= min_swing:
            # Look at the next run; if it is also long enough, mark the joint.
            k = j
            while k < n and filled[k] == filled[j]:
                k += 1
            next_travel = abs(series[k] - series[j])
            if k - j >= min_run and next_travel + 1e-12 >= min_swing and filled[i] != filled[j]:
                # Joint is after observation j-1? series index j is after j observations,
                # so the change slot is j-1? 
                # Observation index 0..n-1. After observation `j` we are at series[j].
                # The last observation of the first run is index j-1.
                # The change is BETWEEN observation j-1 and j, i.e. changes[j-1]?
                # After m observations, series index is m.
                # First run covers observations i .. j-1 inclusive.
                # Next run covers observations j .. k-1.
                # Change is between j-1 and j, so changes[j-1] if we use 0-based pair index.
                # Wait: pair index between unit t and t+1 is t.
                # Units of first run: i .. j-1. Next starts at j. Pair index = j-1.
                # If i=0, j=4, change after units 0,1,2,3 — pair index 3. Yes j-1.
                slot = j - 1
                if 0 <= slot < len(values) - 1:
                    points.append(slot)
        i = j if j > i else i + 1
    return sorted(set(points))


def ascii_cusum(values: list[float] | list[int], width: int = 56, height: int = 11) -> str:
    """Tiny sparkline I can paste into an exam answer or a terminal."""
    series = cusum_series(values)
    if len(series) < 2:
        return "(empty CUSUM)"
    lo, hi = min(series), max(series)
    span = hi - lo if hi > lo else 1.0
    rows = [[" " for _ in range(width)] for _ in range(height)]
    last_c = last_r = None
    for idx, value in enumerate(series):
        col = 0 if len(series) == 1 else round(idx * (width - 1) / (len(series) - 1))
        row = height - 1 - round((value - lo) / span * (height - 1))
        row = min(max(row, 0), height - 1)
        col = min(max(col, 0), width - 1)
        rows[row][col] = "*"
        if last_c is not None:
            steps = max(abs(col - last_c), abs(row - last_r), 1)
            for s in range(1, steps):
                c = last_c + round((col - last_c) * s / steps)
                r = last_r + round((row - last_r) * s / steps)
                if rows[r][c] == " ":
                    rows[r][c] = "·"
        last_c, last_r = col, row
    zero_row = height - 1 - round((0.0 - lo) / span * (height - 1))
    if 0 <= zero_row < height:
        for c, ch in enumerate(rows[zero_row]):
            if ch == " ":
                rows[zero_row][c] = "-"
    body = "\n".join("|" + "".join(row) + "|" for row in rows)
    header = f"CUSUM  n={len(values)}  mean={mean([float(v) for v in values]):.2f}  range=[{lo:.1f}, {hi:.1f}]"
    return header + "\n" + body
