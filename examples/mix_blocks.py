#!/usr/bin/env python3
"""Build a tiny synthetic document from three voice blocks and run the detector."""

from __future__ import annotations

from stylechange.detector import detect, explain_lines
from stylechange.generate import Block, mix_blocks


def main() -> int:
    text, gold, voices = mix_blocks(
        Block(
            "student",
            (
                "I always forget whether the hidden state is on the tags or the words.",
                "For me the picture that sticks is a chain of tags that then emit observations.",
            ),
        ),
        Block(
            "textbook",
            (
                "A hidden Markov model specifies a joint distribution over label sequences and observations.",
                "The forward algorithm therefore computes the marginal likelihood in linear time.",
            ),
        ),
        Block(
            "notes",
            (
                "HMM: y_t -> y_{t+1}, y_t -> x_t",
                "fwd: α_t(j) = Σ_i α_{t-1}(i) a_ij b_j(x_t)",
            ),
        ),
    )
    detection = detect(text)
    print("gold:  ", gold)
    print("pred:  ", detection.changes)
    print("intend:", voices)
    print("voices:", detection.voices)
    print("match: ", gold == detection.changes)
    print()
    print("\n".join(explain_lines(detection)))
    return 0 if gold == detection.changes else 1


if __name__ == "__main__":
    raise SystemExit(main())
