import json
from pathlib import Path

from examscd.cli import main

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "examples" / "documents" / "02_recipe_then_maillard.txt"
TRUTH = ROOT / "examples" / "documents" / "truth" / "02_recipe_then_maillard.json"


def test_detect_explain_exits_zero(capsys) -> None:
    assert main(["detect", str(RECIPE), "--explain"]) == 0
    out = capsys.readouterr().out
    assert "changes:" in out
    assert "CHANGE" in out


def test_evaluate_prints_macro_f1(capsys) -> None:
    assert main(["evaluate", str(RECIPE), str(TRUTH)]) == 0
    out = capsys.readouterr().out
    assert "macro-F1:" in out


def test_cusum_and_compare_and_features(capsys, tmp_path) -> None:
    svg = tmp_path / "cusum.svg"
    assert main(["cusum", str(RECIPE), "--svg", str(svg)]) == 0
    assert svg.exists()
    assert "<svg" in svg.read_text(encoding="utf-8")
    assert main(["compare", str(RECIPE), str(TRUTH)]) == 0
    assert main(["features", str(RECIPE)]) == 0
    out = capsys.readouterr().out
    assert "char-3gram cosine" in out
    assert "mean_word_len" in out


def test_detect_writes_pan_json(tmp_path) -> None:
    dest = tmp_path / "out.json"
    assert main(["detect", str(RECIPE), "-o", str(dest)]) == 0
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["changes"] == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
