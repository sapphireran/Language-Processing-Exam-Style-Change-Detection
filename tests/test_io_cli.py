import json
import tempfile
import unittest
from pathlib import Path

from inkfold.cli import main
from inkfold.io import Truth, read_problem, write_problem, write_truth


class IoTests(unittest.TestCase):
    def test_roundtrip_and_return_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            units = ["one.", "two.", "three.", "four."]
            write_problem(root / "problem-99-return.txt", units)
            truth = Truth(
                authors=2,
                changes=[0, 1, 1],
                site="return",
                title="return demo",
                voices=["stall", "notice", "stall"],
                return_author=True,
                notes="A then B then A.",
            )
            (root / "truth").mkdir(exist_ok=True)
            write_truth(root / "truth" / "truth-problem-99-return.json", truth)
            problem = read_problem(root / "problem-99-return.txt")
            self.assertEqual(problem.units, units)
            self.assertEqual(problem.truth.authors, 2)
            self.assertEqual(problem.truth.validate(4), [])

    def test_missing_return_flag_is_an_error(self):
        truth = Truth(authors=2, changes=[1, 1], return_author=False)
        errs = truth.validate(3)
        self.assertTrue(any("return_author" in e or "!=" in e for e in errs))

    def test_cli_hand_and_detect(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "problem.txt"
            path.write_text(
                "I'm heading home once the pyrometer drops.\n"
                "Vendors shall wear closed footwear in the hall.\n",
                encoding="utf-8",
            )
            self.assertEqual(main(["hand", str(path)]), 0)
            self.assertEqual(main(["detect", str(path)]), 0)
            self.assertEqual(main(["cusum", str(path)]), 0)


if __name__ == "__main__":
    unittest.main()
