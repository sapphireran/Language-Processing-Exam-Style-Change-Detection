"""CLI smoke tests against the teaching corpus."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scarfjoint.cli import main

CORPUS = Path(__file__).resolve().parents[1] / "examples" / "corpus"
EASY = CORPUS / "easy" / "problem-01-ferry-marsh-knit.txt"


class CliTests(unittest.TestCase):
    def test_split_counts_paragraphs(self) -> None:
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["split", str(EASY)])
        self.assertEqual(code, 0)
        self.assertIn("paragraphs=6", buf.getvalue())

    def test_detect_json(self) -> None:
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["detect", str(EASY), "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["changes"], [0, 1, 0, 1, 0])

    def test_predict_dir_writes_solutions(self) -> None:
        import io
        from contextlib import redirect_stdout

        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = main(["predict-dir", str(CORPUS / "easy"), tmp])
            self.assertEqual(code, 0)
            written = sorted(Path(tmp).glob("solution-problem-*.json"))
            self.assertEqual(len(written), 3)
            for path in written:
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("changes", payload)
                self.assertTrue(all(bit in (0, 1) for bit in payload["changes"]))

    def test_eval_runs(self) -> None:
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["eval", str(CORPUS)])
        self.assertEqual(code, 0)
        self.assertIn("mean over documents", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
