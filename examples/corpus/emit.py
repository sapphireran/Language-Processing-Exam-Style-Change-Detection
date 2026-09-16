"""Write problem text, truth JSON, and a manifest from the bank."""

from __future__ import annotations

import json
from pathlib import Path

from examples.corpus.bank import DOCUMENTS, authors_for, changes_for

HERE = Path(__file__).resolve().parent


def problem_name(doc) -> str:
    return f"problem-{doc['ident']:02d}-{doc['slug']}.txt"


def truth_name(doc) -> str:
    return f"truth-problem-{doc['ident']:02d}.json"


def render_text(doc) -> str:
    return "\n\n".join(block["text"] for block in doc["blocks"]) + "\n"


def truth_payload(doc) -> dict:
    changes = changes_for(doc)
    return {
        "authors": authors_for(doc),
        "changes": changes,
        "houses": [block["house"] for block in doc["blocks"]],
        "topics": [block["topic"] for block in doc["blocks"]],
        "difficulty": doc["difficulty"],
        "title": doc["title"],
        "holdout": doc["holdout"],
        "slug": doc["slug"],
    }


def emit(folder: Path | None = None) -> list[Path]:
    folder = folder or HERE
    folder.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    manifest = []
    for doc in DOCUMENTS:
        text_path = folder / problem_name(doc)
        truth_path = folder / truth_name(doc)
        text_path.write_text(render_text(doc), encoding="utf-8", newline="\n")
        payload = truth_payload(doc)
        truth_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        written.extend([text_path, truth_path])
        manifest.append(
            {
                "id": doc["ident"],
                "slug": doc["slug"],
                "file": text_path.name,
                "truth": truth_path.name,
                "difficulty": doc["difficulty"],
                "holdout": doc["holdout"],
                "authors": payload["authors"],
                "changes": payload["changes"],
                "houses": payload["houses"],
                "n_units": len(doc["blocks"]),
            }
        )
    man_path = folder / "manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    written.append(man_path)
    return written


def main() -> None:
    paths = emit()
    print(f"wrote {len(paths)} files")


if __name__ == "__main__":
    main()
