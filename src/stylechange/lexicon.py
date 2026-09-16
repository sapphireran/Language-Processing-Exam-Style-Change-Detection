"""Closed-class lists used by the stylometric extractor.

Keep these short and hand-audited. Adding content nouns here would turn
the detector into a topic model.
"""

from __future__ import annotations

FUNCTION_WORDS = frozenset(
    """
    a an the
    i me my mine myself we us our ours ourselves
    you your yours yourself yourselves
    he him his himself she her hers herself
    they them their theirs themselves it its itself
    this that these those
    who whom whose which what
    am is are was were be been being
    have has had having
    do does did doing
    will would shall should may might must can could
    of to in for on with at by from as into about
    than then there here when where why how
    not no nor
    and but or so yet
    if because although while unless whereas since though
    """.split()
)

FIRST_PERSON = frozenset("i me my mine myself we us our ours ourselves".split())
SECOND_PERSON = frozenset("you your yours yourself yourselves".split())
THIRD_PERSON = frozenset(
    "he him his himself she her hers herself they them their theirs themselves it its itself".split()
)
ARTICLES = frozenset("a an the".split())
COORD_CONJ = frozenset("and but or nor yet so".split())
SUBORD_MARKERS = frozenset(
    "because although while if unless whereas since though whenever wherever whether".split()
)

HEDGES = frozenset(
    """
    however perhaps maybe somewhat relatively apparently seemingly
    roughly approximately fairly arguably generally typically likely
    possible possibly probable probably suggest suggests suggested
    appear appears appeared seeming modest modestly slight slightly
    tend tends tended often usually
    although whereas
    """.split()
)

INTENSIFIERS = frozenset(
    "very really extremely quite pretty super incredibly unusually highly totally".split()
)

BE_FORMS = frozenset("be been being is are was were am".split())

NOMINAL_SUFFIXES = ("tion", "sion", "ment", "ness", "ity")
LATINATE_SUFFIXES = ("ate", "ive", "ous", "ence", "ance", "ure")
LY_STOP = frozenset("only really early likely daily".split())

CONTRACTION_TAILS = (
    "n't",
    "n'T",
    "'re",
    "'RE",
    "'ll",
    "'LL",
    "'ve",
    "'VE",
    "'d",
    "'D",
    "'m",
    "'M",
    "'s",
    "'S",
)

# Abbreviations protected before running-prose sentence splits.
ABBREVIATIONS = (
    "Mr",
    "Mrs",
    "Ms",
    "Dr",
    "Prof",
    "Sr",
    "Jr",
    "vs",
    "etc",
    "approx",
    "fig",
    "al",
    "St",
    "Ave",
    "Inc",
    "Ltd",
    "No",
    "Vol",
    "pp",
    "cf",
)
