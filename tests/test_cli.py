import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "scdkit", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def test_detect_json() -> None:
    proc = _run("detect", "examples/documents/01_single_ferns.txt")
    payload = json.loads(proc.stdout)
    assert payload["changes"] == [0, 0]


def test_eval_prints_macro() -> None:
    proc = _run(
        "eval",
        "examples/documents",
        "--truth",
        "examples/documents/truth",
    )
    assert "macro-F1 1.000" in proc.stdout


def test_features_lists_paragraphs() -> None:
    proc = _run("features", "examples/documents/07_return_ferry.txt")
    assert proc.stdout.count("P") >= 3
