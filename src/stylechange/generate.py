"""Concatenate hand-written blocks and emit a gold ``changes`` array.

Used by tests and by ``examples/mix_blocks.py``. This is not a language
model: you pass the actual sentences, we only join them and mark the
joins between blocks as style changes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Block:
    voice: str
    units: tuple[str, ...]


def mix_blocks(*blocks: Block) -> tuple[str, list[int], list[str]]:
    """Return ``(document, changes, per-unit voices)``.

    ``changes[i]`` is 1 iff unit ``i`` and unit ``i+1`` come from
    different blocks. The document is one unit per line.
    """
    if not blocks:
        raise ValueError("mix_blocks() needs at least one block")
    units: list[str] = []
    voices: list[str] = []
    changes: list[int] = []
    for index, block in enumerate(blocks):
        if not block.units:
            raise ValueError(f"block {index} ({block.voice}) is empty")
        if units:
            changes.append(1)
        changes.extend([0] * (len(block.units) - 1))
        units.extend(block.units)
        voices.extend([block.voice] * len(block.units))
    return "\n".join(units) + "\n", changes, voices
