"""Closed-class lists used as stylometric cues.

These are exam-sized inventories, not a full English lexicon. They exist so
the oral-exam answer is concrete: *which* words did you count, and why?

Function words follow the Mosteller & Wallace intuition — they are frequent,
topic-light, and hard to avoid. The other lists are register flags for the
four voices in ``voices.py``.
"""

from __future__ import annotations

FUNCTION_WORDS: frozenset[str] = frozenset(
    {
        "a",
        "about",
        "above",
        "after",
        "again",
        "against",
        "all",
        "am",
        "an",
        "and",
        "any",
        "are",
        "as",
        "at",
        "be",
        "because",
        "been",
        "before",
        "being",
        "below",
        "between",
        "both",
        "but",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "doing",
        "down",
        "during",
        "each",
        "few",
        "for",
        "from",
        "further",
        "had",
        "has",
        "have",
        "having",
        "here",
        "how",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "just",
        "more",
        "most",
        "no",
        "nor",
        "not",
        "now",
        "of",
        "off",
        "on",
        "once",
        "only",
        "or",
        "other",
        "our",
        "out",
        "over",
        "own",
        "same",
        "should",
        "so",
        "some",
        "such",
        "than",
        "that",
        "the",
        "their",
        "then",
        "there",
        "these",
        "this",
        "those",
        "through",
        "to",
        "too",
        "under",
        "until",
        "up",
        "very",
        "was",
        "we",
        "were",
        "what",
        "when",
        "where",
        "which",
        "while",
        "who",
        "whom",
        "why",
        "will",
        "with",
        "would",
    }
)

# English first person is capital I. Lowercase i in P(w_i) is not.
FIRST_PERSON_SG: frozenset[str] = frozenset(
    {"i", "i'd", "i'll", "i'm", "i've", "me", "mine", "my", "myself"}
)
FIRST_PERSON_PL: frozenset[str] = frozenset({"our", "ours", "ourselves", "us", "we"})
SECOND_PERSON: frozenset[str] = frozenset({"you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself"})
IMPERSONAL: frozenset[str] = frozenset({"one", "one's", "oneself"})

ACADEMIC: frozenset[str] = frozenset(
    {
        "accordingly",
        "albeit",
        "consequently",
        "furthermore",
        "hence",
        "however",
        "moreover",
        "namely",
        "nevertheless",
        "nonetheless",
        "specifically",
        "subsequently",
        "thereafter",
        "therefore",
        "thus",
        "whereas",
        "whereby",
    }
)

HEDGES: frozenset[str] = frozenset(
    {
        "basically",
        "guess",
        "kinda",
        "maybe",
        "perhaps",
        "pretty",
        "probably",
        "quite",
        "rather",
        "sorta",
        "stuff",
        "thing",
        "things",
    }
)

INFORMAL: frozenset[str] = frozenset(
    {
        "alot",
        "btw",
        "chuck",
        "gonna",
        "gotta",
        "hey",
        "idk",
        "imo",
        "kinda",
        "lol",
        "messy",
        "nah",
        "nutty",
        "ok",
        "okay",
        "sorta",
        "wanna",
        "yeah",
        "yep",
    }
)

# Kitchen / diary lexis that is almost never academic.
CASUAL: frozenset[str] = frozenset(
    {
        "butter",
        "chuck",
        "fridge",
        "messy",
        "nutty",
        "oven",
        "pan",
        "recipe",
        "smells",
        "stirring",
        "worry",
    }
)

# Surface forms that almost always mean a student hedging an answer.
STUDENT_PHRASES: tuple[str, ...] = (
    "i think",
    "i guess",
    "i remember",
    "for me",
    "in my head",
    "the way i",
    "so here is",
    "so here's",
    "i expect",
    "i keep",
)

IMPERSONAL_PHRASES: tuple[str, ...] = (
    "one may",
    "one can",
    "one might",
    "one should",
    "one would",
)

CONTRACTION_MARKERS: tuple[str, ...] = (
    "n't",
    "'re",
    "'ve",
    "'ll",
    "'d",
    "'m",
    "’t",
    "’re",
    "’ve",
    "’ll",
    "’d",
    "’m",
)
