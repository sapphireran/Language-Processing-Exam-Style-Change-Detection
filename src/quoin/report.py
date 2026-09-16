"""Text reports for the example bank."""

from __future__ import annotations

from .corpus import Corpus
from .detectors import QuoinDetector, always_fire, never_fire
from .evaluate import DocumentScore, corpus_report, safe_f1


def score_corpus(corpus: Corpus, detector: QuoinDetector | None = None) -> list[DocumentScore]:
    detector = detector or QuoinDetector()
    rows: list[DocumentScore] = []
    for item in corpus:
        pred = detector.predict(item.problem.paragraphs)
        rows.append(DocumentScore.from_pair(item.name, item.truth.changes, pred))
    return rows


def render_table(rows: list[DocumentScore], bands: dict[str, str] | None = None) -> str:
    bands = bands or {}
    header = (
        f"{'document':<44} {'band':<10} {'F1':>6} {'P':>6} {'R':>6} "
        f"{'acc':>6} {'gold':>5} {'pred':>5}"
    )
    lines = [header, "-" * len(header)]
    for row in rows:
        band = bands.get(row.name, "")
        lines.append(
            f"{row.name:<44} {band:<10} {row.f1:6.3f} {row.precision:6.3f} "
            f"{row.recall:6.3f} {row.accuracy:6.3f} {row.n_true_changes:5d} {row.n_pred_changes:5d}"
        )
    summary = corpus_report(rows)
    lines.append("-" * len(header))
    lines.append(
        f"{'MACRO / MICRO':<44} {'':<10} {summary['macro_f1']:6.3f} "
        f"{'':>6} {'':>6} {summary['mean_accuracy']:6.3f} "
        f"{int(summary['n_true_changes']):5d} {int(summary['n_pred_changes']):5d}"
    )
    lines.append(f"micro-F1 {summary['micro_f1']:.3f}   docs {int(summary['n_docs'])}   "
                 f"boundaries {int(summary['n_boundaries'])}")
    return "\n".join(lines)


def render_baselines(corpus: Corpus, detector: QuoinDetector | None = None) -> str:
    detector = detector or QuoinDetector()
    quoin_rows = score_corpus(corpus, detector)
    never_rows = []
    always_rows = []
    for item in corpus:
        n = item.problem.n_boundaries
        never_rows.append(DocumentScore.from_pair(item.name, item.truth.changes, never_fire(n)))
        always_rows.append(DocumentScore.from_pair(item.name, item.truth.changes, always_fire(n)))
    quoin = corpus_report(quoin_rows)
    never = corpus_report(never_rows)
    always = corpus_report(always_rows)
    lines = [
        "Baseline trap (same documents, three predictors)",
        "",
        f"{'predictor':<22} {'macro-F1':>9} {'micro-F1':>9} {'mean acc':>9}",
        "-" * 52,
        f"{'never-fire (all 0)':<22} {never['macro_f1']:9.3f} {never['micro_f1']:9.3f} {never['mean_accuracy']:9.3f}",
        f"{'always-fire (all 1)':<22} {always['macro_f1']:9.3f} {always['micro_f1']:9.3f} {always['mean_accuracy']:9.3f}",
        f"{'quoin':<22} {quoin['macro_f1']:9.3f} {quoin['micro_f1']:9.3f} {quoin['mean_accuracy']:9.3f}",
        "",
        "Accuracy of never-fire is high because most boundaries are 0.",
        "That is why the exam (and PAN) uses F1.",
    ]
    return "\n".join(lines)


def render_markdown(corpus: Corpus, detector: QuoinDetector | None = None) -> str:
    detector = detector or QuoinDetector()
    bands = {item.name: item.band for item in corpus}
    rows = score_corpus(corpus, detector)
    summary = corpus_report(rows)
    lines = [
        "# Quoin live results",
        "",
        f"Threshold `{detector.threshold}`. Weights: NCD `{detector.w_ncd}`, "
        f"char `{detector.w_char}`, function `{detector.w_function}`, "
        f"shape `{detector.w_shape}`.",
        "",
        f"- documents: {int(summary['n_docs'])}",
        f"- boundaries: {int(summary['n_boundaries'])}",
        f"- true changes: {int(summary['n_true_changes'])}",
        f"- predicted changes: {int(summary['n_pred_changes'])}",
        f"- macro-F1: **{summary['macro_f1']:.3f}**",
        f"- micro-F1: **{summary['micro_f1']:.3f}**",
        f"- mean accuracy: {summary['mean_accuracy']:.3f}",
        "",
        "| document | band | F1 | P | R | acc | gold | pred |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| `{row.name}` | {bands.get(row.name, '')} | {row.f1:.3f} | "
            f"{row.precision:.3f} | {row.recall:.3f} | {row.accuracy:.3f} | "
            f"{row.n_true_changes} | {row.n_pred_changes} |"
        )
    lines.append("")
    lines.append("## Per-band macro-F1")
    lines.append("")
    lines.append("| band | docs | macro-F1 |")
    lines.append("| --- | ---: | ---: |")
    for band in ("control", "easy", "medium", "hard", "trap", "return", "collage"):
        subset = [row for row in rows if bands.get(row.name) == band]
        if not subset:
            continue
        from .evaluate import macro_f1

        score = macro_f1([(row.gold, row.pred) for row in subset])
        lines.append(f"| {band} | {len(subset)} | {score:.3f} |")
    lines.append("")
    lines.append(render_baselines(corpus, detector))
    lines.append("")
    return "\n".join(lines)
