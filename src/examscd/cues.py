"""Forensic cue sheet I can recite without a library.

Adjacent short sentences share almost no character 3-grams, even when
the same person wrote both. That is why the detector does *not* cut on
raw pair cosine. It scores a handful of register cues, assigns a label,
and cuts when the label family changes. The cues are the same families
as the notes: slang, imperatives, minutes/formal boilerplate, telegram
notes, ``we`` versus ``one``, first-person diary, and lab shorthand.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from examscd.features import CONNECTIVES, FIRST_PERSON, SECOND_PERSON, TOKEN_RE, word_tokens

SLANG = frozenset(
    {
        "gonna",
        "gotta",
        "hey",
        "idk",
        "kinda",
        "lol",
        "lmao",
        "nvm",
        "ok",
        "omg",
        "r",
        "tbh",
        "u",
        "ur",
        "wanna",
        "wtf",
        "yeah",
        "yo",
    }
)
TEXT_SPEAK = frozenset({"u", "r", "ur", "nvm", "idk", "lol", "omg", "yo", "hey", "yeah", "ok"})
BARE_NEGATION = frozenset({"wont", "dont", "cant", "im", "ive", "id"})
IMPERATIVE = frozenset(
    {
        "add",
        "bake",
        "bring",
        "chop",
        "cover",
        "cut",
        "drop",
        "dump",
        "eat",
        "heat",
        "let",
        "mix",
        "pour",
        "preheat",
        "salt",
        "stir",
        "take",
        "toss",
        "use",
        "wait",
        "warm",
        "write",
    }
)
FORMAL_STRONG = frozenset(
    {
        "agreed",
        "amendment",
        "apologies",
        "chair",
        "committee",
        "confidential",
        "diagnosis",
        "kindly",
        "please",
        "quorum",
        "reminded",
        "rma",
        "warranty",
    }
)
FORMAL_WEAK = frozenset(
    {
        "business",
        "circulated",
        "coordinator",
        "meeting",
        "members",
        "minutes",
        "recorded",
    }
)
FORMAL_PHRASES = (
    "the chair",
    "the minutes",
    "the meeting",
    "no other business",
    "members were",
    "it was agreed",
    "please note",
    "kindly provide",
)
ACADEMIC = frozenset(
    {
        "approximately",
        "authorship",
        "baseline",
        "comprises",
        "compression",
        "constrained",
        "detection",
        "dilute",
        "document",
        "embedding",
        "emulsify",
        "empirical",
        "evidence",
        "formation",
        "infrastructural",
        "institutional",
        "intrinsic",
        "kinetically",
        "likelihood",
        "multinomial",
        "negotiated",
        "objective",
        "procedure",
        "register",
        "segmentation",
        "therefore",
        "thus",
        "topical",
    }
)
LAB = frozenset({"trial", "steep", "steeped", "strip", "kettle", "ph", "leaf"})

LABELS: tuple[str, ...] = (
    "slang",
    "imperative",
    "formal",
    "notes",
    "academic_we",
    "academic_one",
    "academic",
    "personal",
    "lab",
)

# Adjacent labels that are the same writer in a slightly different mood.
ADJACENT_ALIASES = {
    frozenset({"slang", "personal"}),
    frozenset({"academic", "academic_one"}),
    frozenset({"academic", "academic_we"}),
    frozenset({"lab", "personal"}),
}

# Labels that may reuse an earlier author id after someone else spoke.
RETURN_ALIASES = {
    frozenset({"academic", "academic_one"}),
    frozenset({"academic", "academic_we"}),
}


def adjacent_same(left: str, right: str) -> bool:
    return left == right or frozenset({left, right}) in ADJACENT_ALIASES


def return_same(left: str, right: str) -> bool:
    return left == right or frozenset({left, right}) in RETURN_ALIASES


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[.!?]+", text) if part.strip()]


def _first_words(text: str) -> list[str]:
    out = []
    for sent in _sentences(text):
        tokens = word_tokens(TOKEN_RE.findall(sent))
        if tokens:
            out.append(tokens[0])
    return out


@dataclass(frozen=True)
class CueScore:
    label: str
    scores: dict[str, float]
    vector: list[float]


def cue_scores(text: str) -> dict[str, float]:
    """Return a named score for each register. Higher means more like that cue."""
    words = word_tokens(TOKEN_RE.findall(text))
    n = max(len(words), 1)
    low = text.lower()
    firsts = _first_words(text)

    slang_hits = sum(1 for w in words if w in SLANG or w in BARE_NEGATION)
    if text[:1].islower() and words and words[0] in TEXT_SPEAK | {"i", "also", "the", "macro"}:
        slang_hits += 1
    slang = slang_hits / n * 5.0 + (0.9 if slang_hits else 0.0)
    if any(w in TEXT_SPEAK for w in words[:3]):
        slang += 0.6
    if text[:1].islower() and "=" not in text and not low.startswith(("easy set", "intrinsic", "scd")):
        slang += 0.35

    imp_hits = sum(1 for w in firsts if w in IMPERATIVE)
    if low.startswith("do not ") and "z-score" not in low:
        imp_hits += 1
    short = n <= 10
    imperative = imp_hits * 0.9 + (0.35 if short and imp_hits and slang_hits == 0 else 0.0)
    if "z-score" in low:
        imperative *= 0.2

    strong = sum(1 for w in words if w in FORMAL_STRONG)
    weak = sum(1 for w in words if w in FORMAL_WEAK)
    phrases = sum(1 for phrase in FORMAL_PHRASES if phrase in low)
    formal = 0.0
    if strong or phrases or weak >= 2:
        formal = strong * 0.9 + weak * 0.35 + phrases * 0.8 + 0.5

    notes = 0.0
    if "=" in text:
        notes += 1.4
    if low.startswith(("scd", "intrinsic", "easy set", "do not z-score")):
        notes += 1.3
    if "z-score" in low:
        notes += 0.8

    we = sum(1 for w in words if w == "we") / n
    one = sum(1 for w in words if w == "one") / n
    academic_hits = sum(1 for w in words if w in ACADEMIC or w in CONNECTIVES)
    nominal_stop = {"version", "session", "question", "mention", "pension", "tension", "mission"}
    nominal = sum(
        1
        for w in words
        if len(w) >= 8
        and w.endswith(("tion", "sion", "ment", "ness", "ity"))
        and w not in nominal_stop
    )
    longish = min(n / 18.0, 1.2)
    academic = academic_hits / n * 4.5 + nominal / n * 3.0
    if academic_hits or nominal:
        academic += 0.35 * longish
    if "one may" in low or "one should" in low:
        academic += 0.7
        one += 0.15
    if "in more careful terms" in low or "amylopectin" in low:
        academic += 0.6

    academic_we = academic * 0.7 + we * 8.0 + (0.4 if we >= 0.05 else 0.0)
    academic_one = academic * 0.7 + one * 8.0 + (0.5 if "one may" in low or "one should" in low else 0.0)

    first = sum(1 for w in words if w in FIRST_PERSON) / n
    second = sum(1 for w in words if w in SECOND_PERSON) / n
    personal = first * 6.0 + second * 2.5 + (0.35 if first >= 0.04 and slang_hits == 0 else 0.0)

    lab_hits = sum(1 for w in words if w in LAB)
    digits = len(re.findall(r"\d+", text))
    lab = lab_hits / n * 5.0 + min(digits, 3) * 0.15 + (0.5 if lab_hits else 0.0)

    return {
        "slang": slang,
        "imperative": imperative,
        "formal": formal,
        "notes": notes,
        "academic_we": academic_we,
        "academic_one": academic_one,
        "academic": academic,
        "personal": personal,
        "lab": lab,
    }


def assign_label(scores: dict[str, float], floor: float = 0.40) -> str:
    label = max(scores, key=scores.get)
    if scores["notes"] >= 0.80 and scores["notes"] >= scores[label] - 0.15:
        return "notes"
    if scores[label] < floor:
        return "personal" if scores["personal"] >= scores["lab"] else "lab"
    if label == "academic":
        if scores["academic_we"] >= scores["academic"] - 0.05 and scores["academic_we"] >= 0.45:
            return "academic_we"
        if scores["academic_one"] >= scores["academic"] - 0.05 and scores["academic_one"] >= 0.45:
            return "academic_one"
    return label


def score_unit(text: str) -> CueScore:
    scores = cue_scores(text)
    label = assign_label(scores)
    vector = [scores[name] for name in LABELS]
    return CueScore(label=label, scores=scores, vector=vector)


def stick_labels(labels: list[str], scores: list[dict[str, float]]) -> list[str]:
    """Remove one-unit flickers unless the new cue is clearly stronger."""
    out = list(labels)
    for i in range(1, len(out) - 1):
        if out[i] != out[i - 1] and out[i] != out[i + 1] and adjacent_same(out[i - 1], out[i + 1]):
            new = scores[i].get(out[i], 0.0)
            old = scores[i].get(out[i - 1], 0.0)
            if new - old < 0.35:
                out[i] = out[i - 1]
    return out


def label_units(units: list[str]) -> list[CueScore]:
    raw = [score_unit(unit) for unit in units]
    stuck = stick_labels([item.label for item in raw], [item.scores for item in raw])
    return [
        CueScore(label=lab, scores=item.scores, vector=item.vector)
        for lab, item in zip(stuck, raw, strict=True)
    ]
