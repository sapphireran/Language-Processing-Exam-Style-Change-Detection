import unittest

from inkfold.corpus import iter_problems, validate_corpus
from inkfold.detectors import EnsembleDetector
from inkfold.evaluate import score_folder


class CorpusContractTests(unittest.TestCase):
    def test_contract_and_count(self):
        errors = validate_corpus()
        self.assertEqual(errors, [])
        problems = iter_problems()
        self.assertEqual(len(problems), 26)

    def test_return_author_breaks_naive_count(self):
        kiln = next(p for p in iter_problems() if p.problem_id == "problem-22-kiln-return")
        self.assertTrue(kiln.truth.return_author)
        naive = 1 + sum(kiln.truth.changes)
        self.assertNotEqual(kiln.truth.authors, naive)
        self.assertEqual(kiln.truth.authors, 2)
        self.assertEqual(sum(kiln.truth.changes), 2)


class CorpusBehaviourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = score_folder(iter_problems(), EnsembleDetector())
        cls.by_id = {row.problem_id: row for row in cls.folder.rows}

    def test_easy_and_medium_are_exact(self):
        for row in self.folder.rows:
            if row.site in {"easy", "medium"}:
                self.assertTrue(row.exact_boundaries, row.problem_id)

    def test_hard_is_an_honest_miss(self):
        for row in self.folder.rows:
            if row.site == "hard":
                self.assertEqual(row.expected_error, "same_register_miss")
                self.assertFalse(row.exact_boundaries, row.problem_id)
                self.assertEqual(sum(row.pred_changes), 0, row.problem_id)

    def test_topic_controls_stay_quiet(self):
        for pid in (
            "problem-19-stall-three-topics",
            "problem-20-notice-three-topics",
        ):
            self.assertTrue(self.by_id[pid].exact_boundaries, pid)

    def test_chat_control_is_allowed_to_jitter(self):
        row = self.by_id["problem-21-chat-three-topics"]
        self.assertEqual(row.expected_error, "chat_jitter")
        self.assertGreater(sum(row.pred_changes), 0)

    def test_gift_paste_return_folds(self):
        gift = self.by_id["problem-24-gift-abstract"]
        paste = self.by_id["problem-25-exam-two-answers"]
        ret = self.by_id["problem-22-kiln-return"]
        self.assertTrue(gift.exact_boundaries)
        self.assertTrue(paste.exact_boundaries)
        self.assertTrue(ret.exact_boundaries)
        self.assertFalse(ret.author_ok)

    def test_never_fire_wins_accuracy_loses_f1(self):
        never = self.folder.never_baseline()
        real = self.folder.overall
        self.assertGreater(never.accuracy, 0.7)
        self.assertGreater(real.macro_f1, never.macro_f1)
        self.assertGreater(self.folder.mean_macro_f1(), 0.7)


if __name__ == "__main__":
    unittest.main()
