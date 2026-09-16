#!/usr/bin/env python3
"""Write HTML walkthroughs for every bundled document."""

from __future__ import annotations

from _paths import DOC_DIR, REPORT_DIR, TRUTH_DIR

from scdkit.detect import explain_document
from scdkit.evaluate import evaluate_collection
from scdkit.io import iter_collection
from scdkit.report import render_collection_html, render_document_html, write_html


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    for path, text, truth in iter_collection(DOC_DIR, TRUTH_DIR):
        detection = explain_document(text)
        dest = REPORT_DIR / f"{path.stem}.html"
        write_html(
            dest,
            render_document_html(
                detection,
                title=truth.title or path.stem,
                gold=list(truth.changes),
            ),
        )
        print(dest)
    score = evaluate_collection(DOC_DIR, TRUTH_DIR)
    index = REPORT_DIR / "index.html"
    write_html(index, render_collection_html(score, title="Bundled exam collection"))
    print(index)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
