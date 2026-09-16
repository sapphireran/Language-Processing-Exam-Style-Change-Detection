import subprocess
import sys


def test_python_m_kerf_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "kerf", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "inspect" in result.stdout
    assert "score" in result.stdout
