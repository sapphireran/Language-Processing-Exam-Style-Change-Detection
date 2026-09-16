"""Plain-text and HTML reports for a scored corpus."""

from __future__ import annotations

from html import escape
from pathlib import Path

from .corpus import CorpusItem
from .detectors import DEFAULT_THRESHOLD, DetectorResult, threshold_detect
from .evaluate import BinaryReport, CorpusScores, score_corpus
from .explain import explain_document, format_explanation
from .pairwise import score_unit_hinges


def detect_item(item: CorpusItem, threshold: float = DEFAULT_THRESHOLD) -> DetectorResult:
    hinges = score_unit_hinges(item.problem.units)
    return threshold_detect(hinges, threshold=threshold)


def evaluate_items(
    items: list[CorpusItem],
    threshold: float = DEFAULT_THRESHOLD,
) -> CorpusScores:
    rows = []
    for item in items:
        pred = detect_item(item, threshold=threshold).changes
        rows.append((item.name, item.truth.changes, pred))
    return score_corpus(rows)


def format_corpus_table(
    items: list[CorpusItem],
    scored: CorpusScores,
    threshold: float,
) -> str:
    lines = [
        f"documents={scored.documents} hinges={scored.hinges} cut={threshold:.3f}",
        f"mean macro-F1={scored.mean_macro_f1:.3f}  "
        f"mean accuracy={scored.mean_accuracy:.3f}  "
        f"micro macro-F1={scored.micro.macro_f1:.3f}",
        "",
        f"{'document':<42} {'split':<10} {'gold':<18} {'pred':<18} {'mF1':>6} {'acc':>6}",
    ]
    by_name = {name: report for name, report in scored.per_document}
    for item in items:
        report = by_name[item.name]
        gold = "".join(str(x) for x in item.truth.changes)
        pred = "".join(str(x) for x in report.pred)
        lines.append(
            f"{item.name:<42} {item.split:<10} {gold:<18} {pred:<18} "
            f"{report.macro_f1:6.3f} {report.accuracy:6.3f}"
        )
    return "\n".join(lines)


def write_html_report(
    item: CorpusItem,
    dest: Path,
    threshold: float = DEFAULT_THRESHOLD,
) -> None:
    exp = explain_document(
        item.problem.text,
        threshold=threshold,
        gold=item.truth.changes,
        authors=item.truth.authors,
    )
    rows = []
    for h, pred in zip(exp.hinges, exp.result.changes):
        gold = exp.gold[h.index] if exp.gold else None
        klass = "hold"
        if pred:
            klass = "snap"
        if gold is not None and gold != pred:
            klass = "miss" if gold == 1 else "alarm"
        rows.append(
            "<tr class='{k}'><td>{i}</td><td>{pred}</td><td>{gold}</td>"
            "<td>{blend:.3f}</td><td>{reg:.3f}</td><td>{fw:.3f}</td>"
            "<td>{left}</td><td>{right}</td></tr>".format(
                k=klass,
                i=h.index,
                pred=pred,
                gold="" if gold is None else gold,
                blend=h.blend,
                reg=h.register_gap,
                fw=h.fw_distance,
                left=escape(_clip(h.left)),
                right=escape(_clip(h.right)),
            )
        )
    headline = ""
    if exp.report:
        r = exp.report
        headline = (
            f"macro-F1 {r.macro_f1:.3f} · accuracy {r.accuracy:.3f} · "
            f"change-F1 {r.change.f1:.3f}"
        )
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{escape(item.name)}</title>
<style>
body {{ font-family: Georgia, serif; margin: 2rem auto; max-width: 960px; color: #222; }}
h1 {{ font-size: 1.4rem; }}
.meta {{ color: #555; margin-bottom: 1rem; }}
table {{ border-collapse: collapse; width: 100%; font-size: 0.92rem; }}
th, td {{ border-bottom: 1px solid #ddd; padding: 0.4rem 0.5rem; vertical-align: top; }}
th {{ text-align: left; }}
tr.snap td:nth-child(2) {{ font-weight: bold; }}
tr.miss {{ background: #fde8e8; }}
tr.alarm {{ background: #fff4d6; }}
tr.snap {{ background: #e8f4e8; }}
code {{ font-family: ui-monospace, monospace; }}
</style></head>
<body>
<h1>{escape(item.name)}</h1>
<p class="meta">split=<code>{escape(item.split)}</code> · {escape(headline)} · cut={threshold:.3f}</p>
<p>{escape(item.note)}</p>
<table>
<thead><tr><th>#</th><th>pred</th><th>gold</th><th>blend</th><th>reg</th><th>fw</th><th>left</th><th>right</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody></table>
</body></html>
"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")


def write_walkthrough_markdown(
    item: CorpusItem,
    dest: Path,
    threshold: float = DEFAULT_THRESHOLD,
) -> None:
    exp = explain_document(
        item.problem.text,
        threshold=threshold,
        gold=item.truth.changes,
        authors=item.truth.authors,
    )
    body = [
        f"# Walkthrough: `{item.name}`",
        "",
        f"Split: **{item.split}**. {item.note}",
        "",
        "```",
        format_explanation(exp),
        "```",
        "",
    ]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(body), encoding="utf-8")


def _clip(text: str, width: int = 56) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 3] + "..."


# re-export for type checkers that import BinaryReport via this module
__all__ = [
    "BinaryReport",
    "detect_item",
    "evaluate_items",
    "format_corpus_table",
    "write_html_report",
    "write_walkthrough_markdown",
]
