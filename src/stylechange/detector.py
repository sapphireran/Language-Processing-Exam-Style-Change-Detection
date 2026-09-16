"""Mark style-change boundaries between consecutive units.

Two signals, used in that order:

1. **Voice jump.** After smoothing, a ``chat→textbook`` (or any other
   pair of named voices) is a change. This is the easy/medium exam story.
2. **Register distance.** Inside a run of the same voice, average binary
   flags (*I*, *we*, *one*, informal, notes, …) on each side of a
   candidate cut. Keep the strongest cut if it clears ``threshold``.
   That is the hard story: two academic authors, same topic, different
   habits (*we/our* vs *one/may*). Mean word length is *not* used here —
   it flips on a single long sentence.

Exam answers are written in contiguous blocks, so we do not flip a coin
at every sentence. We look for a small number of cuts, not a per-pair
classifier that ignores the rest of the document.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .features import FeatureVector, extract, register_distance, span_distance, top_deltas
from .tokenize import Granularity, segment
from .voices import classify_voice, cut_band, merge_singleton_runs, smooth_voices, voice_scores


@dataclass(frozen=True)
class Boundary:
    index: int
    score: float
    left_voice: str
    right_voice: str
    reason: str
    deltas: tuple[tuple[str, float, float, float], ...] = ()


@dataclass
class Detection:
    units: list[str]
    features: list[FeatureVector]
    voices: list[str]
    raw_voices: list[str]
    changes: list[int]
    boundaries: list[Boundary] = field(default_factory=list)
    granularity: str = "sentence"
    threshold: float = 1.00

    @property
    def n_authors(self) -> int:
        return 1 + sum(self.changes)

    def as_solution(self) -> dict[str, list[int]]:
        return {"changes": list(self.changes)}


def _voice_runs(voices: list[str]) -> list[tuple[int, int, str]]:
    """Inclusive-exclusive runs of an equal (possibly mixed) label."""
    if not voices:
        return []
    runs: list[tuple[int, int, str]] = []
    start = 0
    current = voices[0]
    for index, label in enumerate(voices[1:], start=1):
        if label != current:
            runs.append((start, index, current))
            start = index
            current = label
    runs.append((start, len(voices), current))
    return runs


def detect(
    text: str,
    *,
    granularity: Granularity = "auto",
    threshold: float = 1.00,
    min_span: int = 2,
) -> Detection:
    units = segment(text, granularity)
    features = [extract(unit) for unit in units]
    raw_voices = [classify_voice(vector) for vector in features]
    voices = merge_singleton_runs(smooth_voices(raw_voices))

    n_pairs = max(0, len(units) - 1)
    changes = [0] * n_pairs
    boundaries: list[Boundary] = []

    for index in range(n_pairs):
        left, right = voices[index], voices[index + 1]
        if left == "mixed" or right == "mixed":
            continue
        if cut_band(left) == cut_band(right):
            continue
        deltas = tuple(top_deltas(features[index], features[index + 1]))
        score = span_distance(features[max(0, index - 1) : index + 1], features[index + 1 : index + 3])
        changes[index] = 1
        boundaries.append(
            Boundary(
                index=index,
                score=max(score, 0.75),
                left_voice=left,
                right_voice=right,
                reason="voice",
                deltas=deltas,
            )
        )

    for start, end, voice in _voice_runs(voices):
        if end - start < min_span * 2:
            continue
        # Lecture notes are too short and too noisy for a second cut.
        if voice == "notes":
            continue
        best_k = -1
        best_score = -1.0
        for cut in range(start + min_span, end - min_span + 1):
            if cut - 1 < len(changes) and changes[cut - 1] == 1:
                continue
            score = register_distance(features[start:cut], features[cut:end])
            if score > best_score:
                best_score = score
                best_k = cut
        if best_k < 0 or best_score < threshold:
            continue
        index = best_k - 1
        if changes[index] == 1:
            continue
        deltas = tuple(top_deltas(features[index], features[index + 1]))
        changes[index] = 1
        boundaries.append(
            Boundary(
                index=index,
                score=best_score,
                left_voice=voices[index],
                right_voice=voices[index + 1],
                reason="span",
                deltas=deltas,
            )
        )

    boundaries.sort(key=lambda item: item.index)
    return Detection(
        units=units,
        features=features,
        voices=voices,
        raw_voices=raw_voices,
        changes=changes,
        boundaries=boundaries,
        granularity=granularity,
        threshold=threshold,
    )


def explain_lines(detection: Detection, *, width: int = 88) -> list[str]:
    """Pretty-print units and the join after each one."""
    lines: list[str] = [
        f"units:    {len(detection.units)}",
        f"changes:  {detection.changes}",
        f"authors~  {detection.n_authors}",
        f"voices:   {detection.voices}",
        "",
    ]
    by_index = {item.index: item for item in detection.boundaries}
    for index, unit in enumerate(detection.units):
        voice = detection.voices[index]
        preview = unit.replace("\n", " ")
        if len(preview) > width:
            preview = preview[: width - 1] + "…"
        lines.append(f"{index:2d}  [{voice:<8}] {preview}")
        if index >= len(detection.changes):
            continue
        flag = detection.changes[index]
        boundary = by_index.get(index)
        if flag and boundary:
            delta_txt = ", ".join(
                f"{name} {left:.2f}→{right:.2f}" for name, left, right, _ in boundary.deltas
            )
            lines.append(
                f"    -- CHANGE ({boundary.reason}, {boundary.score:.2f}) "
                f"{boundary.left_voice}→{boundary.right_voice}  {delta_txt}"
            )
        else:
            left = detection.features[index]
            right = detection.features[index + 1]
            score = span_distance([left], [right])
            lines.append(f"    -- same ({score:.2f})")
    return lines


def debug_scores(detection: Detection) -> list[str]:
    """Dump raw voice scores — useful when an example is mis-labelled."""
    rows = []
    for index, (unit, vector, raw, voice) in enumerate(
        zip(detection.units, detection.features, detection.raw_voices, detection.voices)
    ):
        scores = voice_scores(vector)
        packed = " ".join(f"{name[0]}={scores[name]:+.2f}" for name in ("chat", "student", "textbook", "notes"))
        preview = unit.replace("\n", " ")[:60]
        rows.append(f"{index:2d} raw={raw:<8} use={voice:<8} {packed}  {preview}")
    return rows
