#!/usr/bin/env python3
"""Lab 10: write text/HTML walkthroughs for every corpus document."""

from __future__ import annotations

from _paths import CORPUS, REPORTS, require_corpus
from splicefind.detect import detect_text
from splicefind.evaluate import score_document
from splicefind.features import extract_document
from splicefind.io import load_collection
from splicefind.report import html_report, text_report, write_html


def main() -> None:
    require_corpus()
    REPORTS.mkdir(parents=True, exist_ok=True)
    collection = load_collection(CORPUS)
    cards = []
    for problem, truth in collection.pairs():
        features = extract_document(problem.text)
        detection = detect_text(problem.text)
        score = None
        title = problem.problem_id
        if truth is not None:
            score = score_document(truth.changes, detection.changes, problem.problem_id)
            title = truth.title or problem.problem_id
        text = text_report(features, detection, score, title=title)
        (REPORTS / f"problem-{problem.problem_id}.txt").write_text(text + "\n", encoding="utf-8")
        html = html_report(features, detection, score, title=title)
        html_path = REPORTS / f"problem-{problem.problem_id}.html"
        write_html(html_path, html)
        f1 = "" if score is None else f"{score.f1:.3f}"
        cards.append((problem.problem_id, title, f1))
        print(f"wrote {html_path.name}")
    index = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>corpus reports</title></head><body>",
        "<h1>Personal corpus reports</h1><ul>",
    ]
    for pid, title, f1 in cards:
        index.append(f"<li><a href='problem-{pid}.html'>{title}</a> F1 {f1}</li>")
    index.append("</ul></body></html>")
    (REPORTS / "index.html").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"index -> {REPORTS / 'index.html'}")


if __name__ == "__main__":
    main()
