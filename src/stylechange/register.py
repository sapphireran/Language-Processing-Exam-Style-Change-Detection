"""Low-dimensional register axes used by the change-point detector.

Raw cosine over a 30-D stylometric vector is a poor sentence-level metric:
almost every pair of short sentences looks dissimilar. These three axes are
what the example documents actually vary on.

* **personal** — first person, contractions, hedges, informal lexis, questions
* **academic** — connectives, long Latinate words, function-word density
* **telegram** — punctuation, digits, colons, missing function words
"""

from __future__ import annotations

from typing import Sequence

from .features import FeatureVector, cosine

AXIS_NAMES = ("personal", "academic", "telegram")


def register_axes(vector: FeatureVector) -> dict[str, float]:
    n = vector.as_named_dense()
    personal = (
        4.0 * n["first_person_ratio"]
        + 3.2 * n["contraction_ratio"]
        + 2.2 * n["informal_ratio"]
        + 1.2 * n["hedge_ratio"]
        + 1.0 * n["second_person_ratio"]
        + 5.0 * n["question_ratio"]
        + 3.5 * n["exclaim_ratio"]
    )
    academic = (
        3.4 * n["academic_ratio"]
        + 0.20 * max(n["avg_word_len"] - 4.0, 0.0)
        + 0.85 * n["long_word_ratio"]
        + 0.35 * n["function_ratio"]
        + 6.0 * n["comma_ratio"]
        + 0.12 * n["avg_syllables"]
    )
    telegram = (
        8.0 * n["punct_ratio"]
        + 9.0 * n["digit_ratio"]
        + 14.0 * n["colon_ratio"]
        + 8.0 * n["dash_ratio"]
        + 0.45 * n["short_word_ratio"]
        + 1.1 * max(0.42 - n["function_ratio"], 0.0)
        + 0.55 * n["unique_punct_types"]
    )
    return {
        "personal": personal,
        "academic": academic,
        "telegram": telegram,
    }


def register_vector(vector: FeatureVector) -> list[float]:
    axes = register_axes(vector)
    return [axes[name] for name in AXIS_NAMES]


def mean_register(vectors: Sequence[FeatureVector]) -> list[float]:
    if not vectors:
        return [0.0, 0.0, 0.0]
    acc = [0.0, 0.0, 0.0]
    for vector in vectors:
        for i, value in enumerate(register_vector(vector)):
            acc[i] += value
    return [value / len(vectors) for value in acc]


def smoothed_function_distance(
    left: FeatureVector, right: FeatureVector, alpha: float = 0.4
) -> float:
    """Add-k function-word cosine distance. Empty+empty is close, not far."""
    a = [count + alpha for count in left.function_counts]
    b = [count + alpha for count in right.function_counts]
    return 1.0 - cosine(a, b)


def _weighted_register(delta: Sequence[float]) -> float:
    # Personal and academic carry the student-vs-textbook contrast.
    # Telegram is kept (notes vs prose) but damped so two formula lines
    # do not look like different authors.
    personal, academic, telegram = delta
    raw = (
        (4.2 * personal) ** 2 + (2.4 * academic) ** 2 + (0.22 * telegram) ** 2
    ) ** 0.5
    return raw / 1.8


def span_distance(left: FeatureVector, right: FeatureVector) -> tuple[float, dict[str, float]]:
    """Distance between two (possibly merged) spans."""
    axes_l = register_vector(left)
    axes_r = register_vector(right)
    delta = [abs(a - b) for a, b in zip(axes_l, axes_r)]
    register = _weighted_register(delta)
    function = smoothed_function_distance(left, right)
    mixed = 0.82 * register + 0.18 * function
    parts = {
        "register": register,
        "function": function,
        "mixed": mixed,
        "personal": delta[0],
        "academic": delta[1],
        "telegram": delta[2],
    }
    return _confirm_axes(mixed, parts), parts


def _confirm_axes(mixed: float, parts: dict[str, float]) -> float:
    """Down-weight a cut that only moves one academic feature.

    Intra-author textbook sentences vary in connective choice and word
    length. A genuine register shift in this project usually moves
    personal voice, telegram compactness, or both.
    """
    cues = 0
    if parts["personal"] >= 0.10:
        cues += 1
    if parts["telegram"] >= 0.70:
        cues += 1
    if parts["academic"] >= 0.40 and parts["personal"] >= 0.05:
        cues += 1
    if cues == 0:
        return mixed * 0.28
    return mixed


def mean_span_distance(
    left_units: Sequence[FeatureVector],
    right_units: Sequence[FeatureVector],
    left_merged: FeatureVector,
    right_merged: FeatureVector,
) -> tuple[float, dict[str, float]]:
    """Block distance: mean register per side, function words from the merge."""
    mu_l = mean_register(left_units)
    mu_r = mean_register(right_units)
    delta = [abs(a - b) for a, b in zip(mu_l, mu_r)]
    register = _weighted_register(delta)
    function = smoothed_function_distance(left_merged, right_merged)
    mixed = 0.82 * register + 0.18 * function
    parts = {
        "register": register,
        "function": function,
        "mixed": mixed,
        "personal": delta[0],
        "academic": delta[1],
        "telegram": delta[2],
    }
    return _confirm_axes(mixed, parts), parts
