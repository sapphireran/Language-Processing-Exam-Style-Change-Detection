"""PAN-shaped problem / truth / solution files.

Teaching files in this repo follow the same contract as the shared
task so exam answers can talk about `changes` arrays without
switching formats. No shared-task text is stored here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .units import split_units


@dataclass(frozen=True)
class Problem:
    path: Path
    units: list[str]
    text: str

    @property
    def n_pairs(self) -> int:
        return max(0, len(self.units) - 1)


def load_problem(path: str | Path, *, mode: str = "auto") -> Problem:
    p = Path(path)
    # newline="" matches the PAN reading note and keeps \r intact.
    text = p.read_text(encoding="utf-8", newline="")
    return Problem(path=p, units=split_units(text, mode=mode), text=text)


def load_truth(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "changes" not in data:
        raise ValueError(f"{path} has no 'changes' key")
    changes = [int(x) for x in data["changes"]]
    authors = int(data.get("authors", 1 + sum(changes)))
    return {"authors": authors, "changes": changes, "raw": data}


def write_solution(path: str | Path, changes: list[int]) -> None:
    Path(path).write_text(
        json.dumps({"changes": [int(x) for x in changes]}, indent=2) + "\n",
        encoding="utf-8",
    )


def guess_truth_path(problem_path: str | Path) -> Path | None:
    p = Path(problem_path)
    candidates = [
        p.with_name(f"truth-{p.name}").with_suffix(".json"),
        p.parent / "truth" / f"truth-{p.stem}.json",
        p.parent / "truth" / f"{p.stem}.json",
        p.parent / f"truth-{p.stem}.json",
    ]
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def iter_problems(root: str | Path) -> list[Path]:
    folder = Path(root)
    files = sorted(folder.glob("problem-*.txt"))
    if files:
        return files
    return sorted(folder.glob("*.txt"))
