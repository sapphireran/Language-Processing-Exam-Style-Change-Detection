"""Plain-text and HTML reports for a predicted document."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Sequence

from .evaluate import score_pairs
from .features import FEATURE_NAMES, as_dict, extract_document, pairwise_euclidean, zscore_rows


def pair_table(sentences: list[str], gold: Sequence[int] | None, pred: Sequence[int]) -> str:
    lines = ["idx  gold pred  sent_i → sent_j", "-" * 72]
    n = len(sentences)
    for i in range(n - 1):
        g = "-" if gold is None else str(gold[i])
        p = str(pred[i])
        left = _clip(sentences[i], 28)
        right = _clip(sentences[i + 1], 28)
        mark = "  " if gold is None or gold[i] == pred[i] else " !"
        lines.append(f"{i:>3} {g:>5} {p:>4}{mark} {left} → {right}")
    return "\n".join(lines)


def _clip(text: str, width: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 1] + "…"


def explain_text(
    sentences: list[str],
    *,
    gold: Sequence[int] | None = None,
    pred: Sequence[int] | None = None,
    pair_limit: int | None = None,
    top_features: int = 6,
) -> str:
    matrix = extract_document(sentences)
    z = zscore_rows(matrix) if len(matrix) else matrix
    distances = pairwise_euclidean(z) if len(z) > 1 else []
    chunks: list[str] = []
    chunks.append(f"sentences: {len(sentences)}   pairs: {max(0, len(sentences) - 1)}")
    if gold is not None and pred is not None and len(gold) == len(pred):
        scores = score_pairs(gold, pred)
        chunks.append(
            f"document macro-F1: {scores['macro_f1']:.3f}   "
            f"acc: {scores['accuracy']:.3f}   f1_1: {scores['f1_1']:.3f}"
        )
    chunks.append("")
    limit = len(sentences) - 1 if pair_limit is None else min(pair_limit, len(sentences) - 1)
    for i in range(max(0, limit)):
        g = None if gold is None else gold[i]
        p = None if pred is None else pred[i]
        header = f"pair {i}  (sentence {i} → {i + 1})"
        if g is not None or p is not None:
            header += f"   gold={g} pred={p}"
        if i < len(distances):
            header += f"   z-euclid={distances[i]:.3f}"
        chunks.append(header)
        chunks.append(f"  S{i}: {sentences[i]}")
        chunks.append(f"  S{i+1}: {sentences[i + 1]}")
        if len(matrix) > i + 1:
            delta = abs(matrix[i] - matrix[i + 1])
            ranked = sorted(zip(FEATURE_NAMES, delta.tolist()), key=lambda item: item[1], reverse=True)
            chunks.append("  largest |Δ| features:")
            for name, value in ranked[:top_features]:
                left = as_dict(matrix[i])[name]
                right = as_dict(matrix[i + 1])[name]
                chunks.append(f"    {name:22} {left:8.3f} → {right:8.3f}   |Δ|={value:.3f}")
        chunks.append("")
    return "\n".join(chunks).rstrip() + "\n"


def render_html(
    title: str,
    documents: list[dict],
) -> str:
    """`documents` items: pid, sentences, gold, pred, notes."""
    cards = []
    for doc in documents:
        sentences: list[str] = doc["sentences"]
        gold = doc.get("gold")
        pred = doc.get("pred") or [0] * max(0, len(sentences) - 1)
        spans = []
        for i, sentence in enumerate(sentences):
            after = pred[i] if i < len(pred) else 0
            gold_after = gold[i] if gold is not None and i < len(gold) else None
            cls = "sent"
            if i > 0:
                prev = pred[i - 1]
                if prev:
                    cls += " after-pred-change"
            spans.append(f'<span class="{cls}">{html.escape(sentence)}</span>')
            if i < len(pred):
                boundary_cls = "boundary"
                if after:
                    boundary_cls += " pred-change"
                if gold_after == 1:
                    boundary_cls += " gold-change"
                if gold_after is not None and after != gold_after:
                    boundary_cls += " mismatch"
                label = "change" if after else "same"
                gold_txt = "" if gold_after is None else f" gold={gold_after}"
                spans.append(
                    f'<span class="{boundary_cls}" title="pair {i} pred={after}{gold_txt}">'
                    f" ¶{label} </span>"
                )
        score_txt = ""
        if gold is not None and len(gold) == len(pred):
            scores = score_pairs(gold, pred)
            score_txt = (
                f'<p class="meta">macro-F1 {scores["macro_f1"]:.3f} · '
                f'acc {scores["accuracy"]:.3f} · f1_change {scores["f1_1"]:.3f}</p>'
            )
        notes = html.escape(str(doc.get("notes") or ""))
        cards.append(
            f'<article class="card"><h2>problem-{html.escape(str(doc["pid"]))}</h2>'
            f"{score_txt}<p class='notes'>{notes}</p>"
            f'<p class="body">{" ".join(spans)}</p></article>'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Georgia, serif; margin: 2rem auto; max-width: 880px; color: #1b1b1b; }}
    h1 {{ font-size: 1.6rem; }}
    .legend span {{ display: inline-block; margin-right: 1rem; font-size: 0.9rem; }}
    .card {{ border-top: 1px solid #ccc; padding: 1rem 0 1.4rem; }}
    .meta, .notes {{ color: #444; font-size: 0.95rem; }}
    .sent {{ line-height: 1.55; }}
    .boundary {{ font-family: ui-monospace, monospace; font-size: 0.75rem;
                 color: #666; padding: 0 0.2rem; }}
    .boundary.pred-change {{ color: #7a1f1f; background: #f8d0d0; }}
    .boundary.gold-change {{ box-shadow: inset 0 -2px 0 #1f4d7a; }}
    .boundary.mismatch {{ outline: 1px dashed #b36b00; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p class="legend">
    <span>Red pill = predicted change</span>
    <span>Blue underline = gold change</span>
    <span>Dashed outline = disagreement</span>
  </p>
  {"".join(cards)}
</body>
</html>
"""


def write_html(path: str | Path, title: str, documents: list[dict]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_html(title, documents), encoding="utf-8")
    return path
