import math

from style_change.detectors import DetectionResult
from style_change.evaluate import adjusted_rand_index, bcubed, evaluate_document


def test_ari_perfect_and_permuted_labels() -> None:
    gold = [0, 0, 1, 1, 0]
    assert adjusted_rand_index(gold, gold) == 1.0
    assert adjusted_rand_index([5, 5, 9, 9, 5], gold) == 1.0


def test_ari_chance_and_inverted() -> None:
    # two balanced labels vs a single cluster is not perfect
    assert adjusted_rand_index([0, 0, 0, 0], [0, 0, 1, 1]) < 1.0
    # a totally split labelling vs two pairs
    score = adjusted_rand_index([0, 1, 2, 3], [0, 0, 1, 1])
    assert score < 0.5


def test_bcubed_perfect() -> None:
    p, r, f1 = bcubed([1, 1, 2, 2], [0, 0, 9, 9])
    assert math.isclose(p, 1.0)
    assert math.isclose(r, 1.0)
    assert math.isclose(f1, 1.0)


def test_vacuous_all_negative_is_perfect() -> None:
    result = DetectionResult(
        multi_author=False,
        changes=[False, False],
        authors=[0, 0, 0],
        distances=[0.1, 0.1],
        threshold=0.75,
        paragraph_indices=[0, 1, 2],
    )
    report = evaluate_document(result, gold_authors=[0, 0, 0])
    assert report.task1.f1 == 1.0
    assert report.task2.f1 == 1.0


def test_evaluate_document_task_alignment() -> None:
    result = DetectionResult(
        multi_author=True,
        changes=[False, True, False],
        authors=[0, 0, 1, 1],
        distances=[0.1, 0.8, 0.1],
        threshold=0.42,
        paragraph_indices=[0, 1, 2, 3],
    )
    report = evaluate_document(result, gold_authors=[7, 7, 3, 3])
    assert report.task1.f1 == 1.0
    assert report.task2.f1 == 1.0
    assert report.ari == 1.0
    assert report.bcubed_f1 == 1.0
