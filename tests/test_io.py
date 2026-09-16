import json
from pathlib import Path

from examscd.io import read_text, read_truth, write_solution


def test_write_and_read_roundtrip(tmp_path: Path) -> None:
    dest = tmp_path / "sol.json"
    write_solution(dest, [0, 1, 0], authors=[1, 1, 2, 2], extra={"note": "toy"})
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["changes"] == [0, 1, 0]
    assert payload["authors"] == [1, 1, 2, 2]
    assert payload["note"] == "toy"
    truth = read_truth(dest)
    assert truth.changes == [0, 1, 0]
    assert truth.authors == [1, 1, 2, 2]


def test_read_text_keeps_utf8(tmp_path: Path) -> None:
    path = tmp_path / "note.txt"
    path.write_text("café — 140 °C\n", encoding="utf-8")
    assert "café" in read_text(path)
