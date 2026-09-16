from pathlib import Path

from style_change.cli import main

ROOT = Path(__file__).resolve().parents[1]
MIXED = ROOT / "examples" / "documents" / "mixed_formal_casual.txt"
LABELS = ROOT / "examples" / "documents" / "labels" / "mixed_formal_casual.json"


def test_detect_json_and_evaluate(capsys) -> None:
    assert main(["detect", "--json", str(MIXED)]) == 0
    out = capsys.readouterr().out
    assert "multi_author" in out
    assert main(["evaluate", str(MIXED), str(LABELS)]) == 0
    ev = capsys.readouterr().out
    assert "Task 1" in ev
    assert main(["features", str(MIXED)]) == 0
    feats = capsys.readouterr().out
    assert "words_per_sentence" in feats
