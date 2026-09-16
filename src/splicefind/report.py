"""Plain-text and HTML reports for a single detection."""

from __future__ import annotations

from html import escape
from pathlib import Path

from .cusum import ascii_sparkline, paragraph_feature_trace
from .detect import Detection
from .evaluate import DocumentScore
from .features import DocumentFeatures, named_diffs


def text_report(
    features: DocumentFeatures,
    detection: Detection,
    score: DocumentScore | None = None,
    title: str = "style-change report",
) -> str:
    lines = [title, "=" * len(title), ""]
    lines.append(f"paragraphs: {len(features.paragraphs)}")
    lines.append(f"method: {detection.method}  threshold: {detection.threshold:.2f}")
    lines.append(f"predicted changes: {detection.changes}")
    if score is not None:
        lines.append(
            f"F1={score.f1:.3f}  P={score.precision:.3f}  "
            f"R={score.recall:.3f}  Acc={score.accuracy:.3f}"
        )
    lines.append("")
    trace = paragraph_feature_trace(features.vectors, "avg_sent_len")
    lines.append("CUSUM of average sentence length: " + ascii_sparkline(trace.cusum))
    lines.append("")
    for paragraph_i, paragraph in enumerate(features.paragraphs, start=1):
        vector = features.vectors[paragraph_i - 1]
        lines.append(f"[P{paragraph_i}] words={vector.n_words}  sents={vector.n_sents}")
        lines.append("    " + " ".join(paragraph.split()))
        lines.append(
            "    avg_sent={avg_sent_len:.1f}  ttr={type_token_ratio:.2f}  "
            "I/we={first_person_rate:.2f}  you={second_person_rate:.2f}  "
            "contr={contraction_rate:.2f}".format(**vector.scalars)
        )
        lines.append("")
        if paragraph_i <= len(detection.boundaries):
            boundary = detection.boundaries[paragraph_i - 1]
            flag = "CHANGE" if boundary.decision else "same  "
            lines.append(
                f"    -- {flag}  ensemble={boundary.ensemble:.3f}  "
                f"delta={boundary.delta:.3f}  ngram={boundary.ngram_distance:.3f}"
            )
            top = named_diffs(
                features.vectors[paragraph_i - 1],
                features.vectors[paragraph_i],
            )[:4]
            lines.append(
                "    top scalar gaps: "
                + ", ".join(f"{name}={gap:.3f}" for name, gap in top)
            )
            lines.append("")
    return "\n".join(lines)


def html_report(
    features: DocumentFeatures,
    detection: Detection,
    score: DocumentScore | None = None,
    title: str = "style-change report",
) -> str:
    rows = []
    for i, paragraph in enumerate(features.paragraphs):
        vector = features.vectors[i]
        rows.append(
            "<section class='para'>"
            f"<h2>Paragraph {i + 1}</h2>"
            f"<p>{escape(paragraph)}</p>"
            "<ul>"
            f"<li>words {vector.n_words}, sentences {vector.n_sents}</li>"
            f"<li>avg sentence length {vector.scalars['avg_sent_len']:.1f}</li>"
            f"<li>first person {vector.scalars['first_person_rate']:.3f}, "
            f"contractions {vector.scalars['contraction_rate']:.3f}</li>"
            "</ul>"
            "</section>"
        )
        if i < len(detection.boundaries):
            boundary = detection.boundaries[i]
            klass = "cut" if boundary.decision else "hold"
            label = "style change" if boundary.decision else "same author"
            rows.append(
                f"<div class='{klass}'><strong>{escape(label)}</strong> "
                f"ensemble {boundary.ensemble:.3f}, Delta {boundary.delta:.3f}, "
                f"3-gram {boundary.ngram_distance:.3f}</div>"
            )
    metrics = ""
    if score is not None:
        metrics = (
            f"<p>F1 {score.f1:.3f} · precision {score.precision:.3f} · "
            f"recall {score.recall:.3f} · accuracy {score.accuracy:.3f}</p>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{escape(title)}</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 760px; margin: 2rem auto; line-height: 1.5; }}
    .cut {{ background: #f8d7da; padding: 0.4rem 0.7rem; margin: 0.6rem 0; }}
    .hold {{ background: #d1e7dd; padding: 0.4rem 0.7rem; margin: 0.6rem 0; }}
    .para {{ border-left: 3px solid #333; padding-left: 1rem; }}
    code {{ font-size: 0.95em; }}
  </style>
</head>
<body>
  <h1>{escape(title)}</h1>
  <p>method <code>{escape(detection.method)}</code>, threshold {detection.threshold:.2f}</p>
  {metrics}
  {''.join(rows)}
</body>
</html>
"""


def write_html(path: Path | str, html: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
