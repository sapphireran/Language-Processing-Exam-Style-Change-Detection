import json

from quoin.cli import main


def test_cli_score_exits_zero(capsys):
    assert main(["score", "examples/corpus"]) == 0
    out = capsys.readouterr().out
    assert "macro" in out.lower() or "MACRO" in out


def test_cli_predict_prints_json(capsys):
    assert main(["predict", "examples/corpus/problem-27-solo-press.txt"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["changes"] == [0, 0, 0]


def test_cli_ncd_on_two_literals(capsys):
    assert main(["ncd", "the same locked forme", "pursuant to ordinance shall"]) == 0
    out = capsys.readouterr().out
    assert "NCD" in out


def test_cli_baselines(capsys):
    assert main(["baselines", "examples/corpus"]) == 0
    assert "never-fire" in capsys.readouterr().out
