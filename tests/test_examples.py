from pathlib import Path

from examscd.detect import detect_document
from examscd.evaluate import boundary_report
from examscd.io import read_text, read_truth
from examscd.tokenize import split_units

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "examples" / "documents"
TRUTH = DOCS / "truth"

CASES = [
    "01_single_commute",
    "02_recipe_then_maillard",
    "03_forum_three_voices",
    "04_minutes_return",
    "05_same_topic_hard",
    "06_gift_abstract",
    "07_collage_paragraphs",
    "08_sms_essay_mix",
    "09_lab_notebook",
    "10_exam_mashup",
]


def _load(stem: str) -> tuple[str, object]:
    text = read_text(DOCS / f"{stem}.txt")
    truth = read_truth(TRUTH / f"{stem}.json")
    return text, truth


def test_gold_pair_counts_match_the_tokenizer() -> None:
    for stem in CASES:
        text, truth = _load(stem)
        units = split_units(text, truth.granularity)
        assert len(truth.changes) == len(units) - 1, stem
        if truth.authors:
            assert len(truth.authors) == len(units), stem


def test_negative_controls_stay_single_author() -> None:
    for stem in ("01_single_commute", "09_lab_notebook"):
        text, truth = _load(stem)
        result = detect_document(text, granularity=truth.granularity)
        assert result.changes == truth.changes, stem
        assert result.multi_author is False


def test_easy_cuts_are_recovered() -> None:
    for stem in ("02_recipe_then_maillard", "06_gift_abstract", "08_sms_essay_mix"):
        text, truth = _load(stem)
        result = detect_document(text, granularity=truth.granularity)
        report = boundary_report(truth.changes, result.changes)
        assert result.changes == truth.changes, (stem, result.changes)
        assert report.macro_f1 == 1.0


def test_forum_and_minutes_recover_both_cuts() -> None:
    for stem in ("03_forum_three_voices", "04_minutes_return"):
        text, truth = _load(stem)
        result = detect_document(text, granularity=truth.granularity)
        assert result.changes == truth.changes, (stem, result.changes)


def test_hard_bpe_file_finds_the_only_cut() -> None:
    text, truth = _load("05_same_topic_hard")
    result = detect_document(text, granularity=truth.granularity)
    assert result.changes == truth.changes, result.changes


def test_mashup_and_collage_keep_high_pair_f1() -> None:
    for stem in ("07_collage_paragraphs", "10_exam_mashup"):
        text, truth = _load(stem)
        result = detect_document(text, granularity=truth.granularity)
        report = boundary_report(truth.changes, result.changes)
        assert report.macro_f1 >= 0.85, (stem, result.changes, report.macro_f1)
