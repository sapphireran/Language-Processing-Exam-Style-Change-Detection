"""Text reports and optional matplotlib plots of adjacent distances."""

from __future__ import annotations

from pathlib import Path

from style_change.detectors import DetectionResult
from style_change.features import DETECTION_FEATURES, STYLE_AXIS_NAMES, FeatureTable, describe_features
from style_change.tokenize import Document


def sparkline(values: list[float], width: int = 40) -> str:
    if not values:
        return ""
    glyphs = "▁▂▃▄▅▆▇█"
    lo = min(values)
    hi = max(values)
    span = hi - lo if hi > lo else 1.0
    chars = []
    for value in values:
        idx = int(round((value - lo) / span * (len(glyphs) - 1)))
        chars.append(glyphs[idx])
    return "".join(chars)


def format_report(
    document: Document,
    table: FeatureTable,
    result: DetectionResult,
    preview_chars: int = 88,
) -> str:
    lines = [
        f"source: {document.source or '<string>'}",
        f"paragraphs: {len(document.paragraphs)}  scored: {len(result.paragraph_indices)}",
        f"multi-author: {result.multi_author}  threshold: {result.threshold:.3f}",
        f"authors: {result.authors}",
        f"changes after paragraphs: {result.change_positions}",
        f"distances: {[round(x, 3) for x in result.distances]}",
        f"distance sparkline: {sparkline(result.distances)}",
    ]
    if result.axes:
        lines.extend(["", "style axes (formality, address, rhythm, procedure)"])
        header = "para " + " ".join(f"{name:>12}" for name in STYLE_AXIS_NAMES)
        lines.append(header)
        for index, axis in zip(result.paragraph_indices, result.axes, strict=True):
            values = " ".join(f"{value:12.3f}" for value in axis)
            lines.append(f"{index:>4} {values}")
    lines.extend(
        [
            "",
            describe_features(table),
            "",
            "paragraph preview",
        ]
    )
    for paragraph in document.paragraphs:
        snippet = paragraph.text.replace("\n", " ")
        if len(snippet) > preview_chars:
            snippet = snippet[: preview_chars - 3] + "..."
        author = ""
        if paragraph.index in result.paragraph_indices:
            pos = result.paragraph_indices.index(paragraph.index)
            author = f"  author={result.authors[pos]}"
        lines.append(f"  [{paragraph.index}]{author}  {snippet}")
    if result.notes:
        lines.append("")
        lines.extend(f"note: {note}" for note in result.notes)
    if table.matrix.shape[0] >= 2:
        lines.append("")
        lines.append("largest core-feature gaps between adjacent scored paragraphs")
        core = table.subset(DETECTION_FEATURES) if DETECTION_FEATURES[0] in table.names else table
        for left in range(core.matrix.shape[0] - 1):
            right = left + 1
            gaps = core.top_differences(left, right, k=5)
            marker = "CHANGE" if left < len(result.changes) and result.changes[left] else "same"
            lines.append(
                f"  {table.paragraph_indices[left]} -> {table.paragraph_indices[right]} [{marker}]"
            )
            for name, a, b, delta in gaps:
                lines.append(f"      {name:24} {a:8.4f} vs {b:8.4f}  |z|={delta:.2f}")
    return "\n".join(lines)


def plot_distances(result: DetectionResult, path: str | Path) -> Path:
    """Save a simple adjacent-distance plot. Requires matplotlib."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:  # pragma: no cover - optional extra
        raise RuntimeError("matplotlib is required for plot_distances") from exc

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    xs = list(range(len(result.distances)))
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(xs, result.distances, marker="o", color="#1f4e79")
    ax.axhline(result.threshold, color="#b42318", linestyle="--", label=f"threshold {result.threshold:.2f}")
    for i, changed in enumerate(result.changes):
        if changed:
            ax.scatter([i], [result.distances[i]], s=80, color="#b42318", zorder=3)
    ax.set_xlabel("Boundary after paragraph")
    ax.set_ylabel("Euclidean distance in 4-D style space")
    ax.set_title("Adjacent style distance")
    ax.legend(loc="best")
    ax.set_xticks(xs)
    fig.tight_layout(pad=1.2)
    fig.savefig(destination, dpi=140)
    plt.close(fig)
    return destination
