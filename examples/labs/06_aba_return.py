"""ABA must fire both seams, not only the first cut."""

import _paths  # noqa: F401

from isogloss.detect import detect_problem
from isogloss.io import read_problem
from _paths import problem

if __name__ == "__main__":
    doc = read_problem(problem(29))
    det = detect_problem(doc)
    print("houses", doc.truth["houses"] if doc.truth else None)
    print("gold", doc.gold)
    print("pred", det.changes)
    for view in det.hinges:
        print(
            f"  hinge {view.index} votes={view.votes} "
            f"reason={view.reason or 'quiet'} "
            f"{', '.join(m.name for m in view.top_channels(3))}"
        )
