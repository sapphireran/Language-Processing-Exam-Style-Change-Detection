"""Self-contained HTML reports for a detected document."""

from __future__ import annotations

import html
from pathlib import Path

from .cusum import formality_cusum, sentence_length_cusum, svg_polyline, word_length_cusum
from .detect import Detection
from .evaluate import BinaryScore, CollectionScore, binary_scores


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _bar(value: float, ceiling: float, color: str) -> str:
    width = max(0.0, min(100.0, 100.0 * value / ceiling if ceiling else 0.0))
    return (
        f'<div class="bar"><span style="width:{width:.1f}%;background:{color}"></span>'
        f'<em>{value:.2f}</em></div>'
    )


def render_document_html(
    detection: Detection,
    title: str = "Style-change report",
    gold: list[int] | None = None,
) -> str:
    score_html = ""
    if gold is not None:
        sc = binary_scores(gold, detection.changes)
        score_html = (
            f'<p class="score">Gold {gold} · Pred {list(detection.changes)} · '
            f"P {sc.precision:.2f} · R {sc.recall:.2f} · F1 {sc.f1:.2f}</p>"
        )
    blocks = []
    for i, para in enumerate(detection.paragraphs):
        feat = detection.features[i]
        changed_before = i > 0 and detection.changes[i - 1] == 1
        cls = "para change" if changed_before else "para"
        badge = " style change ↑" if changed_before else ""
        blocks.append(
            f'<section class="{cls}">'
            f"<header>P{i + 1}{badge} · {feat.n_words} words · "
            f"sent {feat.mean_sent_len:.1f} · formality {feat.formality:.2f} · "
            f"contr {feat.contraction_rate:.2f}</header>"
            f"<p>{_esc(para)}</p></section>"
        )
    rows = []
    for pair in detection.pairs:
        mark = "YES" if pair.change else "no"
        rows.append(
            "<tr>"
            f"<td>{pair.index + 1}→{pair.index + 2}</td>"
            f"<td class='{'hit' if pair.change else 'miss'}'>{mark}</td>"
            f"<td>{_bar(pair.formality, 1.2, '#4a7c3a')}</td>"
            f"<td>{_bar(pair.register, 1.2, '#2c6e8a')}</td>"
            f"<td>{_bar(pair.person, 2.0, '#6b4c9a')}</td>"
            f"<td>{_bar(pair.contraction, 0.2, '#8a4b2c')}</td>"
            f"<td>{_bar(pair.char, 1.0, '#8a6a2c')}</td>"
            f"<td>{_bar(pair.topic, 1.0, '#666')}</td>"
            f"<td>{_esc('; '.join(pair.reasons) or '—')}</td>"
            "</tr>"
        )
    figures = "".join(
        svg_polyline(series)
        for series in (
            word_length_cusum(detection.features),
            sentence_length_cusum(detection.features),
            formality_cusum(detection.features),
        )
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{_esc(title)}</title>
<style>
body {{ font: 16px/1.45 Georgia, serif; margin: 2rem auto; max-width: 980px; color: #222; }}
h1,h2 {{ font-family: Palatino, Georgia, serif; }}
.para {{ border: 1px solid #ddd4c4; padding: 0.8rem 1rem; margin: 0.7rem 0; background: #fffdf8; }}
.para.change {{ border-left: 6px solid #a33; background: #fff6f2; }}
.para header {{ font: 12px/1.3 Menlo, Consolas, monospace; color: #555; margin-bottom: 0.4rem; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
th, td {{ border-bottom: 1px solid #eadfcf; padding: 0.35rem 0.4rem; vertical-align: middle; }}
th {{ text-align: left; font-family: Menlo, Consolas, monospace; }}
.hit {{ color: #a33; font-weight: 700; }}
.miss {{ color: #888; }}
.bar {{ position: relative; height: 14px; background: #f0e8dc; min-width: 70px; }}
.bar span {{ display: block; height: 100%; }}
.bar em {{ position: absolute; inset: 0; font: 11px Menlo, Consolas, monospace; text-align: center; }}
.score {{ background: #eef5ea; padding: 0.6rem 0.8rem; }}
.figs svg {{ margin: 0.4rem 0.4rem 0.4rem 0; }}
.note {{ color: #555; font-size: 0.95rem; }}
</style>
</head>
<body>
<h1>{_esc(title)}</h1>
<p class="note">Personal exam lab report · method <code>{_esc(detection.method)}</code> ·
{len(detection.paragraphs)} paragraphs · changes {list(detection.changes)}</p>
{score_html}
<h2>Paragraphs</h2>
{''.join(blocks)}
<h2>Adjacent channels</h2>
<table>
<thead><tr><th>pair</th><th>Δ?</th><th>formality</th><th>register</th><th>person</th><th>contr</th><th>char3</th><th>topic</th><th>votes</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
<h2>CUSUM paths</h2>
<div class="figs">{figures}</div>
</body>
</html>
"""


def render_collection_html(score: CollectionScore, title: str = "Collection score") -> str:
    rows = []
    for doc in score.documents:
        ok = "ok" if doc.gold == doc.pred else "diff"
        rows.append(
            "<tr>"
            f"<td>{_esc(doc.name)}</td>"
            f"<td>{''.join(str(x) for x in doc.gold)}</td>"
            f"<td>{''.join(str(x) for x in doc.pred)}</td>"
            f"<td>{doc.score.f1:.2f}</td>"
            f"<td class='{ok}'>{ok}</td>"
            "</tr>"
        )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>{_esc(title)}</title>
<style>
body {{ font: 16px/1.45 Georgia, serif; margin: 2rem auto; max-width: 860px; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border-bottom: 1px solid #ddd; padding: 0.35rem 0.5rem; text-align: left; }}
.diff {{ color: #a33; }} .ok {{ color: #2a6; }}
</style></head><body>
<h1>{_esc(title)}</h1>
<p>macro-F1 {score.macro_f1:.3f} · micro-F1 {score.micro.f1:.3f}</p>
<table><thead><tr><th>document</th><th>gold</th><th>pred</th><th>F1</th><th></th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
</body></html>
"""


def write_html(path: str | Path, markup: str) -> Path:
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(markup, encoding="utf-8")
    return dest
