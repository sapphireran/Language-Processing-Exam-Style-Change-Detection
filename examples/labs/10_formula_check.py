"""Check the formula card against a tiny two-unit toy."""

import _paths  # noqa: F401

from isogloss.detect import DEFAULT_K, DEFAULT_ZETA, inspect_hinges
from isogloss.evaluate import confusion, macro_f1
from isogloss.features import extract


SKIFF = (
    "I don't trust a wet knot. I'll pull it and I'll tie it again. "
    "So I keep my knife open."
)
ROLL = (
    "The committee shall receive the log. It was resolved that the "
    "clerk must file a second copy. Members shall not leave the loft."
)


if __name__ == "__main__":
    rows = [extract(SKIFF), extract(ROLL)]
    views = inspect_hinges(rows)
    assert len(views) == 1
    view = views[0]
    print(f"votes={view.votes} k={DEFAULT_K} zeta={DEFAULT_ZETA} fire={view.fires}")
    print("marked", [m.name for m in view.marks if m.marked])
    gold = [1]
    pred = [1 if view.fires else 0]
    table = confusion(gold, pred)
    print(f"macro-F1={macro_f1(gold, pred):.3f} acc={table.accuracy:.3f}")
    if not view.fires:
        raise SystemExit("toy Skiff→Roll must fire; the houses are not distinct enough")
