"""Lab 06: if we drop the register channel, topic leaks back in."""

from inkfold.corpus import iter_problems
from inkfold.detectors import hinge_scores
from inkfold.distance import blend


def _reblend(problem, weights):
    scores = hinge_scores(problem.units)
    fires = []
    for sc in scores:
        value = blend(sc.channels, weights)
        fires.append(1 if value >= 0.30 else 0)
    return fires


def main() -> None:
    stall = next(p for p in iter_problems() if p.problem_id.endswith("stall-three-topics"))
    kiln = next(p for p in iter_problems() if p.problem_id.endswith("kiln-then-notice"))
    setups = {
        "default (reg+fw)": {
            "register_l1": 0.80,
            "function_cosine_distance": 0.20,
            "char3_distance": 0.0,
            "delta": 0.0,
        },
        "char3 only": {
            "register_l1": 0.0,
            "function_cosine_distance": 0.0,
            "char3_distance": 1.0,
            "delta": 0.0,
        },
    }
    for name, weights in setups.items():
        print(f"## {name}")
        for problem in (kiln, stall):
            pred = _reblend(problem, weights)
            print(f"  {problem.problem_id:36s} gold={problem.truth.changes} pred={pred}")
        print()
    print("This lab applies a raw 0.30 cut with no peak-picking, on purpose.")
    print("Char-3 lights the topic control. Register+fw does not.")


if __name__ == "__main__":
    main()
