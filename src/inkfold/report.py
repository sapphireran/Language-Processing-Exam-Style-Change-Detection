"""Plain-text and HTML scoreboards for the teaching corpus."""

from __future__ import annotations

from pathlib import Path

from .evaluate import BinaryScores, DocumentScore, FolderScore
from .explain import HingeExplain, format_explain
from .io import Problem


def format_binary(label: str, s: BinaryScores) -> str:
    return (
        f"{label:16s}  acc={s.accuracy:.3f}  macroF1={s.macro_f1:.3f}  "
        f"posF1={s.f1_pos:.3f}  n={s.support}  "
        f"tp={s.tp} fp={s.fp} tn={s.tn} fn={s.fn}"
    )


def format_scoreboard(folder: FolderScore) -> str:
    lines = ["# inkfold scoreboard", ""]
    lines.append(format_binary("overall", folder.overall))
    lines.append(format_binary("never-fire", folder.never_baseline()))
    lines.append(f"{'mean macro-F1':16s}  {folder.mean_macro_f1():.3f}")
    lines.append("")
    lines.append("## by site")
    for site, scores in folder.by_site().items():
        lines.append(format_binary(site, scores))
    lines.append("")
    lines.append("## per document")
    lines.append(
        f"{'id':36s} {'site':10s} {'macroF1':>8s} {'exact':>6s} {'auth':>6s} {'err':>22s}"
    )
    for row in folder.rows:
        lines.append(
            f"{row.problem_id:36s} {row.site:10s} {row.scores.macro_f1:8.3f} "
            f"{'yes' if row.exact_boundaries else 'no':>6s} "
            f"{'yes' if row.author_ok else 'no':>6s} "
            f"{(row.expected_error or '—'):>22s}"
        )
    return "\n".join(lines) + "\n"


def html_report(problem: Problem, rows: list[HingeExplain], doc: DocumentScore) -> str:
    body_rows = []
    for unit_i, unit in enumerate(problem.units, start=1):
        body_rows.append(
            f"<tr class='unit'><td>{unit_i}</td><td colspan='4'>{_esc(unit)}</td></tr>"
        )
        cut = next((r for r in rows if r.index == unit_i), None)
        if cut is None:
            continue
        klass = "fold" if cut.predicted else "seam"
        if cut.gold is not None and cut.predicted != cut.gold:
            klass += " miss" if cut.gold == 1 else " alarm"
        body_rows.append(
            f"<tr class='{klass}'><td>cut {cut.index}</td>"
            f"<td>{cut.score:.3f}</td><td>pred {cut.predicted} / gold {cut.gold}</td>"
            f"<td>{_esc(cut.verdict)}</td>"
            f"<td>{_esc('; '.join(cut.drivers))}</td></tr>"
        )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{_esc(problem.problem_id)}</title>
<style>
body {{ font-family: Georgia, serif; max-width: 52rem; margin: 2rem auto; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border-top: 1px solid #ccc; padding: 0.4rem 0.5rem; vertical-align: top; }}
tr.fold td {{ background: #f4e1c8; }}
tr.seam td {{ background: #eef2e8; }}
tr.miss td {{ background: #f3d6d6; }}
tr.alarm td {{ background: #f7e7a8; }}
.meta {{ color: #444; }}
</style></head><body>
<h1>{_esc(problem.problem_id)}</h1>
<p class="meta">{_esc(problem.truth.title)} · site={_esc(problem.truth.site)} ·
macroF1={doc.scores.macro_f1:.3f} · authors gold {doc.gold_authors} pred {doc.pred_authors}</p>
<p>{_esc(problem.truth.notes)}</p>
<table>
<tr><th>where</th><th>score</th><th>labels</th><th>verdict</th><th>drivers</th></tr>
{''.join(body_rows)}
</table>
</body></html>
"""


def write_html_reports(out_dir: Path, items: list[tuple[Problem, list[HingeExplain], DocumentScore]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    index = ["<html><body><h1>inkfold reports</h1><ul>"]
    for problem, rows, doc in items:
        path = out_dir / f"{problem.problem_id}.html"
        path.write_text(html_report(problem, rows, doc), encoding="utf-8")
        index.append(
            f"<li><a href='{path.name}'>{problem.problem_id}</a> "
            f"({problem.truth.site}, F1={doc.scores.macro_f1:.2f})</li>"
        )
    index.append("</ul></body></html>")
    (out_dir / "index.html").write_text("\n".join(index), encoding="utf-8")


def write_markdown_explain(path: Path, problem: Problem, rows: list[HingeExplain]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_explain(problem, rows), encoding="utf-8")


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
