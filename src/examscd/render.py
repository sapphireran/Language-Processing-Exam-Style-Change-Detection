"""Dependency-free SVG so a CUSUM can sit in the exam notes as a figure."""

from __future__ import annotations

from pathlib import Path

from examscd.cusum import cusum_series, mean


def cusum_svg(
    values: list[float] | list[int],
    path: str | Path,
    width: int = 720,
    height: int = 280,
    title: str = "CUSUM of sentence length",
    change_slots: list[int] | None = None,
) -> Path:
    """Write a small SVG. ``change_slots`` are pair indices to mark with a line."""
    series = cusum_series(values)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    pad_l, pad_r, pad_t, pad_b = 56, 18, 36, 40
    inner_w = width - pad_l - pad_r
    inner_h = height - pad_t - pad_b
    lo, hi = min(series), max(series)
    span = hi - lo if hi > lo else 1.0

    def xy(i: int, value: float) -> tuple[float, float]:
        x = pad_l + (i / max(len(series) - 1, 1)) * inner_w
        y = pad_t + (1.0 - (value - lo) / span) * inner_h
        return x, y

    points = " ".join(f"{xy(i, v)[0]:.1f},{xy(i, v)[1]:.1f}" for i, v in enumerate(series))
    zero_y = xy(0, 0.0)[1]
    marks = []
    for slot in change_slots or []:
        # slot i sits between observation i and i+1, which is series index i+1
        idx = slot + 1
        if 0 <= idx < len(series):
            x, _ = xy(idx, series[idx])
            marks.append(
                f'<line x1="{x:.1f}" y1="{pad_t}" x2="{x:.1f}" y2="{height - pad_b}" '
                f'stroke="#c0392b" stroke-dasharray="4 3" stroke-width="1.5"/>'
            )
    ticks = []
    for i, raw in enumerate(values):
        x, _ = xy(i + 1, series[i + 1] if i + 1 < len(series) else series[-1])
        ticks.append(
            f'<text x="{x:.1f}" y="{height - 14}" text-anchor="middle" '
            f'font-size="10" fill="#444">{raw}</text>'
        )
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fffaf3"/>
  <text x="{pad_l}" y="22" font-size="14" font-family="ui-sans-serif, sans-serif" fill="#222">{title}</text>
  <text x="{pad_l}" y="{height - 4}" font-size="10" fill="#666">word count per unit (x) · cumulative sum of (x − mean)</text>
  <line x1="{pad_l}" y1="{zero_y:.1f}" x2="{width - pad_r}" y2="{zero_y:.1f}" stroke="#bbb" stroke-dasharray="3 3"/>
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{height - pad_b}" stroke="#888"/>
  <line x1="{pad_l}" y1="{height - pad_b}" x2="{width - pad_r}" y2="{height - pad_b}" stroke="#888"/>
  {''.join(marks)}
  <polyline fill="none" stroke="#1f4e79" stroke-width="2.2" points="{points}"/>
  {''.join(f'<circle cx="{xy(i, v)[0]:.1f}" cy="{xy(i, v)[1]:.1f}" r="3.2" fill="#1f4e79"/>' for i, v in enumerate(series))}
  {''.join(ticks)}
  <text x="8" y="{pad_t + 10}" font-size="10" fill="#666">+S</text>
  <text x="8" y="{height - pad_b}" font-size="10" fill="#666">−S</text>
  <text x="{width - 150}" y="22" font-size="11" fill="#666">mean = {mean([float(v) for v in values]):.2f}</text>
</svg>
"""
    dest.write_text(svg, encoding="utf-8")
    return dest
