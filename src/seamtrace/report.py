"""Plain-text and HTML reports for one document or a whole folder."""

from __future__ import annotations

from html import escape
from pathlib import Path

from .cusum import cusum_scores
from .evaluate import PairMetrics
from .explain import PairExplanation
from .features import FeatureTable
from .pairwise import ScoreBreakdown


def format_metrics(name: str, metrics: PairMetrics) -> str:
    return (
        f"{name}: macro-F1={metrics.macro_f1:.3f}  "
        f"F1-change={metrics.f1_1:.3f}  F1-stay={metrics.f1_0:.3f}  "
        f"acc={metrics.accuracy:.3f}  "
        f"tp={metrics.tp} fp={metrics.fp} fn={metrics.fn} tn={metrics.tn}"
    )


def format_pair_table(
    units: list[str],
    rows: list[ScoreBreakdown],
    explanations: list[PairExplanation],
) -> str:
    lines = [
        f"{'i':>3}  {'gold':>4}  {'pred':>4}  {'score':>6}  {'fw':>5}  {'tri':>5}  {'Δ':>5}  label"
    ]
    for exp, row in zip(explanations, rows):
        gold = "-" if exp.gold is None else str(exp.gold)
        left = _clip(units[exp.index], 42)
        right = _clip(units[exp.index + 1], 42)
        lines.append(
            f"{exp.index:>3}  {gold:>4}  {exp.pred:>4}  {exp.score:6.3f}  "
            f"{row.function_words:5.2f}  {row.trigrams:5.2f}  {row.delta:5.2f}  {exp.label}"
        )
        lines.append(f"     {left}  ||  {right}")
    return "\n".join(lines)


def _clip(text: str, n: int) -> str:
    one = " ".join(text.split())
    return one if len(one) <= n else one[: n - 1] + "…"


def html_report(
    title: str,
    units: list[str],
    table: FeatureTable,
    explanations: list[PairExplanation],
    metrics: PairMetrics | None,
) -> str:
    cusum = cusum_scores(table)
    metric_block = escape(format_metrics("detector", metrics)) if metrics else "unlabelled"
    rows = []
    for exp in explanations:
        klass = exp.label
        gold = "—" if exp.gold is None else str(exp.gold)
        rows.append(
            "<tr class='{klass}'>"
            "<td>{i}</td><td>{gold}</td><td>{pred}</td>"
            "<td>{score:.3f}</td><td>{fw:.2f}</td><td>{tri:.2f}</td>"
            "<td>{delta:.2f}</td><td>{label}</td>"
            "<td>{left}</td><td>{right}</td></tr>".format(
                klass=escape(klass),
                i=exp.index,
                gold=escape(gold),
                pred=exp.pred,
                score=exp.score,
                fw=exp.parts.function_words,
                tri=exp.parts.trigrams,
                delta=exp.parts.delta,
                label=escape(exp.label),
                left=escape(_clip(units[exp.index], 80)),
                right=escape(_clip(units[exp.index + 1], 80)),
            )
        )
    cusum_txt = ", ".join(f"{v:.2f}" for v in cusum) if cusum else "n/a"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escape(title)}</title>
  <style>
    body {{ font-family: Georgia, serif; margin: 2rem auto; max-width: 1100px; color: #222; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 0.92rem; }}
    th, td {{ border: 1px solid #ddd; padding: 0.35rem 0.45rem; vertical-align: top; }}
    th {{ background: #f4f1ea; text-align: left; }}
    tr.genuine_hit {{ background: #e7f6e7; }}
    tr.genuine_stay {{ background: #f7f7f7; }}
    tr.topic_confound {{ background: #fff3cd; }}
    tr.threshold_near_miss, tr.register_only {{ background: #fde2e1; }}
    tr.single_author_drift, tr.short_unit_noise {{ background: #e8eefc; }}
    code, .nums {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .note {{ color: #444; }}
  </style>
</head>
<body>
  <h1>{escape(title)}</h1>
  <p class="note">{metric_block}</p>
  <p class="nums">CUSUM trace: {escape(cusum_txt)}</p>
  <table>
    <thead>
      <tr>
        <th>i</th><th>gold</th><th>pred</th><th>score</th>
        <th>fw</th><th>tri</th><th>delta</th><th>label</th>
        <th>left</th><th>right</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""


def write_html(path: str | Path, html: str) -> None:
    Path(path).write_text(html, encoding="utf-8")
