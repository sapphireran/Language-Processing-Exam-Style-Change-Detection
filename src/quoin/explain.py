"""Plain-language boundary explanations for revision, not for a paper."""

from __future__ import annotations

from .detectors import BoundaryScore, QuoinDetector
from .features import vectorize
from .io import Problem
from .tokenize import word_count


def _channel_note(row: BoundaryScore) -> str:
    parts = [
        ("ncd", row.ncd),
        ("char-3gram", row.char_cosine),
        ("function-word L1", row.function_l1),
        ("shape L1", row.shape_l1),
        ("register L1", row.register_l1),
    ]
    parts.sort(key=lambda item: item[1], reverse=True)
    leader = parts[0]
    return f"loudest channel: {leader[0]} ({leader[1]:.3f})"


def explain_document(problem: Problem, detector: QuoinDetector | None = None) -> str:
    detector = detector or QuoinDetector()
    rows = detector.boundaries(problem.paragraphs)
    lines = [
        f"# {problem.path.name}",
        "",
        f"paragraphs: {problem.n_paragraphs}    boundaries: {problem.n_boundaries}",
        f"threshold: {detector.threshold:.2f}   rel-margin: {detector.rel_margin:.2f}   floor: {detector.floor:.2f}",
        "",
    ]
    for row in rows:
        left = problem.paragraphs[row.index]
        right = problem.paragraphs[row.index + 1]
        left_vec = vectorize(left)
        right_vec = vectorize(right)
        mark = "CHANGE" if row.pred else "same"
        lines.extend(
            [
                f"## boundary {row.index} → {row.index + 1}   [{mark}]  quoin={row.quoin:.3f}",
                f"- words: {word_count(left)} / {word_count(right)}",
                f"- mean sentence: {left_vec.shape['mean_sentence']:.1f} / "
                f"{right_vec.shape['mean_sentence']:.1f}",
                f"- contraction rate: {left_vec.shape['contraction']:.3f} / "
                f"{right_vec.shape['contraction']:.3f}",
                f"- formal-marker rate: {left_vec.shape['formal']:.3f} / "
                f"{right_vec.shape['formal']:.3f}",
                f"- informal-marker rate: {left_vec.shape['informal']:.3f} / "
                f"{right_vec.shape['informal']:.3f}",
                f"- NCD {row.ncd:.3f}   char-cosine {row.char_cosine:.3f}   "
                f"function L1 {row.function_l1:.3f}   shape L1 {row.shape_l1:.3f}   "
                f"register L1 {row.register_l1:.3f}",
                f"- residual vs document median: {row.residual:+.3f}",
                f"- {_channel_note(row)}",
                "",
            ]
        )
    return "\n".join(lines)
