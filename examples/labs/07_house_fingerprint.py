"""Top saw-axis contributions for one paragraph of each house."""

from __future__ import annotations

from examples.corpus.bank import DOCUMENTS
from kerf.features import extract

SAMPLES = {
    "caliper": ("01-caliper-stilling-control", 0),
    "placard": ("02-placard-cinema-control", 0),
    "pocket": ("03-pocket-icehouse-control", 0),
    "statute": ("04-statute-signal-control", 0),
    "seminar": ("10-seminar-grain-then-bench-bells", 0),
    "bench": ("07-bench-box-then-seminar-compass", 0),
}


def main() -> None:
    by_id = {d.id: d for d in DOCUMENTS}
    for house, (doc_id, idx) in SAMPLES.items():
        para = by_id[doc_id].paragraphs[idx]
        vec = extract(para)
        ranked = sorted(
            zip(vec.saw_names(), vec.saw_values()),
            key=lambda t: -abs(t[1]),
        )
        print(f"# {house}  ({doc_id} [{idx}])")
        for name, value in ranked[:6]:
            print(f"  {name:<16} {value:6.3f}")
        print()


if __name__ == "__main__":
    main()
