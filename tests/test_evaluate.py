from examscd.evaluate import adjusted_rand_index, boundary_report, macro_f1


def test_worked_macro_f1_from_docs() -> None:
    gold = [0, 0, 1, 0, 0]
    pred = [0, 1, 1, 0, 0]
    report = boundary_report(gold, pred)
    assert abs(report.f1_1 - (2 / 3)) < 1e-9
    assert abs(report.f1_0 - (6 / 7)) < 1e-9
    assert abs(report.macro_f1 - (19 / 21)) < 1e-9


def test_empty_class_convention_is_perfect_on_silence() -> None:
    assert macro_f1([0, 0, 0, 0], [0, 0, 0, 0]) == 1.0


def test_always_one_is_punished_on_a_quiet_document() -> None:
    gold = [0, 0, 0, 0]
    pred = [1, 1, 1, 1]
    assert macro_f1(gold, pred) < 0.6


def test_ari_is_permutation_invariant() -> None:
    gold = [1, 1, 2, 2, 1, 1]
    perm = [7, 7, 3, 3, 7, 7]
    other = [1, 1, 2, 2, 3, 3]
    assert abs(adjusted_rand_index(gold, perm) - 1.0) < 1e-9
    assert adjusted_rand_index(gold, other) < 1.0


def test_ari_perfect_on_identical_single_author() -> None:
    assert adjusted_rand_index([1, 1, 1, 1], [4, 4, 4, 4]) == 1.0
