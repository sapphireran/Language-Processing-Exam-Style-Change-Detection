#!/usr/bin/env python3
"""Lab 0: can you see the paragraphs the scorer will see?"""

from __future__ import annotations

from _paths import CORPUS, require_corpus
from splicefind.io import load_collection


def main() -> None:
    require_corpus()
    collection = load_collection(CORPUS)
    print(f"{'id':<28} paras  bounds  gold  authors  difficulty")
    print("-" * 78)
    for problem, truth in collection.pairs():
        paras = problem.paragraphs
        gold = "" if truth is None else str(truth.changes)
        authors = "" if truth is None else str(truth.authors)
        difficulty = "" if truth is None else (truth.difficulty or "")
        print(
            f"{problem.problem_id:<28} {len(paras):5}  {problem.n_boundaries:6}  "
            f"{gold:<18} {authors:<8} {difficulty}"
        )
        if truth is not None and len(truth.changes) != problem.n_boundaries:
            raise SystemExit(
                f"truth length {len(truth.changes)} != {problem.n_boundaries} "
                f"for {problem.problem_id}"
            )
    print()
    print(f"{len(collection)} documents. Gold length matches paragraph pairs.")


if __name__ == "__main__":
    main()
