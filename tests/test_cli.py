import json
from pathlib import Path

from stylechange.cli import main

DOC = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "documents"
    / "problem-medium-one-topic.txt"
)


def test_detect_json(capsys):
    assert main(["detect", str(DOC), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["changes"] == [0, 0, 0, 1, 0, 0, 0]
    assert payload["authors"] == 2


def test_features_lists_units(capsys):
    assert main(["features", str(DOC)]) == 0
    out = capsys.readouterr().out
    assert "8 sentence units" in out
    assert "first_person_ratio" in out


def test_evaluate_writes_solutions(tmp_path: Path, capsys):
    inp = Path(__file__).resolve().parents[1] / "examples" / "documents"
    out = tmp_path / "pred"
    assert main(["evaluate", str(inp), "--output", str(out)]) == 0
    printed = capsys.readouterr().out
    assert "macro-F1=" in printed
    solutions = list(out.glob("solution-problem-*.json"))
    assert len(solutions) >= 6


def test_generate_emits_truth(capsys):
    assert main(["generate", "--difficulty", "medium", "--seed", "4", "--id", "x"]) == 0
    out = capsys.readouterr().out
    assert '"changes"' in out
    assert "voices:" in out


def test_module_entrypoint_help(capsys):
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "stylechange", "detect", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "style-change" in result.stdout.lower() or "detect" in result.stdout
