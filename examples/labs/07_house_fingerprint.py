"""Mean closed-class rates for each house, to see the atlas before a hinge."""

from collections import defaultdict

import _paths  # noqa: F401

from isogloss.features import extract
from examples.corpus.bank import DOCUMENTS
from _paths import CORPUS  # noqa: F401


KEYS = (
    "i_rate",
    "we_rate",
    "you_rate",
    "contraction_rate",
    "deontic_rate",
    "hedge_rate",
    "formal_rate",
    "digit_rate",
)


if __name__ == "__main__":
    buckets: dict[str, list] = defaultdict(list)
    for doc in DOCUMENTS:
        for block in doc["blocks"]:
            buckets[block["house"]].append(extract(block["text"]))
    header = f"{'house':<8} " + " ".join(f"{k[:7]:>8}" for k in KEYS) + f"{'n':>5}"
    print(header)
    for house in ("skiff", "roll", "twine", "vellum", "flint", "brine"):
        rows = buckets[house]
        n = len(rows)
        means = []
        for key in KEYS:
            means.append(sum(getattr(r, key) for r in rows) / n)
        cells = " ".join(f"{v:8.3f}" for v in means)
        print(f"{house:<8} {cells}{n:5d}")
