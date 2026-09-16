"""Closed stylometric inventory I can recite without opening a paper.

Every feature is a rate or a mean. Nothing is z-scored across a 100-D
vector on a six-sentence document — that is the trap I keep writing down
in the exam notes. The function-word list is the Mosteller–Wallace idea
(closed-class words carry style, open-class words carry topic), not their
Federalist list copied verbatim.
"""

from __future__ import annotations

import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\w\s]", re.UNICODE)

# Closed-class English words plus a few contractions. Topic nouns stay out.
FUNCTION_WORDS: tuple[str, ...] = (
    "a",
    "about",
    "after",
    "all",
    "also",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "been",
    "before",
    "being",
    "between",
    "both",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "down",
    "each",
    "for",
    "from",
    "had",
    "has",
    "have",
    "he",
    "her",
    "here",
    "him",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "just",
    "like",
    "me",
    "more",
    "most",
    "my",
    "no",
    "not",
    "now",
    "of",
    "on",
    "one",
    "only",
    "or",
    "other",
    "our",
    "out",
    "over",
    "she",
    "so",
    "some",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "up",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "will",
    "with",
    "would",
    "you",
    "your",
)

FUNCTION_WORD_SET = frozenset(FUNCTION_WORDS)

CONTRACTIONS = frozenset(
    {
        "aren't",
        "can't",
        "couldn't",
        "didn't",
        "doesn't",
        "don't",
        "hadn't",
        "hasn't",
        "haven't",
        "he'd",
        "he'll",
        "he's",
        "i'd",
        "i'll",
        "i'm",
        "i've",
        "isn't",
        "it's",
        "let's",
        "mightn't",
        "mustn't",
        "she'd",
        "she'll",
        "she's",
        "shouldn't",
        "that's",
        "there's",
        "they'd",
        "they'll",
        "they're",
        "they've",
        "wasn't",
        "we'd",
        "we'll",
        "we're",
        "we've",
        "weren't",
        "what's",
        "won't",
        "wouldn't",
        "you'd",
        "you'll",
        "you're",
        "you've",
        "gonna",
        "wanna",
        "gotta",
        "kinda",
        "lol",
        "omg",
        "idk",
        "tbh",
    }
)

FIRST_PERSON = frozenset({"i", "me", "my", "mine", "we", "us", "our", "ours", "i'm", "i've", "i'll", "i'd", "we're", "we've", "we'll"})
SECOND_PERSON = frozenset({"you", "your", "yours", "you're", "you've", "you'll", "you'd"})
HEDGES = frozenset({"maybe", "perhaps", "might", "somewhat", "rather", "quite", "probably", "possibly", "apparently", "arguably"})
BOOSTERS = frozenset({"very", "really", "extremely", "highly", "clearly", "obviously", "totally", "literally"})
CONNECTIVES = frozenset({"however", "therefore", "thus", "moreover", "nevertheless", "furthermore", "hence", "consequently"})
IMPERATIVE_CUES = frozenset(
    {
        "add",
        "bake",
        "chop",
        "cut",
        "heat",
        "mix",
        "note",
        "pour",
        "preheat",
        "see",
        "stir",
        "take",
        "use",
        "wait",
        "write",
        "consider",
        "let",
    }
)

STYLE_DIMS: tuple[str, ...] = (
    "mean_word_len",
    "mean_unit_len",
    "type_token",
    "function_rate",
    "punct_rate",
    "digit_rate",
    "upper_rate",
    "first_person",
    "second_person",
    "contraction_rate",
    "question_rate",
    "hedge_rate",
    "booster_rate",
    "connective_rate",
    "nominal_rate",
    "imperative_rate",
)


def tokenize(text: str) -> list[str]:
    """Lowercased word/punct tokens. Apostrophes stay inside contractions."""
    return TOKEN_RE.findall(text)


def word_tokens(tokens: list[str]) -> list[str]:
    return [tok.lower() for tok in tokens if re.search(r"[A-Za-z]", tok)]


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def style_vector(text: str) -> list[float]:
    """Return the closed inventory as a list aligned with ``STYLE_DIMS``."""
    tokens = tokenize(text)
    words = word_tokens(tokens)
    n_tok = len(tokens)
    n_word = len(words)
    types = set(words)
    punct = sum(1 for tok in tokens if not re.search(r"[A-Za-z0-9]", tok))
    digits = sum(1 for tok in tokens if tok.isdigit())
    letters = [ch for ch in text if ch.isalpha()]
    upper = sum(1 for ch in letters if ch.isupper())
    first = sum(1 for w in words if w in FIRST_PERSON)
    second = sum(1 for w in words if w in SECOND_PERSON)
    contr = sum(1 for w in words if w in CONTRACTIONS)
    hedges = sum(1 for w in words if w in HEDGES)
    boost = sum(1 for w in words if w in BOOSTERS)
    conn = sum(1 for w in words if w in CONNECTIVES)
    nominal = sum(1 for w in words if w.endswith(("tion", "sion", "ment", "ness", "ity", "ance")))
    questions = text.count("?")
    first_words = [w.split()[0].lower().strip(".,;:!?") for w in re.split(r"[.!?]", text) if w.split()]
    imper = sum(1 for w in first_words if w in IMPERATIVE_CUES)
    mean_word = _safe_div(sum(len(w) for w in words), n_word)
    return [
        mean_word / 10.0,
        min(n_word / 40.0, 1.5),
        _safe_div(len(types), n_word),
        _safe_div(sum(1 for w in words if w in FUNCTION_WORD_SET), n_word),
        _safe_div(punct, n_tok),
        _safe_div(digits, n_tok),
        _safe_div(upper, max(len(letters), 1)),
        _safe_div(first, n_word),
        _safe_div(second, n_word),
        _safe_div(contr, n_word),
        _safe_div(questions, max(text.count(".") + text.count("!") + questions, 1)),
        _safe_div(hedges, n_word),
        _safe_div(boost, n_word),
        _safe_div(conn, n_word),
        _safe_div(nominal, n_word),
        _safe_div(imper, max(len(first_words), 1)),
    ]


def style_dict(text: str) -> dict[str, float]:
    return dict(zip(STYLE_DIMS, style_vector(text), strict=True))


def function_word_rates(text: str) -> list[float]:
    """Relative frequencies over the closed function-word list."""
    words = word_tokens(tokenize(text))
    counts = Counter(words)
    total = max(len(words), 1)
    return [counts[w] / total for w in FUNCTION_WORDS]


def l1_distance(a: list[float], b: list[float]) -> float:
    return sum(abs(x - y) for x, y in zip(a, b, strict=True))


def l2_distance(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b, strict=True)))


def function_word_l1(a: str, b: str) -> float:
    """L1 between two function-word distributions. Range is roughly [0, 2]."""
    return l1_distance(function_word_rates(a), function_word_rates(b))


def style_l2(a: str, b: str) -> float:
    return l2_distance(style_vector(a), style_vector(b))
