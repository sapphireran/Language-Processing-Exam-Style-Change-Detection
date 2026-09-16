#!/usr/bin/env python3
"""Lab 7: topic change is not an author change.

Builds two toys in memory:

1. Same diarist, balcony tomato then a delayed train (gold: no cut).
2. Two voices, both about the balcony tomato (gold: a cut).

A style detector should be quieter on (1) than on (2). A noun detector
wants the opposite.
"""

from __future__ import annotations

from splicefind.detect import detect_text


SAME_AUTHOR = """The balcony tomato has decided to live. I water it from a jar and I eat the fruit over the sink like a person who has not earned a plate. I left seeds on my wrist as evidence.

The train sat outside the station and I ate an apple over my bag like a person who has not earned a platform. I left crumbs on my wrist as evidence.
"""

NEW_AUTHOR = """The balcony tomato has decided to live. I water it from a jar and I eat the fruit over the sink like a person who has not earned a plate.

One may regard the container planting as a modest horticultural trial. Irrigation from a jar is irregular; fruit nevertheless formed. The observation is a result, not a recipe, and it does not generalise beyond this balcony.
"""


def show(title: str, text: str, gold: list[int]) -> float:
    detection = detect_text(text)
    score = detection.boundaries[0].ensemble if detection.boundaries else 0.0
    print(title)
    print(f"  gold={gold}  pred={detection.changes}  ensemble={score:.3f}")
    if detection.boundaries:
        print(f"  {detection.boundaries[0].reasons[-1]}")
    print()
    return score


def main() -> None:
    same = show("1. same author, new topic (should stay calm)", SAME_AUTHOR, [0])
    switched = show("2. new author, same topic (should fire)", NEW_AUTHOR, [1])
    print(f"gap (2 - 1) = {switched - same:.3f}")
    if switched > same:
        print("Direction is right: same-topic author change scored higher.")
    else:
        print("Direction is wrong on this toy: residual topic leakage, talk about it.")


if __name__ == "__main__":
    main()
