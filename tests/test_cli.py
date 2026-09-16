from kerf.cli import main


def test_inspect_hard_exits_zero(capsys) -> None:
    code = main(["inspect", "examples/corpus/problem-16-stilling-caliper-then-seminar.txt"])
    assert code == 0
    out = capsys.readouterr().out
    assert "predicted authors" in out
    assert "CHANGE" in out


def test_score_prints_never_fire(capsys) -> None:
    code = main(["score", "examples/corpus"])
    assert code == 0
    out = capsys.readouterr().out
    assert "never-fire" in out
    assert "kerf" in out
