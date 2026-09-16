from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from stylechange.cli import main
from stylechange.evaluate import evaluate_dirs
from stylechange.io import load_problem_dir, problem_id
from stylechange.sentences import split_sentences


ROOT = Path(__file__).resolve().parents[1]
SYNTH = ROOT / "data" / "synthetic"


class CorpusTests(unittest.TestCase):
    def test_inventory(self) -> None:
        problems = load_problem_dir(SYNTH, require_truth=True)
        self.assertEqual(len(problems), 24)
        by_diff = {}
        for item in problems:
            by_diff.setdefault(item.path.parent.name, 0)
            by_diff[item.path.parent.name] += 1
        self.assertEqual(by_diff, {"easy": 8, "medium": 8, "hard": 8})

    def test_truth_matches_author_ids_and_splitter(self) -> None:
        for item in load_problem_dir(SYNTH, require_truth=True):
            ids = item.meta["author_ids"]
            derived = [int(left != right) for left, right in zip(ids, ids[1:])]
            self.assertEqual(derived, item.changes, item.path)
            self.assertEqual(len(item.sentences), len(ids))
            again = split_sentences(item.path.read_text(encoding="utf-8"))
            self.assertEqual(again, item.sentences)

    def test_manifest_keys_exist(self) -> None:
        manifest = json.loads((SYNTH / "manifest.json").read_text(encoding="utf-8"))
        for key in manifest["problems"]:
            self.assertTrue((SYNTH / key).is_file(), key)


class CliTests(unittest.TestCase):
    def test_features_and_evaluate_roundtrip(self) -> None:
        self.assertEqual(main(["features", "--text", "I don't mind 15 grams."]), 0)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "hard-unsupervised"
            self.assertEqual(
                main(
                    [
                        "detect",
                        "--input",
                        str(SYNTH / "hard"),
                        "--out",
                        str(out),
                        "--detector",
                        "always0",
                    ]
                ),
                0,
            )
            solutions = list(out.glob("solution-problem-*.json"))
            self.assertEqual(len(solutions), 8)
            result = evaluate_dirs(str(SYNTH / "hard"), str(out))
            self.assertEqual(result.io_failures, [])
            self.assertGreater(result.pooled["n_pairs"], 0)

    def test_problem_id_parser(self) -> None:
        self.assertEqual(problem_id("truth-problem-008.json"), "008")
        self.assertEqual(problem_id("/tmp/problem-12.txt"), "12")


if __name__ == "__main__":
    unittest.main()
