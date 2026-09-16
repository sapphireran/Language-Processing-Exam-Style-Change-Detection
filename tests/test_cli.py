import json
from pathlib import Path

from seamtrace.cli import main
from seamtrace.corpus import DEFAULT_CORPUS, load_teaching_corpus


def test_inspect_zero(capsys) -> None:
    path = DEFAULT_CORPUS / "problem-01-ferns-solo.txt"
    assert main(["inspect", str(path)]) == 0
    out = capsys.readouterr().out
    assert "units=" in out
    assert "pair" in out.lower() or "score" in out.lower() or "label" in out


def test_solve_writes_pan_names(tmp_path: Path) -> None:
    src = tmp_path / "in"
    src.mkdir()
    sample = (DEFAULT_CORPUS / "problem-01-ferns-solo.txt").read_text(encoding="utf-8")
    (src / "problem-99.txt").write_text(sample, encoding="utf-8")
    out = tmp_path / "out"
    assert main(["solve", "-i", str(src), "-o", str(out)]) == 0
    dest = out / "solution-problem-99.json"
    payload = json.loads(dest.read_text(encoding="utf-8"))
    doc = next(d for d in load_teaching_corpus() if d.stem.endswith("ferns-solo"))
    assert len(payload["changes"]) == len(doc.changes)
    assert set(payload) == {"changes"}


def test_score_folder(capsys) -> None:
    assert main(["score", str(DEFAULT_CORPUS)]) == 0
    out = capsys.readouterr().out
    assert "TOTAL" in out
    assert "macro-F1" in out
