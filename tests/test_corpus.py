from __future__ import annotations

import json
import unittest
from pathlib import Path

from hingemark.corpus import list_corpus
from hingemark.evaluate import score_pairs
from hingemark.io import read_problem, read_truth, truth_path_for, write_solution

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "examples" / "corpus"


class CorpusIntegrityTests(unittest.TestCase):
    def test_manifest_matches_files(self) -> None:
        items = list_corpus(CORPUS)
        self.assertEqual(len(items), 26)
        splits = {item.split for item in items}
        self.assertGreaterEqual(len(splits), 6)

    def test_changes_match_hinges_and_authors(self) -> None:
        for item in list_corpus(CORPUS):
            self.assertEqual(len(item.truth.changes), item.problem.n_hinges, item.name)
            self.assertTrue(all(c in (0, 1) for c in item.truth.changes), item.name)
            if item.truth.authors is not None:
                derived = tuple(
                    0 if a == b else 1
                    for a, b in zip(item.truth.authors, item.truth.authors[1:])
                )
                self.assertEqual(derived, item.truth.changes, item.name)

    def test_return_file_breaks_the_sum_rule(self) -> None:
        item = next(it for it in list_corpus(CORPUS) if it.split == "return")
        self.assertTrue(item.truth.returning_author)
        self.assertNotEqual(len(set(item.truth.authors or ())), item.truth.n_authors_from_changes)

    def test_control_has_no_gold_changes(self) -> None:
        controls = [it for it in list_corpus(CORPUS) if it.split == "control"]
        self.assertGreaterEqual(len(controls), 3)
        for item in controls:
            self.assertEqual(sum(item.truth.changes), 0, item.name)
            self.assertEqual(len(set(item.truth.authors or ())), 1)

    def test_one_sentence_per_line(self) -> None:
        for path in sorted(CORPUS.glob("problem-*.txt")):
            lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
            problem = read_problem(path)
            self.assertEqual(len(lines), len(problem.units), path.name)

    def test_solution_roundtrip(self) -> None:
        dest = Path("/tmp/hingemark-solution.json")
        write_solution(dest, [0, 1, 0])
        raw = json.loads(dest.read_text(encoding="utf-8"))
        self.assertEqual(raw, {"changes": [0, 1, 0]})

    def test_truth_path_helper(self) -> None:
        problem = CORPUS / "problem-13-two-mycologists.txt"
        path = truth_path_for(problem, CORPUS / "truth")
        truth = read_truth(path)
        self.assertEqual(truth.meta["split"], "hard")


class EasyDetectTests(unittest.TestCase):
    def test_easy_register_pairs_are_loud(self) -> None:
        from hingemark.detectors import DEFAULT_THRESHOLD, threshold_detect
        from hingemark.pairwise import score_unit_hinges

        easy = [it for it in list_corpus(CORPUS) if it.split == "easy"]
        hits = 0
        for item in easy:
            pred = threshold_detect(
                score_unit_hinges(item.problem.units),
                threshold=DEFAULT_THRESHOLD,
            ).changes
            report = score_pairs(item.truth.changes, pred)
            if report.change.recall >= 0.99:
                hits += 1
        self.assertGreaterEqual(hits, 4, "easy split should mostly light up")


if __name__ == "__main__":
    unittest.main()
