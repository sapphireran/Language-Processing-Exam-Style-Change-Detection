"""Plain-text reports for a document or a scored directory."""

from __future__ import annotations

from pathlib import Path

from .detect import Detection, detect_path
from .io import read_problem, read_truth
from .metrics import hinge_macro_f1, score_directory


def document_report(path: str | Path, gold: list[int] | None = None) -> str:
    path = Path(path)
    det = detect_path(path)
    problem = read_problem(path)
    lines = [
        f"# {path.name}",
        f"paragraphs: {len(problem.paragraphs)}",
        f"hinges: {problem.n_hinges}",
        f"penalty: {det.penalty:.3f}",
        f"predicted authors (naive 1+cuts): {det.authors_guess}",
        "",
        "index  split   adjacent  pred  reason",
    ]
    for i in range(problem.n_hinges):
        split = det.split_scores[i] if i < len(det.split_scores) else 0.0
        adj = det.adjacent[i] if i < len(det.adjacent) else 0.0
        pred = det.changes[i]
        reason = det.cut_reason[i] or "-"
        mark = "CHANGE" if pred else "same  "
        lines.append(f"{i:>5}  {split:6.3f}  {adj:8.3f}  {mark}  {reason}")
    if gold is None:
        sibling = path.with_name("truth-" + path.name.replace(".txt", ".json"))
        if not sibling.exists():
            stem = path.name.removeprefix("problem-").removesuffix(".txt")
            prefix = stem.split("-", 1)[0]
            sibling = path.with_name(f"truth-problem-{prefix}.json")
        if sibling.exists():
            gold = read_truth(sibling).changes
    if gold is not None:
        scores = hinge_macro_f1(det.changes, gold)
        lines += [
            "",
            f"gold:     {gold}",
            f"pred:     {det.changes}",
            f"macro-F1: {scores.macro_f1:.3f}",
            f"accuracy: {scores.accuracy:.3f}",
            f"tp/fp/fn/tn: {scores.tp}/{scores.fp}/{scores.fn}/{scores.tn}",
        ]
    lines += ["", "paragraph heads:"]
    for i, para in enumerate(problem.paragraphs):
        head = " ".join(para.split())[:88]
        lines.append(f"  [{i}] {head}…")
    return "\n".join(lines) + "\n"


def directory_report(directory: str | Path) -> str:
    bundle = score_directory(directory)
    overall = bundle["overall"]
    never = bundle["never"]
    always = bundle["always"]
    lines = [
        f"# kerf score  {directory}",
        f"docs:    {bundle['n_docs']}",
        f"hinges:  {bundle['n_hinges']}",
        "",
        "predictor     macro-F1  mean-doc-acc  hinge-acc  f1-change  f1-same",
        (
            f"never-fire    {never.macro_f1:8.3f}  {never.accuracy:12.3f}  "
            f"{never.accuracy:9.3f}  {never.f1_change:9.3f}  {never.f1_same:7.3f}"
        ),
        (
            f"always-fire   {always.macro_f1:8.3f}  {always.accuracy:12.3f}  "
            f"{always.accuracy:9.3f}  {always.f1_change:9.3f}  {always.f1_same:7.3f}"
        ),
        (
            f"kerf          {overall.macro_f1:8.3f}  {bundle['mean_doc_accuracy']:12.3f}  "
            f"{overall.accuracy:9.3f}  {overall.f1_change:9.3f}  {overall.f1_same:7.3f}"
        ),
        "",
        "id                                      gold            pred            f1    acc  reasons",
    ]
    for row in bundle["rows"]:
        gold = "".join(str(x) for x in row["gold"])
        pred = "".join(str(x) for x in row["pred"])
        reasons = ",".join(r or "-" for r in row["reasons"])
        lines.append(
            f"{row['id']:<40} {gold:<15} {pred:<15} {row['macro_f1']:.2f}  {row['accuracy']:.2f}  {reasons}"
        )
    lines += [
        "",
        "Never-fire accuracy is high when most hinges are zeros.",
        "That is why the table leads with macro-F1.",
    ]
    return "\n".join(lines) + "\n"


def feature_table(paragraph: str, top: int = 12) -> str:
    from .features import extract

    vec = extract(paragraph)
    ranked = sorted(vec.as_weighted(), key=lambda t: abs(t[1] * t[2]), reverse=True)
    lines = [
        f"words: {vec.n_words}   sentences: {vec.n_sentences}",
        "name                    value   weight    contrib",
    ]
    for name, value, weight in ranked[:top]:
        lines.append(f"{name:<22} {value:7.4f}  {weight:6.2f}  {value * weight:8.4f}")
    return "\n".join(lines) + "\n"
