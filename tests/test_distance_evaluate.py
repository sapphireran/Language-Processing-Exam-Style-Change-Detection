import unittest

from inkfold.detectors import EnsembleDetector, ThresholdDetector, never_fire
from inkfold.distance import blend, cosine, cosine_distance, score_cut
from inkfold.evaluate import accuracy_trap_demo, confusion
from inkfold.io import Problem, Truth


class DistanceTests(unittest.TestCase):
    def test_identical_cosine_is_one(self):
        self.assertAlmostEqual(cosine([1, 2, 3], [1, 2, 3]), 1.0)

    def test_orthogonal_cosine_is_zero(self):
        self.assertAlmostEqual(cosine([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(cosine_distance([1, 0], [0, 1]), 1.0)

    def test_register_flip_scores_higher_than_same_voice(self):
        stall = [
            "I'm keeping the damper cracked so Mira's bowls don't pink.",
            "I'll be home once the pyrometer drops.",
        ]
        notice = [
            "Persons entering the hall shall wear closed footwear.",
            "A written record must be completed if any cone collapses.",
        ]
        same_left = stall[:1]
        same_right = stall[1:]
        flip, _ = score_cut(stall, notice)
        same, _ = score_cut(same_left, same_right)
        self.assertGreater(flip, same)
        self.assertGreater(flip, 0.25)

    def test_blend_is_bounded(self):
        score = blend(
            {
                "register_l1": 2.0,
                "function_cosine_distance": 1.0,
                "char3_distance": 1.0,
                "delta": 2.0,
            }
        )
        self.assertGreater(score, 0.5)
        self.assertLessEqual(score, 1.0)


class EvaluateTests(unittest.TestCase):
    def test_confusion_and_accuracy_trap(self):
        gold = [0, 0, 0, 1]
        never = confusion(gold, [0, 0, 0, 0])
        self.assertAlmostEqual(never.accuracy, 0.75)
        self.assertLess(never.macro_f1, 0.5)
        perfect = confusion(gold, gold)
        self.assertEqual(perfect.macro_f1, 1.0)

    def test_never_fire_baseline_on_tiny_problem(self):
        problem = Problem(
            path=__import__("pathlib").Path("x"),
            problem_id="toy",
            units=["a.", "b.", "c.", "d."],
            truth=Truth(authors=2, changes=[0, 1, 0], site="easy"),
        )
        demo = accuracy_trap_demo([problem])
        self.assertAlmostEqual(demo["never_accuracy"], 2 / 3)
        self.assertEqual(demo["n_changes"], 1)

    def test_threshold_finds_a_loud_hinge(self):
        units = [
            "I'm telling you the dough's too wet and I can't roll it.",
            "Don't wait up, I'll freeze the extra filling.",
            "Vendors shall maintain a probe thermometer at the stall.",
            "A written incident record must be completed after any complaint.",
        ]
        det = ThresholdDetector(0.28).detect(units)
        self.assertEqual(len(det.changes), 3)
        self.assertEqual(det.changes[1], 1, det.scores)


if __name__ == "__main__":
    unittest.main()
