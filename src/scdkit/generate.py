"""Tiny author-bank mixer for extra exam drills.

The bundled documents are hand-written. This generator only restacks
those banks (or any JSON author card) so you can build A-B-A patterns
without inventing new prose under time pressure.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .evaluate import gold_from_authors
from .io import Truth, dump_document, dump_truth


@dataclass(frozen=True)
class AuthorCard:
    name: str
    register: str
    notes: str
    paragraphs: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AuthorCard":
        paras = payload.get("paragraphs") or []
        if not paras:
            raise ValueError("author card needs paragraphs")
        return cls(
            name=str(payload.get("name", "anon")),
            register=str(payload.get("register", "unknown")),
            notes=str(payload.get("notes", "")),
            paragraphs=tuple(str(p).strip() for p in paras if str(p).strip()),
        )


def load_author_card(path: str | Path) -> AuthorCard:
    return AuthorCard.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def load_author_bank(directory: str | Path) -> list[AuthorCard]:
    cards = []
    for path in sorted(Path(directory).glob("*.json")):
        cards.append(load_author_card(path))
    return cards


def mix_document(
    cards: list[AuthorCard],
    pattern: str,
    rng: random.Random | None = None,
) -> tuple[str, Truth]:
    """``pattern`` is a string of author letters, e.g. ``AABBA`` or ``ABA``."""
    rng = rng or random.Random(0)
    if not pattern or not pattern.isalpha():
        raise ValueError("pattern must be letters like AABBC")
    letters = [ch.upper() for ch in pattern]
    unique = list(dict.fromkeys(letters))
    if len(unique) > len(cards):
        raise ValueError(f"pattern needs {len(unique)} authors, have {len(cards)}")
    assigned = {letter: cards[i] for i, letter in enumerate(unique)}
    used: dict[str, set[int]] = {letter: set() for letter in unique}
    paragraphs: list[str] = []
    authors: list[int] = []
    for letter in letters:
        card = assigned[letter]
        available = [i for i in range(len(card.paragraphs)) if i not in used[letter]]
        if not available:
            used[letter].clear()
            available = list(range(len(card.paragraphs)))
        idx = rng.choice(available)
        used[letter].add(idx)
        paragraphs.append(card.paragraphs[idx])
        authors.append(unique.index(letter) + 1)
    text = "\n\n".join(paragraphs)
    truth = Truth(
        changes=tuple(gold_from_authors(authors)),
        authors=len(unique),
        paragraph_authors=tuple(authors),
        title=f"mixed:{pattern}",
        notes=" / ".join(assigned[l].name for l in unique),
        difficulty="generated",
    )
    return text, truth


def write_mix(
    cards: list[AuthorCard],
    pattern: str,
    dest_dir: str | Path,
    stem: str,
    seed: int = 0,
) -> tuple[Path, Path]:
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    text, truth = mix_document(cards, pattern, rng=random.Random(seed))
    doc = dest / f"{stem}.txt"
    gold = dest / f"truth-{stem}.json"
    dump_document(doc, text)
    dump_truth(gold, truth)
    return doc, gold
