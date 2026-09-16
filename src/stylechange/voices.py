"""Four coarse writing voices for an exam-sized baseline.

A full authorship model would keep a continuous embedding. For a take-home
that you can still *read*, we project each unit onto four named voices:

- **chat** — contractions, *you*, questions, informal lexis
- **student** — *I / me / my*, hedges, ``I think``
- **textbook** — academic connectives, long words, no first person
- **notes** — colons, digits, arrows, missing function words

``mixed`` means the scores did not separate cleanly. The detector then
inherits a neighbour or falls back to span distance.
"""

from __future__ import annotations

from .features import FeatureVector

VOICES: tuple[str, ...] = ("chat", "student", "textbook", "notes")

# Chat and student are different labels for --explain, but they are one
# author-like band: a recipe that says "yeah" then "I" is still one person.
_PERSONAL = frozenset({"chat", "student"})

# How much the winner must beat the runner-up before we trust the label.
_MARGIN = 0.10


def voice_scores(features: FeatureVector) -> dict[str, float]:
    chat = (
        2.2 * features.contraction_rate
        + 1.8 * features.second_person
        + 1.4 * features.question_rate
        + 2.0 * features.informal_rate
        + 1.8 * features.casual_rate
        + 1.0 * features.exclaim_rate
        + 0.4 * features.first_person_sg
        + 0.30 * max(0.0, 4.5 - features.mean_word_len)
        - 1.2 * features.academic_rate
        - 1.0 * features.arrow_rate
    )
    student = (
        2.6 * features.first_person_sg
        + 1.8 * features.student_phrase
        + 1.4 * features.hedge_rate
        + 0.5 * features.contraction_rate
        - 0.8 * features.academic_rate
        - 1.2 * features.arrow_rate
        - 0.8 * features.colon_rate
    )
    textbook = (
        2.2 * features.academic_rate
        + 0.55 * max(0.0, features.mean_word_len - 4.3)
        + 0.8 * features.comma_rate
        + 0.9 * features.passive_rate
        + 0.5 * features.first_person_pl
        + 0.7 * features.impersonal
        - 2.0 * features.contraction_rate
        - 1.6 * features.informal_rate
        - 1.4 * features.arrow_rate
        - 1.2 * features.colon_rate
        - 0.8 * features.first_person_sg
    )
    notes = (
        2.4 * features.arrow_rate
        + 2.0 * features.colon_rate
        + 1.6 * features.digit_rate
        + 1.2 * features.uppercase_word_rate
        + 1.0 * max(0.0, 8.0 - features.n_words) / 8.0
        + 0.6 * features.dash_rate
        - 1.1 * features.function_word_rate
        - 0.8 * features.first_person_sg
    )
    return {
        "chat": chat,
        "student": student,
        "textbook": textbook,
        "notes": notes,
    }


def cut_band(voice: str) -> str:
    """Voice used for *cutting*. ``chat`` and ``student`` share a band."""
    if voice in _PERSONAL:
        return "personal"
    return voice


def classify_voice(features: FeatureVector) -> str:
    # Short labelled lines (CFG: …, CRF: …, feat: …) are notes even when
    # a stray contraction or letter I would otherwise pull them toward chat.
    if features.n_words <= 14 and (features.arrow_rate > 0 or features.colon_rate > 0.2):
        return "notes"
    scores = voice_scores(features)
    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    winner, best = ordered[0]
    runner_up = ordered[1][1]
    if best < 0.08:
        return "mixed"
    if best - runner_up < _MARGIN and runner_up > 0:
        return "mixed"
    return winner


def merge_singleton_runs(labels: list[str]) -> list[str]:
    """Absorb a one-unit voice blip between two matching neighbours.

    Exam answers are written in blocks. A single sentence that looks
    briefly textbook-like in the middle of a student paragraph is almost
    never a real author change.
    """
    if len(labels) < 3:
        return list(labels)
    filled = list(labels)
    for index in range(1, len(filled) - 1):
        left, mid, right = filled[index - 1], filled[index], filled[index + 1]
        if mid != left and left == right and left != "mixed":
            filled[index] = left
    return filled


def smooth_voices(labels: list[str]) -> list[str]:
    """Fill ``mixed`` from the nearest confident neighbour (left, then right)."""
    if not labels:
        return []
    filled = list(labels)
    last = "mixed"
    for index, label in enumerate(filled):
        if label != "mixed":
            last = label
        elif last != "mixed":
            filled[index] = last
    last = "mixed"
    for index in range(len(filled) - 1, -1, -1):
        if filled[index] != "mixed":
            last = filled[index]
        elif last != "mixed":
            filled[index] = last
    return filled
