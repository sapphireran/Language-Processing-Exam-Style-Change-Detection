"""Closed-class word lists used as style markers.

Function words are weakly coupled to topic, so they remain useful when
easy topic cues disappear. The lists are short on purpose: an exam answer
should be able to name the categories and a handful of examples.
"""

from __future__ import annotations

FUNCTION_WORDS = frozenset(
    """
    a an the
    i me my mine myself we us our ours ourselves
    you your yours yourself yourselves
    he him his himself she her hers herself
    it its itself they them their theirs themselves
    this that these those
    who whom whose which what
    am is are was were be been being
    have has had having
    do does did doing done
    can could may might must shall should will would
    about above across after against along among around at
    before behind below beneath beside between beyond by
    down during except for from in inside into near of off
    on onto out outside over through throughout to toward
    under until up upon with within without
    and but or nor so yet
    although because if since though unless until while
    both either neither not only
    also just even still already
    """.split()
)

PERSONAL_PRONOUNS = frozenset(
    """
    i me my mine myself we us our ours ourselves
    you your yours yourself yourselves
    he him his himself she her hers herself
    it its itself they them their theirs themselves
    """.split()
)

FIRST_PERSON = frozenset("i me my mine myself we us our ours ourselves".split())

ARTICLES = frozenset("a an the".split())

PREPOSITIONS = frozenset(
    """
    about above across after against along among around at
    before behind below beneath beside between beyond by
    down during except for from in inside into near of off
    on onto out outside over through throughout to toward
    under until up upon with within without
    """.split()
)

HEDGES = frozenset(
    """
    maybe perhaps might may seems seem seemingly
    possibly probably apparently roughly approximately
    somewhat fairly rather quite
    """.split()
)

INTENSIFIERS = frozenset(
    """
    very really extremely totally incredibly super so
    absolutely completely utterly highly
    """.split()
)

CONNECTIVES = frozenset(
    """
    therefore however moreover furthermore nevertheless
    nonetheless consequently meanwhile otherwise instead
    thus hence accordingly
    """.split()
)
