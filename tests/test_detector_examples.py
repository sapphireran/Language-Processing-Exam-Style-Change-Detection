from pathlib import Path

from stylechange.detector import detect
from stylechange.evaluate import evaluate_collection
from stylechange.generate import Block, mix_blocks
from stylechange.io import iter_problems, load_problem, load_truth

DOCS = Path(__file__).resolve().parents[1] / "examples" / "documents"


def test_every_bundled_document_matches_gold():
    score = evaluate_collection(DOCS)
    assert score.n_exact == len(score.documents)
    assert score.macro_f1 == 1.0
    assert score.n_pairs == 46


def test_gold_length_matches_units():
    for problem in iter_problems(DOCS):
        truth = load_truth(problem)
        assert truth is not None
        detection = detect(load_problem(problem))
        assert len(detection.changes) == len(detection.units) - 1
        assert len(truth["changes"]) == len(detection.units) - 1
        assert detection.changes == [int(x) for x in truth["changes"]]


def test_exam_takehome_has_three_author_blocks():
    detection = detect(load_problem(DOCS / "problem-exam-takehome.txt"))
    assert detection.changes == [0, 0, 1, 0, 0, 0, 1, 0, 0]
    assert detection.n_authors == 3
    assert detection.voices[:3] == ["student", "student", "student"]
    assert detection.voices[-3:] == ["notes", "notes", "notes"]


def test_single_author_has_no_cuts():
    detection = detect(load_problem(DOCS / "problem-single-author.txt"))
    assert detection.changes == [0, 0, 0, 0, 0]
    assert detection.n_authors == 1


def test_hard_cut_is_a_span_not_a_voice_jump():
    detection = detect(load_problem(DOCS / "problem-hard-we-vs-one.txt"))
    assert detection.changes == [0, 0, 1, 0, 0]
    assert all(voice == "textbook" for voice in detection.voices)
    assert detection.boundaries[0].reason == "span"


def test_paragraph_gift_uses_blank_lines():
    detection = detect(load_problem(DOCS / "problem-paragraph-gift.txt"))
    assert len(detection.units) == 3
    assert detection.changes == [1, 1]


def test_mix_blocks_round_trip():
    text, gold, _voices = mix_blocks(
        Block("student", ("I think this is the student block.", "For me it still reads like notes.")),
        Block(
            "textbook",
            (
                "A hidden Markov model specifies a joint distribution over labels.",
                "The forward algorithm therefore computes the marginal likelihood.",
            ),
        ),
        Block("notes", ("HMM: y -> x", "fwd: alpha recursion")),
    )
    detection = detect(text)
    assert detection.changes == gold
