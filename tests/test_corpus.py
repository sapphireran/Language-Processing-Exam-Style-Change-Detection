from examples.corpus.bank import DOCUMENTS, HOLDOUT, holdout, in_band
from kerf.detect import detect_path
from kerf.io import paired_files, read_truth
from kerf.metrics import hinge_macro_f1, score_directory


def test_bank_matches_files() -> None:
    assert len(DOCUMENTS) == 28
    assert len(HOLDOUT) == 7
    assert len(in_band()) == 21
    assert len(holdout()) == 7
    pairs = paired_files("examples/corpus")
    assert len(pairs) == 28


def test_truth_agrees_with_bank() -> None:
    by_code = {d.code: d for d in DOCUMENTS}
    for problem, truth in paired_files("examples/corpus"):
        code = problem.name.removeprefix("problem-").split("-", 1)[0]
        doc = by_code[code]
        t = read_truth(truth)
        assert t.changes == list(doc.changes)
        assert len(t.changes) == len(doc.paragraphs) - 1


def test_kerf_zero_false_positives() -> None:
    bundle = score_directory("examples/corpus")
    assert bundle["overall"].fp == 0
    assert bundle["overall"].fn == 1
    assert bundle["overall"].macro_f1 > 0.95


def test_holdout_is_clean() -> None:
    bundle = score_directory("examples/corpus")
    codes = {d.code: d for d in DOCUMENTS}
    pred, gold = [], []
    for row in bundle["rows"]:
        code = row["id"].replace("problem-", "").split("-")[0]
        if codes[code].holdout:
            pred.extend(row["pred"])
            gold.extend(row["gold"])
    scores = hinge_macro_f1(pred, gold)
    assert scores.fp == 0
    assert scores.fn == 0


def test_controls_and_traps_stay_quiet() -> None:
    codes = {d.code: d for d in DOCUMENTS}
    for problem, truth in paired_files("examples/corpus"):
        code = problem.name.removeprefix("problem-").split("-", 1)[0]
        if codes[code].band not in {"control", "trap"}:
            continue
        det = detect_path(problem)
        assert det.changes == read_truth(truth).changes
        assert sum(det.changes) == 0


def test_live_miss_is_document_27_last_hinge() -> None:
    from pathlib import Path

    path = Path("examples/corpus/problem-27-stilling-four-houses.txt")
    det = detect_path(path)
    gold = read_truth(path.with_name("truth-problem-27.json")).changes
    assert gold == [1, 1, 1]
    assert det.changes == [1, 1, 0]


def test_never_fire_accuracy_is_the_liar() -> None:
    bundle = score_directory("examples/corpus")
    never, kerf = bundle["never"], bundle["overall"]
    assert never.accuracy > 0.6
    assert kerf.macro_f1 > never.macro_f1
    assert kerf.macro_f1 > bundle["always"].macro_f1
