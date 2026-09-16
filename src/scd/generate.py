"""Deterministic synthetic corpus for the personal exam notes."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path

from scd.io import write_problem, write_truth

DEFAULT_SEED = 20260316
BANDS = ("easy", "medium", "hard")
DOCS_PER_BAND = 12

PINNED_EASY_PROBLEM_1_UNITS = (
    "The souffle requires a precise fold of the egg whites into the batter.",
    "Oven temperature should remain stable so the structure can set.",
    "Yeah I'm just gonna chuck the frozen pizza in and hope for the best.",
    "Don't overthink dinner tonight, seriously.",
)
PINNED_EASY_PROBLEM_1_AUTHORS = 2
PINNED_EASY_PROBLEM_1_CHANGES = (0, 1, 0)


@dataclass(frozen=True)
class Persona:
    name: str
    templates: tuple[str, ...]


# Formal academic: long, hedges, no contractions, almost no first person.
AVERY = Persona(
    name="avery",
    templates=(
        "The {noun} requires a precise {act} of the {noun2} before the next stage can begin.",
        "However, one must consider whether the {noun} can remain {adj} under these conditions.",
        "It is therefore reasonable to treat the {noun} as a {adj} component of the process.",
        "Subsequently, the {noun} should remain {adj} so that the {noun2} may settle.",
        "Moreover, a careful reading of the {noun} suggests that the {noun2} is not incidental.",
        "The available evidence indicates that the {noun} will {verb} only if the {noun2} is {adj}.",
        "In such cases the {noun} constitutes a {adj} constraint on the surrounding {noun2}.",
        "A further observation is that the {noun}, once {adj}, no longer governs the {noun2}.",
        "One may nevertheless argue that the {noun} remains the more {adj} of the two factors.",
        "The procedure, however, depends on a {adj} {noun} rather than on a hurried {act}.",
    ),
)

# Casual internet: contractions, first/second person, short, exclamation.
BLAKE = Persona(
    name="blake",
    templates=(
        "Yeah I'm just gonna {verb} the {noun} and hope for the best!",
        "Don't {verb} the {noun} tonight, seriously.",
        "I kinda think the {noun} is pretty much a lost cause.",
        "Tbh you should just {verb} it and move on.",
        "Wait, that's not how I {verb} the {noun} at all!",
        "I'm not gonna overthink the {noun}; it's fine.",
        "You really don't need a fancy {noun} for this.",
        "Honestly the {noun} was a mess and I didn't care.",
        "Just {verb} the {noun} already and let's go.",
        "I can't deal with this {noun} right now, ugh.",
    ),
)

# Technical procedural: parentheses, digits, low pronouns.
CASEY = Persona(
    name="casey",
    templates=(
        "Set the {noun} threshold to {n} and re-run the {noun2}.",
        "The {noun} vector is then projected via the {adj} transform.",
        "If the {noun} exceeds {n}, discard the sample (see {noun2}).",
        "Call the {act} routine after the {noun} has been normalized.",
        "Keep the {noun} at {n} units; log the {noun2} on each pass.",
        "Replace the {noun} parameter (default {n}) before the next {act}.",
        "The {noun} is stored as a {adj} table keyed by {noun2}.",
        "Validate the {noun} against the {noun2} checksum, then continue.",
        "Scale the {noun} by {n} and write the {noun2} to disk.",
        "A {adj} {noun} of length {n} is sufficient for this check.",
    ),
)

# Narrative past: sensory, medium length, occasional first-person plural.
DREW = Persona(
    name="drew",
    templates=(
        "We walked past the {noun} before the {noun2} started.",
        "She said the {noun} had already {verb} by then.",
        "Later that afternoon the {noun} felt {adj} against the {noun2}.",
        "Nobody mentioned the {noun} until the {noun2} was over.",
        "The {noun} sat there, {adj}, as if waiting for the {noun2}.",
        "We watched the {noun} change while the {noun2} cooled.",
        "He kept the {noun} in his pocket until the {noun2} arrived.",
        "By evening the {noun} had {verb} and the {noun2} was quiet.",
        "A small {noun} remained on the table beside the {noun2}.",
        "They left the {noun} where it was and talked about the {noun2}.",
    ),
)

# Clipped formal: no hedges, prefers "which", short-medium, no contractions.
ELLIS = Persona(
    name="ellis",
    templates=(
        "The {noun} which follows is {adj}.",
        "Keep the {noun} {adj}. The {noun2} can wait.",
        "This {noun} is the {adj} part. The rest is secondary.",
        "Use the {noun} which matches the {noun2}.",
        "The {noun} is ready. Leave the {noun2} untouched.",
        "A {adj} {noun} is enough. Extra {noun2} adds noise.",
        "Note the {noun} which sits beside the {noun2}.",
        "The {noun} holds. The {noun2} does not.",
        "Apply the {noun} once. Repeat only if the {noun2} fails.",
        "The {adj} {noun} comes first; the {noun2} is later.",
    ),
)

PERSONAS = {
    "avery": AVERY,
    "blake": BLAKE,
    "casey": CASEY,
    "drew": DREW,
    "ellis": ELLIS,
}

# Topic lexicons: nouns / acts / adjectives / verbs shared inside a topic.
Topic = dict[str, tuple[str, ...]]

BAKING: Topic = {
    "noun": ("souffle", "batter", "crust", "dough", "meringue", "oven"),
    "noun2": ("egg whites", "structure", "glaze", "tin", "rack", "crumb"),
    "act": ("fold", "whisk", "rest", "bake", "proof"),
    "adj": ("stable", "precise", "fragile", "even", "warm"),
    "verb": ("set", "collapse", "rise", "cool", "brown"),
    "n": ("180", "12", "3"),
}

TRAINS: Topic = {
    "noun": ("timetable", "platform", "ticket", "delay", "carriage", "guard"),
    "noun2": ("connection", "barrier", "announcement", "queue", "siding"),
    "act": ("check", "rebook", "board", "wait", "scan"),
    "adj": ("late", "crowded", "revised", "short", "open"),
    "verb": ("leave", "stall", "arrive", "fill", "close"),
    "n": ("7", "14", "2"),
}

HIKING: Topic = {
    "noun": ("ridge", "trail", "pack", "switchback", "cairn", "map"),
    "noun2": ("ascent", "weather", "stream", "shelter", "descent"),
    "act": ("climb", "mark", "ford", "pace", "rest"),
    "adj": ("steep", "narrow", "clear", "icy", "quiet"),
    "verb": ("turn", "hold", "drop", "open", "fade"),
    "n": ("8", "16", "4"),
}

DEBUGGING: Topic = {
    "noun": ("test", "fixture", "trace", "timeout", "mock", "build"),
    "noun2": ("log", "harness", "assert", "cache", "runner"),
    "act": ("rerun", "isolate", "patch", "bisect", "stub"),
    "adj": ("flaky", "stale", "local", "silent", "red"),
    "verb": ("fail", "pass", "hang", "leak", "trip"),
    "n": ("3", "10", "5"),
}

COFFEE: Topic = {
    "noun": ("bloom", "slurry", "kettle", "grind", "filter", "pour"),
    "noun2": ("grounds", "carafe", "scale", "bed", "drawdown"),
    "act": ("wet", "pour", "swirl", "weigh", "rinse"),
    "adj": ("even", "fine", "hot", "slow", "level"),
    "verb": ("rise", "stall", "drain", "cool", "clog"),
    "n": ("15", "4", "92"),
}

TRANSPORT: Topic = {
    "noun": ("bus", "stop", "fare", "card", "lane", "signal"),
    "noun2": ("depot", "driver", "transfer", "shelter", "loop"),
    "act": ("tap", "board", "hold", "reroute", "time"),
    "adj": ("frequent", "packed", "early", "slow", "direct"),
    "verb": ("skip", "wait", "move", "stop", "turn"),
    "n": ("12", "6", "20"),
}

PLANTS: Topic = {
    "noun": ("seedling", "soil", "pot", "leaf", "tray", "stem"),
    "noun2": ("window", "water", "root", "light", "sill"),
    "act": ("water", "thin", "turn", "pot", "feed"),
    "adj": ("damp", "leggy", "bright", "tight", "young"),
    "verb": ("wilt", "lean", "sprout", "dry", "yellow"),
    "n": ("2", "9", "11"),
}

RECYCLING: Topic = {
    "noun": ("bin", "label", "lid", "crate", "sort", "film"),
    "noun2": ("glass", "paper", "collection", "yard", "route"),
    "act": ("rinse", "sort", "flatten", "leave", "check"),
    "adj": ("empty", "clean", "mixed", "weekly", "closed"),
    "verb": ("count", "miss", "fill", "split", "stick"),
    "n": ("2", "7", "14"),
}

EASY_TOPICS = (BAKING, TRAINS, HIKING, DEBUGGING)
MEDIUM_DOMAINS = (COFFEE, TRANSPORT, PLANTS)
HARD_TOPICS = (COFFEE, RECYCLING, PLANTS)

EASY_PAIRS = (("avery", "blake"), ("drew", "blake"), ("avery", "casey"), ("drew", "casey"))
MEDIUM_PAIRS = (("avery", "blake"), ("casey", "blake"), ("avery", "drew"), ("ellis", "blake"))
HARD_PAIRS = (("avery", "ellis"), ("casey", "ellis"), ("avery", "casey"), ("drew", "ellis"))

# Author-run patterns. Integers index into the chosen pair (0 or 1),
# or 2 for a third voice on easy multi-author docs.
SEQUENCES_MULTI = (
    (0, 0, 1, 1),
    (0, 1, 1, 1),
    (0, 0, 0, 1, 1),
    (0, 0, 1, 1, 0, 0),
    (0, 1, 0, 1),
    (0, 0, 1, 1, 1),
    (0, 0, 1, 1, 2, 2),
)
SEQUENCES_SINGLE = (
    (0, 0, 0, 0),
    (0, 0, 0, 0, 0),
)


def _fill(template: str, topic: Topic, rng: random.Random) -> str:
    fields = {key: rng.choice(values) for key, values in topic.items()}
    return template.format(**fields)


def render_sentence(persona: Persona, topic: Topic, rng: random.Random) -> str:
    template = rng.choice(persona.templates)
    return _fill(template, topic, rng)


def changes_from_authors(authors: list[str]) -> list[int]:
    return [int(left != right) for left, right in zip(authors, authors[1:])]


def _unique_sentences(
    persona: Persona,
    topic: Topic,
    rng: random.Random,
    n: int,
) -> list[str]:
    seen: set[str] = set()
    units: list[str] = []
    # Templates × slot combinations are large enough; still guard loops.
    for _ in range(n * 20):
        sentence = render_sentence(persona, topic, rng)
        if sentence in seen:
            continue
        seen.add(sentence)
        units.append(sentence)
        if len(units) == n:
            return units
    # Fall back to allowing repeats rather than hanging.
    while len(units) < n:
        units.append(render_sentence(persona, topic, rng))
    return units


def _choose_personas(band: str, rng: random.Random, *, single: bool) -> list[str]:
    table = {"easy": EASY_PAIRS, "medium": MEDIUM_PAIRS, "hard": HARD_PAIRS}[band]
    pair = list(rng.choice(table))
    if single:
        return [rng.choice(pair)]
    if band == "easy" and rng.random() < 0.25:
        extra = rng.choice([name for name in PERSONAS if name not in pair])
        pair.append(extra)
    return pair


def _topic_for_author(
    band: str,
    author_index: int,
    shared: Topic,
    rng: random.Random,
) -> Topic:
    if band == "easy":
        # Each author voice gets its own topic so aboutness leaks with style.
        return EASY_TOPICS[(EASY_TOPICS.index(shared) + author_index) % len(EASY_TOPICS)]
    return shared


def build_document(
    band: str,
    rng: random.Random,
    *,
    single: bool,
) -> tuple[list[str], list[str]]:
    voices = _choose_personas(band, rng, single=single)
    if single:
        sequence = list(rng.choice(SEQUENCES_SINGLE))
        names = [voices[0] for _ in sequence]
    else:
        raw = list(rng.choice(SEQUENCES_MULTI))
        names = [voices[min(index, len(voices) - 1)] for index in raw]
        if len(set(names)) < 2:
            names[-1] = voices[1] if len(voices) > 1 else names[-1]

    if band == "easy":
        shared = rng.choice(EASY_TOPICS)
    elif band == "medium":
        shared = rng.choice(MEDIUM_DOMAINS)
    else:
        shared = rng.choice(HARD_TOPICS)

    units: list[str] = []
    for position, name in enumerate(names):
        topic = _topic_for_author(band, voices.index(name) if name in voices else 0, shared, rng)
        # Give each slot a fresh sentence from that persona/topic.
        sentence = _unique_sentences(PERSONAS[name], topic, rng, 1)[0]
        # Extra guard against accidental identical neighbours.
        if units and sentence == units[-1]:
            sentence = render_sentence(PERSONAS[name], topic, rng)
        units.append(sentence)
        _ = position
    return units, names


def generate_band(band: str, rng: random.Random) -> list[tuple[list[str], list[int], int]]:
    docs: list[tuple[list[str], list[int], int]] = []
    if band == "easy":
        docs.append(
            (
                list(PINNED_EASY_PROBLEM_1_UNITS),
                list(PINNED_EASY_PROBLEM_1_CHANGES),
                PINNED_EASY_PROBLEM_1_AUTHORS,
            )
        )
    target = DOCS_PER_BAND
    # One single-author document per band, plus the rest mixed.
    singles_needed = 1
    while len(docs) < target:
        single = singles_needed > 0 and len(docs) >= (1 if band == "easy" else 0)
        if single:
            singles_needed -= 1
        # After the first (possibly pinned) doc, insert the single-author one next.
        if band == "easy" and len(docs) == 1 and singles_needed:
            single = True
            singles_needed -= 1
        units, names = build_document(band, rng, single=single)
        changes = changes_from_authors(names)
        authors = len(set(names))
        if authors == 1 and any(changes):
            continue
        if authors >= 2 and not any(changes):
            continue
        docs.append((units, changes, authors))
    return docs[:target]


def write_corpus(root: str | Path, *, seed: int = DEFAULT_SEED) -> dict[str, int]:
    root = Path(root)
    rng = random.Random(seed)
    counts: dict[str, int] = {}
    for band in BANDS:
        docs = generate_band(band, rng)
        dest = root / band
        if dest.exists():
            for stale in dest.glob("problem-*.txt"):
                stale.unlink()
            for stale in dest.glob("truth-problem-*.json"):
                stale.unlink()
        dest.mkdir(parents=True, exist_ok=True)
        for index, (units, changes, authors) in enumerate(docs, start=1):
            write_problem(dest / f"problem-{index}.txt", units)
            write_truth(dest / f"truth-problem-{index}.json", authors, changes)
        counts[band] = len(docs)
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the synthetic SCD toy corpus.")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args(argv)
    counts = write_corpus(args.out, seed=args.seed)
    print(f"wrote {counts} under {args.out} (seed={args.seed})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
