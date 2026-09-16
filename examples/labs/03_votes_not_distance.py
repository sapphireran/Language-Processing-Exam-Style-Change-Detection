"""Show that a bundle is not the same object as L2 on z."""

import math

import _paths  # noqa: F401

from isogloss.detect import inspect_hinges
from isogloss.features import extract_many
from isogloss.io import read_problem
from _paths import problem


def l2(marks) -> float:
    return math.sqrt(sum(m.z * m.z for m in marks))


if __name__ == "__main__":
    doc = read_problem(problem(27))
    views = inspect_hinges(extract_many(doc.units))
    print("trap 27 (Flint cider → Flint charcoal)")
    print("If L2 were the rule, a digit wrinkle could win. Votes should not.")
    for view in views:
        print(
            f"  hinge {view.index}: votes={view.votes} "
            f"L2={l2(view.marks):.2f} fires={view.fires} gold={doc.gold[view.index]}"
        )
