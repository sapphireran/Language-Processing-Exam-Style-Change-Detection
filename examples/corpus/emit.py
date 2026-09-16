"""Write PAN-shaped problem/truth files from bank.py."""

from __future__ import annotations

import json
from pathlib import Path

from examples.corpus.bank import DOCUMENTS


def emit(root: str | Path | None = None) -> list[Path]:
    root = Path(root) if root else Path(__file__).resolve().parent
    written: list[Path] = []
    manifest: list[dict[str, object]] = []
    for doc in DOCUMENTS:
        text_path = root / f"problem-{doc.id}.txt"
        truth_path = root / f"truth-problem-{doc.code}.json"
        text_path.write_text("\n\n".join(doc.paragraphs) + "\n", encoding="utf-8")
        payload = {
            "changes": list(doc.changes),
            "authors": len(set(doc.houses)),
            "houses": list(doc.houses),
            "band": doc.band,
            "holdout": doc.holdout,
        }
        truth_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        written.extend([text_path, truth_path])
        manifest.append(
            {
                "id": doc.id,
                "code": doc.code,
                "band": doc.band,
                "houses": list(doc.houses),
                "topics": list(doc.topics),
                "n_paragraphs": len(doc.paragraphs),
                "changes": list(doc.changes),
                "holdout": doc.holdout,
                "note": doc.note,
                "problem": text_path.name,
                "truth": truth_path.name,
            }
        )
    man_path = root / "manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    written.append(man_path)
    return written


if __name__ == "__main__":
    paths = emit()
    print(f"wrote {len(paths)} files")
