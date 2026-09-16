"""Write a standalone HTML walk-through of one document."""

from __future__ import annotations

from html import escape
from pathlib import Path

from scd.features import pairwise_feature_map
from scd.io import reconstruct_authors

PALETTE = (
    "#dbeafe",
    "#fce7f3",
    "#dcfce7",
    "#fef3c7",
    "#e0e7ff",
    "#ffedd5",
)


def render_report(
    units: list[str],
    *,
    truth: list[int] | None = None,
    pred: list[int] | None = None,
    title: str = "Style-change report",
    proba: list[float] | None = None,
) -> str:
    n = len(units)
    if n == 0:
        raise ValueError("no units to render")
    expected = n - 1
    if truth is not None and len(truth) != expected:
        raise ValueError("truth length must be n_units - 1")
    if pred is not None and len(pred) != expected:
        raise ValueError("pred length must be n_units - 1")
    if proba is not None and len(proba) != expected:
        raise ValueError("proba length must be n_units - 1")

    runs = reconstruct_authors(truth if truth is not None else [0] * expected)
    cards = []
    for i, unit in enumerate(units):
        color = PALETTE[(runs[i] - 1) % len(PALETTE)]
        cards.append(
            "<article class='unit' style='background:{color}'>"
            "<header>Sentence {n} · author-run {run}</header>"
            "<p>{text}</p>"
            "</article>".format(
                color=color,
                n=i + 1,
                run=runs[i],
                text=escape(unit),
            )
        )
        if i < expected:
            true_bit = truth[i] if truth is not None else None
            pred_bit = pred[i] if pred is not None else None
            p = proba[i] if proba is not None else None
            pair = pairwise_feature_map(units[i], units[i + 1])
            cues = (
                ("|Δ contraction|", pair["abs_contraction_rate"]),
                ("|Δ first person|", pair["abs_first_person_rate"]),
                ("function-word cosine", pair["fw_cosine"]),
                ("char 3-gram cosine", pair["char_tri_cosine"]),
                ("word Jaccard", pair["jaccard"]),
                ("length ratio", pair["length_ratio"]),
            )
            cue_html = "".join(
                f"<li><span>{escape(name)}</span><strong>{value:.3f}</strong></li>"
                for name, value in cues
            )
            status = []
            if true_bit is not None:
                status.append(f"truth={true_bit}")
            if pred_bit is not None:
                status.append(f"pred={pred_bit}")
            if p is not None:
                status.append(f"p(change)={p:.3f}")
            kind = "boundary"
            if true_bit == 1:
                kind += " change"
            if pred_bit is not None and true_bit is not None:
                kind += " hit" if pred_bit == true_bit else " miss"
            cards.append(
                "<div class='pair {kind}'>"
                "<p class='pair-label'>Pair {a}–{b} · {status}</p>"
                "<ul>{cues}</ul>"
                "</div>".format(
                    kind=kind,
                    a=i + 1,
                    b=i + 2,
                    status=escape(" · ".join(status) or "features only"),
                    cues=cue_html,
                )
            )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{escape(title)}</title>
  <style>
    body {{ font-family: ui-sans-serif, system-ui, sans-serif; margin: 1.5rem auto;
           max-width: 42rem; color: #111827; background: #f8fafc; line-height: 1.45; }}
    h1 {{ font-size: 1.45rem; margin-bottom: 0.4rem; }}
    .note {{ color: #4b5563; font-size: 0.95rem; }}
    .unit {{ border-radius: 0.6rem; padding: 0.85rem 1rem; margin: 0.7rem 0; }}
    .unit header {{ font-size: 0.75rem; letter-spacing: 0.06em; text-transform: uppercase;
                    color: #334155; margin-bottom: 0.35rem; }}
    .unit p {{ margin: 0; font-size: 1.05rem; }}
    .pair {{ border-left: 5px solid #94a3b8; padding: 0.55rem 0.8rem; margin: 0.45rem 0;
             border-radius: 0 0.4rem 0.4rem 0; }}
    .pair.change {{ border-left-color: #b45309; }}
    .pair.hit {{ background: #ecfdf5; }}
    .pair.miss {{ background: #fef2f2; }}
    .pair-label {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
                   font-size: 0.9rem; margin: 0 0 0.4rem; }}
    ul {{ list-style: none; padding: 0; margin: 0;
          display: grid; grid-template-columns: 1fr 1fr; gap: 0.25rem 1.2rem; }}
    li {{ display: flex; justify-content: space-between; gap: 1rem; font-size: 0.92rem; }}
    li span {{ color: #4b5563; }}
  </style>
</head>
<body>
  <h1>{escape(title)}</h1>
  <p class="note">Colours follow reconstructed author runs from the truth vector
  (or a single run if no truth was given). Pair boxes show a few stylometric
  cues from <code>scd.features</code>.</p>
  {''.join(cards)}
</body>
</html>
"""


def write_report(path: str | Path, html: str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path
