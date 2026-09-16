"""Closed-class English lists used as style, not topic, signals.

Function words are the exam-friendly reason stylometry still works when
the topic is held constant. They are frequent, topic-light, and hard to
fake consistently. The list below is a personal study list — not the
only defensible inventory, and you should be ready to add or drop items
if an examiner asks.
"""

from __future__ import annotations

# High-frequency English function words, grouped so the oral exam can
# name the categories rather than reciting 80 tokens.
ARTICLES = ("a", "an", "the")
DEMONSTRATIVES = ("this", "that", "these", "those")
PERSONAL = (
    "i",
    "me",
    "my",
    "mine",
    "myself",
    "we",
    "us",
    "our",
    "ours",
    "ourselves",
    "you",
    "your",
    "yours",
    "yourself",
    "he",
    "him",
    "his",
    "she",
    "her",
    "hers",
    "they",
    "them",
    "their",
    "theirs",
    "it",
    "its",
    "one",
)
PREPOSITIONS = (
    "of",
    "in",
    "to",
    "for",
    "with",
    "on",
    "at",
    "from",
    "by",
    "about",
    "as",
    "into",
    "like",
    "through",
    "after",
    "over",
    "between",
    "out",
    "against",
    "during",
    "without",
    "before",
    "under",
    "around",
    "among",
    "across",
    "within",
    "along",
    "toward",
    "upon",
)
AUXILIARIES = (
    "is",
    "am",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "shall",
    "should",
    "can",
    "could",
    "may",
    "might",
    "must",
)
CONJUNCTIONS = (
    "and",
    "but",
    "or",
    "nor",
    "so",
    "yet",
    "because",
    "if",
    "while",
    "although",
    "though",
    "unless",
    "until",
    "since",
    "whether",
)
RELATIVES = ("who", "whom", "whose", "which", "what", "where", "when", "why", "how")
NEGATION = ("not", "no", "nor")
QUANTIFIERS = (
    "all",
    "any",
    "each",
    "every",
    "few",
    "many",
    "more",
    "most",
    "other",
    "some",
    "such",
    "both",
    "own",
    "same",
)

FUNCTION_WORDS: tuple[str, ...] = tuple(
    dict.fromkeys(
        ARTICLES
        + DEMONSTRATIVES
        + PERSONAL
        + PREPOSITIONS
        + AUXILIARIES
        + CONJUNCTIONS
        + RELATIVES
        + NEGATION
        + QUANTIFIERS
    )
)

# Discourse / academic connective layer — still mostly style, but more
# register-sensitive than "the".
FORMAL_CONNECTIVES = (
    "however",
    "therefore",
    "moreover",
    "furthermore",
    "nevertheless",
    "nonetheless",
    "consequently",
    "thus",
    "hence",
    "whereas",
    "whereby",
    "herein",
    "thereafter",
    "accordingly",
    "conversely",
    "specifically",
    "particularly",
    "subsequently",
)

CASUAL_MARKERS = (
    "lol",
    "lmao",
    "idk",
    "imo",
    "imho",
    "btw",
    "gonna",
    "wanna",
    "gotta",
    "kinda",
    "sorta",
    "yeah",
    "yep",
    "nah",
    "ok",
    "okay",
    "hey",
    "wow",
    "pretty",
    "really",
    "just",
    "like",
    "stuff",
    "things",
    "guys",
    "dude",
    "tbh",
    "rn",
    "bc",
    "cos",
    "cause",
    "whatever",
    "anyway",
    "gosh",
    "oops",
    "huh",
)

HEDGES = (
    "maybe",
    "perhaps",
    "possibly",
    "probably",
    "apparently",
    "seemingly",
    "somewhat",
    "fairly",
    "quite",
    "rather",
    "arguably",
)

CONTRACTION_TOKENS = (
    "i'm",
    "i've",
    "i'd",
    "i'll",
    "you're",
    "you've",
    "you'd",
    "you'll",
    "we're",
    "we've",
    "we'd",
    "we'll",
    "they're",
    "they've",
    "they'd",
    "they'll",
    "it's",
    "it'd",
    "it'll",
    "that's",
    "there's",
    "here's",
    "who's",
    "what's",
    "can't",
    "cannot",
    "won't",
    "don't",
    "doesn't",
    "didn't",
    "isn't",
    "aren't",
    "wasn't",
    "weren't",
    "haven't",
    "hasn't",
    "hadn't",
    "wouldn't",
    "shouldn't",
    "couldn't",
    "mustn't",
    "let's",
    "ain't",
)

FIRST_PERSON = {"i", "me", "my", "mine", "myself", "i'm", "i've", "i'd", "i'll"}
INCLUSIVE_WE = {"we", "us", "our", "ours", "ourselves", "we're", "we've", "we'd", "we'll"}
SECOND_PERSON = {"you", "your", "yours", "yourself", "you're", "you've", "you'd", "you'll"}
IMPERSONAL_ONE = {"one", "one's"}

SUFFIX_BINS = ("ing", "ed", "ly", "tion", "ness", "ment", "able", "ible")
