"""Synthetic exam-answer generator with known style-change labels.

The voices are exaggerated on purpose. That is useful for:

* unit tests that must stay green without a neural model
* README walkthroughs that show *why* a boundary fired
* threshold calibration when you do not have the PAN zip files locally
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import random
from typing import Sequence

from .io import Solution

TOPICS = (
    "n-grams",
    "part-of-speech tagging",
    "constituency parsing",
    "vector semantics",
    "coreference",
    "morphology",
)


@dataclass(frozen=True)
class GeneratedDocument:
    problem_id: str
    text: str
    units: list[str]
    authors: list[str]
    truth: Solution
    difficulty: str


def _textbook(topic: str, rng: random.Random) -> list[str]:
    catalog = {
        "n-grams": [
            "An n-gram language model estimates the probability of a token given a bounded history of preceding tokens.",
            "Therefore the chain rule is approximated by a Markov assumption of order n minus one.",
            "Moreover, add-one smoothing redistributes probability mass so that unseen n-grams receive a non-zero estimate.",
            "Consequently, perplexity on a held-out corpus is the conventional intrinsic evaluation of such a model.",
        ],
        "part-of-speech tagging": [
            "Part-of-speech tagging assigns a morphosyntactic category to each token in a running text.",
            "A hidden Markov model therefore treats tags as latent states and words as emissions.",
            "The Viterbi algorithm subsequently recovers the most probable tag sequence in linear time relative to the tagset.",
            "Nevertheless, contextual ambiguity remains, particularly among verbs, nouns, and gerunds.",
        ],
        "constituency parsing": [
            "A constituency parser recovers nested phrase-structure trees licensed by a context-free grammar.",
            "Chomsky normal form is frequently imposed so that dynamic programming remains cubic in sentence length.",
            "The CKY algorithm thus fills a chart of spans with weighted non-terminals.",
            "Accordingly, the highest-scoring tree is recovered by pointer traversal from the root cell.",
        ],
        "vector semantics": [
            "Distributional semantics represents lexical meaning as a vector derived from co-occurrence statistics.",
            "Thus words that occur in similar contexts obtain similar embeddings.",
            "Cosine similarity is the conventional geometric proxy for relatedness in that space.",
            "However, static embeddings cannot distinguish the several senses of an ambiguous token.",
        ],
        "coreference": [
            "Coreference resolution clusters mentions that refer to the same discourse entity.",
            "Mention detection is therefore a prerequisite, after which pairwise or higher-order clustering is applied.",
            "Features of gender, number, and syntactic command remain informative even in neural systems.",
            "Consequently, evaluation reports MUC, B-cubed, and CEAF scores rather than a single accuracy figure.",
        ],
        "morphology": [
            "Morphological analysis decomposes surface forms into stems and inflectional or derivational affixes.",
            "Finite-state transducers are therefore a classical implementation of concatenative morphology.",
            "Nevertheless, non-concatenative processes such as templatic morphology complicate a purely concatenative account.",
            "A gold analysis typically records lemma, part of speech, and a structured feature bundle.",
        ],
    }
    pool = list(catalog[topic])
    rng.shuffle(pool)
    return pool[:3]


def _student(topic: str, rng: random.Random) -> list[str]:
    catalog = {
        "n-grams": [
            "I keep mixing up bigrams and trigrams when I'm in a hurry.",
            "It's basically just 'what word comes next' with a tiny memory window.",
            "Smoothing feels like a hack, but I get why we can't leave unseen stuff at zero.",
            "If the history is too long the counts get ridiculously sparse, right?",
        ],
        "part-of-speech tagging": [
            "POS tagging is the one where we slap NNP or VB on every word.",
            "I'm never sure about 'flying planes' — is flying a verb or an adjective here?",
            "HMM + Viterbi is the exam answer they want, even if BERT would crush it.",
            "Yeah the tagset size matters a lot and I always forget the exact number for PTB.",
        ],
        "constituency parsing": [
            "Okay so parsing is drawing those nested trees from syntax class.",
            "CKY is the chart one — I drew it in the margin and it still looks messy.",
            "If the grammar isn't in Chomsky normal form I just panic a little.",
            "I keep writing NP -> Det N and hoping the rest of the tree forgives me.",
        ],
        "vector semantics": [
            "Word vectors are the 'you shall know a word by the company it keeps' thing.",
            "I always picture king - man + woman and hope the joke still lands.",
            "Cosine is just the angle, not the raw distance, which I definitely mixed up once.",
            "Static vectors can't do bank-the-river vs bank-the-money and that's the whole point.",
        ],
        "coreference": [
            "Coreference is when 'she' and 'the linguist' are the same person.",
            "I always lose points for missing the singleton mentions.",
            "Pronouns are easy-ish; the company names and 'the former' are not.",
            "There's like three metrics and I can never remember which one is B-cubed.",
        ],
        "morphology": [
            "Morphology is stems and affixes — un-happi-ness and all that.",
            "I still trip over irregular verbs because they refuse to play nice.",
            "FSTs sound fancy but they're basically a tidy way to generate forms.",
            "Don't ask me to gloss a Semitic template on no sleep.",
        ],
    }
    pool = list(catalog[topic])
    rng.shuffle(pool)
    return pool[:3]


def _notes(topic: str, rng: random.Random) -> list[str]:
    catalog = {
        "n-grams": [
            "n-gram: P(w_i | w_{i-n+1}..w_{i-1}).",
            "Markov order = n-1 — sparse counts — add-k / Kneser-Ney.",
            "eval: perplexity; lower = tighter predictive fit.",
            "OOV: open vocab + unk bucket or subword fallback.",
        ],
        "part-of-speech tagging": [
            "POS: token -> tag. HMM: t_i -> t_{i+1}, t_i -> w_i.",
            "Viterbi: max path, not sum. Forward = likelihood.",
            "confusions: NN/NNP, VB/VBG, IN/RP.",
            "beam / greedy left-to-right if Viterbi too slow.",
        ],
        "constituency parsing": [
            "CFG + CNF. CKY: spans [i,j], binary split k.",
            "score(A -> B C) + score(left) + score(right).",
            "unary closures first, then binary split.",
            "eval: PARSEVAL bracketing F1, not exact-tree.",
        ],
        "vector semantics": [
            "co-occur matrix -> PMI / SVD or skip-gram / CBOW.",
            "cosine(sim); analogy = vector offset.",
            "static vs contextual: one vector vs one-per-token.",
            "bias in corpora survives the linear algebra.",
        ],
        "coreference": [
            "mentions -> clusters. anaphor + antecedent.",
            "constraints: number/gender/c-command.",
            "metrics: MUC / B3 / CEAF; report the average.",
            "end-to-end now: span scores + pairwise.",
        ],
        "morphology": [
            "lemma + feats. concat vs templatic.",
            "FST: upper lemma, lower surface.",
            "irregulars: listed exceptions, not rules.",
            "eval: full-form accuracy + feature-wise F1.",
        ],
    }
    pool = list(catalog[topic])
    rng.shuffle(pool)
    return pool[:3]


VOICES = {
    "textbook": _textbook,
    "student": _student,
    "notes": _notes,
}


def _assemble(blocks: Sequence[tuple[str, list[str]]]) -> GeneratedDocument:
    units: list[str] = []
    authors: list[str] = []
    for voice, sentences in blocks:
        units.extend(sentences)
        authors.extend([voice] * len(sentences))
    changes = [0 if authors[i] == authors[i + 1] else 1 for i in range(len(authors) - 1)]
    unique_authors = len(set(authors))
    text = "\n".join(units) + "\n"
    return GeneratedDocument(
        problem_id="tmp",
        text=text,
        units=units,
        authors=authors,
        truth=Solution(changes=changes, authors=unique_authors),
        difficulty="unspecified",
    )


def generate_document(
    *,
    difficulty: str = "easy",
    seed: int | None = None,
    problem_id: str = "gen",
) -> GeneratedDocument:
    """Build one labelled exam-style document.

    * **easy** — topic *and* voice change together
    * **medium** — one topic, two clearly different voices
    * **hard** — one topic, textbook vs lecture-notes (closer registers)
    * **single** — one voice, no change
    """
    rng = random.Random(seed)
    difficulty = difficulty.lower()
    if difficulty == "single":
        topic = rng.choice(TOPICS)
        voice = rng.choice(list(VOICES))
        blocks = [(voice, VOICES[voice](topic, rng))]
    elif difficulty == "easy":
        topics = rng.sample(list(TOPICS), 3)
        voices = rng.sample(list(VOICES), 3)
        blocks = [(voice, VOICES[voice](topic, rng)) for voice, topic in zip(voices, topics)]
    elif difficulty == "medium":
        topic = rng.choice(TOPICS)
        voices = ["textbook", "student"]
        rng.shuffle(voices)
        blocks = [(voice, VOICES[voice](topic, rng)) for voice in voices]
    elif difficulty == "hard":
        topic = rng.choice(TOPICS)
        voices = ["textbook", "notes"]
        rng.shuffle(voices)
        blocks = [(voice, VOICES[voice](topic, rng)) for voice in voices]
    else:
        raise ValueError(f"unknown difficulty: {difficulty}")

    document = _assemble(blocks)
    return GeneratedDocument(
        problem_id=problem_id,
        text=document.text,
        units=document.units,
        authors=document.authors,
        truth=document.truth,
        difficulty=difficulty,
    )


def generate_split(
    *,
    n_per_level: int = 8,
    seed: int = 7,
    prefix: str = "synth",
) -> list[GeneratedDocument]:
    """A tiny train-like split across the four difficulty tags."""
    documents: list[GeneratedDocument] = []
    counter = itertools.count(1)
    rng = random.Random(seed)
    for difficulty in ("easy", "medium", "hard", "single"):
        for _ in range(n_per_level):
            pid = f"{prefix}-{next(counter):03d}"
            documents.append(
                generate_document(
                    difficulty=difficulty,
                    seed=rng.randint(0, 10_000_000),
                    problem_id=pid,
                )
            )
    return documents
