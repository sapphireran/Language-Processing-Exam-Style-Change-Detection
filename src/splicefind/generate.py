"""Tiny synthetic voices for exam demos.

These generators do not scrape Reddit and they do not reproduce PAN
data. Each voice is a handful of original paragraph templates with a
stable stylometric habit so students can build easy / medium / hard
splices without leaving the repository.
"""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from typing import Sequence

from .io import Problem, Truth


@dataclass(frozen=True)
class Voice:
    name: str
    register: str
    templates: tuple[str, ...]

    def paragraph(self, rng: random.Random, index: int = 0) -> str:
        if not self.templates:
            raise ValueError(f"voice {self.name} has no templates")
        return self.templates[(index + rng.randrange(len(self.templates))) % len(self.templates)]


VOICE_CASUAL = Voice(
    name="casual_first",
    register="casual",
    templates=(
        "I keep meaning to fix the latch on the shed. It's not broken exactly, just stubborn, and I don't want to spend a Saturday arguing with a screwdriver.",
        "Honestly I thought the bus would be empty. It wasn't. I stood there with a bag of apples and hoped nobody asked why I was smiling at a window.",
        "I can't find the spare key. I looked in the drawer, then the coat, then the drawer again like it was going to apologise and show up.",
        "We should just leave earlier. I know that sounds dull, but I'm tired of sprinting for a door that closes in my face.",
    ),
)

VOICE_FORMAL = Voice(
    name="formal_impersonal",
    register="formal",
    templates=(
        "One may observe that the latch mechanism has drifted from its intended alignment. A modest adjustment, rather than replacement, would likely restore reliable closure.",
        "The service interval appears sufficient under ordinary load. However, crowding at peak hours remains a structural inconvenience rather than an incidental delay.",
        "The spare key was last recorded in the household inventory. Its present location cannot be established from the available notes.",
        "An earlier departure would reduce the probability of a missed connection. The recommendation follows from the published timetable rather than from preference.",
    ),
)

VOICE_QUESTIONS = Voice(
    name="question_you",
    register="interactive",
    templates=(
        "Have you checked the hinge side, not just the latch? What if the door is swelling and you're blaming the wrong part?",
        "You ever notice how the bus only feels late when you're carrying something fragile? Why is that the rule?",
        "Did you look behind the cookbooks? Why do keys always migrate toward the least obvious shelf?",
        "Could you leave ten minutes sooner? Would that really ruin the morning, or would it just feel like a smaller panic?",
    ),
)

VOICE_LAB = Voice(
    name="lab_we",
    register="scientific",
    templates=(
        "We measured the gap at three points along the strike plate. The mean offset was 1.8 mm, which is consistent with seasonal swelling of the frame.",
        "We recorded boarding times for twelve departures. The upper quartile exceeded the scheduled dwell, suggesting a systematic rather than random delay.",
        "We inventoried the drawer contents twice. The key was absent on both passes; a third search is unlikely to change the observation.",
        "We compared an 08:10 departure with an 08:00 departure over five weekdays. The earlier slot reduced missed connections in four of five trials.",
    ),
)

VOICE_NOTES = Voice(
    name="telegram_notes",
    register="notes",
    templates=(
        "Shed latch. Sticky. Not urgent. Saturday maybe. Need screwdriver, oil, patience.",
        "Bus packed. Apples survived. Window seat gone. Smile unexplained. Home 18:40.",
        "Spare key: missing. Drawer: no. Coat: no. Bowl by door: no. Stop repeating drawer.",
        "Leave earlier. Door closes at :12. Sprint failed. Dull plan is still a plan.",
    ),
)

VOICES: dict[str, Voice] = {
    voice.name: voice
    for voice in (VOICE_CASUAL, VOICE_FORMAL, VOICE_QUESTIONS, VOICE_LAB, VOICE_NOTES)
}


@dataclass(frozen=True)
class SyntheticDocument:
    problem: Problem
    truth: Truth
    voice_sequence: tuple[str, ...]


def _author_runs(sequence: Sequence[str]) -> list[int]:
    changes = []
    for left, right in zip(sequence, sequence[1:]):
        changes.append(0 if left == right else 1)
    return changes


def stitch(
    voice_names: Sequence[str],
    *,
    problem_id: str,
    difficulty: str,
    title: str,
    seed: int = 0,
) -> SyntheticDocument:
    rng = random.Random(seed)
    paragraphs = []
    for index, name in enumerate(voice_names):
        voice = VOICES[name]
        paragraphs.append(voice.paragraph(rng, index))
    text = "\n\n".join(paragraphs)
    changes = _author_runs(voice_names)
    n_authors = len(set(voice_names))
    problem = Problem(problem_id=problem_id, text=text)
    truth = Truth(
        problem_id=problem_id,
        changes=changes,
        authors=n_authors,
        difficulty=difficulty,
        title=title,
        notes="synthetic voices: " + " -> ".join(voice_names),
    )
    return SyntheticDocument(problem=problem, truth=truth, voice_sequence=tuple(voice_names))


def pattern_easy(index: int) -> tuple[str, ...]:
    pairs = [
        ("casual_first", "formal_impersonal"),
        ("telegram_notes", "lab_we"),
        ("question_you", "formal_impersonal"),
        ("casual_first", "lab_we"),
    ]
    left, right = pairs[index % len(pairs)]
    return (left, left, right, right)


def pattern_medium(index: int) -> tuple[str, ...]:
    triples = [
        ("casual_first", "question_you", "casual_first"),
        ("formal_impersonal", "lab_we", "formal_impersonal"),
        ("lab_we", "casual_first", "lab_we"),
        ("question_you", "telegram_notes", "question_you"),
    ]
    a, b, c = triples[index % len(triples)]
    return (a, a, b, c, c)


def pattern_hard(index: int) -> tuple[str, ...]:
    # Close registers: lab vs formal, or notes vs casual fragments.
    pairs = [
        ("formal_impersonal", "lab_we"),
        ("casual_first", "telegram_notes"),
        ("formal_impersonal", "formal_impersonal"),
        ("lab_we", "formal_impersonal"),
    ]
    left, right = pairs[index % len(pairs)]
    return (left, right, right, left)


def make_split(
    *,
    n_easy: int = 6,
    n_medium: int = 6,
    n_hard: int = 6,
    seed: int = 23,
) -> list[SyntheticDocument]:
    docs: list[SyntheticDocument] = []
    counter = itertools.count(1)
    for i in range(n_easy):
        pid = f"{next(counter):03d}"
        docs.append(
            stitch(
                pattern_easy(i),
                problem_id=pid,
                difficulty="easy",
                title=f"easy splice {pid}",
                seed=seed + i,
            )
        )
    for i in range(n_medium):
        pid = f"{next(counter):03d}"
        docs.append(
            stitch(
                pattern_medium(i),
                problem_id=pid,
                difficulty="medium",
                title=f"medium splice {pid}",
                seed=seed + 100 + i,
            )
        )
    for i in range(n_hard):
        pid = f"{next(counter):03d}"
        docs.append(
            stitch(
                pattern_hard(i),
                problem_id=pid,
                difficulty="hard",
                title=f"hard splice {pid}",
                seed=seed + 200 + i,
            )
        )
    return docs
