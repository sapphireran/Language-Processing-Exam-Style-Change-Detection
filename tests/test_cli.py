from pathlib import Path

from stylechange.cli import main

ROOT = Path(__file__).resolve().parents[1]
TAKEHOME = ROOT / "examples" / "documents" / "problem-exam-takehome.txt"
DOCS = ROOT / "examples" / "documents"


def test_detect_help():
    try:
        main(["detect", "--help"])
    except SystemExit as exc:
        assert exc.code == 0


def test_detect_prints_changes(capsys):
    assert main(["detect", str(TAKEHOME)]) == 0
    out = capsys.readouterr().out
    assert "changes:" in out
    assert "[0, 0, 1, 0, 0, 0, 1, 0, 0]" in out


def test_detect_json(capsys):
    assert main(["detect", str(TAKEHOME), "--json"]) == 0
    assert '"changes"' in capsys.readouterr().out


def test_evaluate_collection(capsys):
    assert main(["evaluate", str(DOCS)]) == 0
    out = capsys.readouterr().out
    assert "macro-F1=1.000" in out
    assert "exact=8/8" in out


def test_module_entry_help():
    # Imported by python -m stylechange; just check the parser lives.
    from stylechange.cli import build_parser

    parser = build_parser()
    assert parser.parse_args(["detect", "--help".replace("--help", str(TAKEHOME))]).command == "detect"
