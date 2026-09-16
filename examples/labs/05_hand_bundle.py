"""Compute votes for document 19 by hand from the feature table."""

import _paths  # noqa: F401

from isogloss.detect import DEFAULT_K, DEFAULT_RHO, DEFAULT_ZETA, inspect_hinges
from isogloss.features import CHANNELS, extract_many
from isogloss.io import read_problem
from _paths import problem

if __name__ == "__main__":
    doc = read_problem(problem(19))
    rows = extract_many(doc.units)
    views = inspect_hinges(rows)
    print("channels:", ", ".join(CHANNELS))
    for i, row in enumerate(rows):
        d = row.as_dict()
        print(
            f"unit {i}: I={d['i_rate']:.3f} we={d['we_rate']:.3f} "
            f"contr={d['contraction_rate']:.3f} formal={d['formal_rate']:.3f} "
            f"n={d['n_words']:.0f}"
        )
    print(f"zeta={DEFAULT_ZETA} rho={DEFAULT_RHO} k={DEFAULT_K}")
    for view in views:
        marked = [m.name for m in view.marks if m.marked]
        print(f"hinge {view.index}: votes={view.votes} marked={marked} fire={view.fires}")
    print("gold", doc.gold, "pred", [int(v.fires) for v in views])
