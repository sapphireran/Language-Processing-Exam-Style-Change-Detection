"""A trap must stay quiet. An easy join must not."""

import _paths  # noqa: F401

from isogloss.detect import detect_problem
from isogloss.io import read_problem
from _paths import problem


def show(ident: int) -> None:
    doc = read_problem(problem(ident))
    det = detect_problem(doc)
    print(f"problem-{ident:02d} gold={doc.gold} pred={det.changes}")
    for view in det.hinges:
        tops = ", ".join(f"{m.name}={m.z:+.2f}" for m in view.top_channels(3))
        print(f"  hinge {view.index} votes={view.votes} {tops}")


if __name__ == "__main__":
    print("easy 07 (Skiff → Roll)")
    show(7)
    print("trap 25 (Skiff eel → Skiff hop)")
    show(25)
