from pathlib import Path

from splicefind.cli import main


def test_detect_json_roundtrip(tmp_path: Path, capsys):
    path = tmp_path / "problem.txt"
    path.write_text("Hello there, friend.\n\nOne must consider the alternative.\n", encoding="utf-8")
    assert main(["detect", str(path), "--json"]) == 0
    out = capsys.readouterr().out
    assert '"changes"' in out


def test_generate_and_score(tmp_path: Path, capsys):
    out = tmp_path / "split"
    assert main(["generate", "-o", str(out), "--easy", "2", "--medium", "1", "--hard", "1"]) == 0
    assert list(out.glob("problem-*.txt"))
    assert main(["score-corpus", str(out), "--threshold", "0.50"]) == 0
    logged = capsys.readouterr().out
    assert "macro F1" in logged
