"""CLI predict / evaluate / features on a tiny temp corpus."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from style_change.cli import main


class CliTests(unittest.TestCase):
    def test_predict_evaluate_features(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            problems = root / "problems"
            output = root / "out"
            problems.mkdir()
            (problems / "problem-1.txt").write_text(
                "I'm tired and I don't want to wait around here.\n\n"
                "The committee therefore declines the proposal without further review.\n",
                encoding="utf-8",
            )
            (problems / "truth-problem-1.json").write_text(
                json.dumps({"authors": 2, "changes": [1]}),
                encoding="utf-8",
            )

            buf = io.StringIO()
            with redirect_stdout(buf):
                code = main(["predict", "-i", str(problems), "-o", str(output)])
            self.assertEqual(code, 0)
            solution = json.loads((output / "solution-problem-1.json").read_text())
            self.assertEqual(list(solution.keys()), ["changes"])
            self.assertEqual(len(solution["changes"]), 1)

            buf = io.StringIO()
            with redirect_stdout(buf):
                code = main(["evaluate", "--gold", str(problems), "--pred", str(output)])
            self.assertEqual(code, 0)
            self.assertIn("macro-F1", buf.getvalue())

            buf = io.StringIO()
            with redirect_stdout(buf):
                code = main(["features", str(problems / "problem-1.txt")])
            self.assertEqual(code, 0)
            self.assertIn("contraction_rate", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
