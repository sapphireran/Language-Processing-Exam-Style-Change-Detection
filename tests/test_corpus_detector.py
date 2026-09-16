from quoin.corpus import load_corpus
from quoin.detectors import QuoinDetector, always_fire, never_fire
from quoin.evaluate import safe_f1
from quoin.io import validate_pair


def test_corpus_loads_and_matches_truth_lengths():
    corpus = load_corpus()
    assert len(corpus) == 28
    bands = {item.band for item in corpus}
    assert {"easy", "medium", "hard", "trap", "control", "return", "collage"} <= bands
    for item in corpus:
        validate_pair(item.problem, item.truth)
        assert item.truth.authors is not None
        assert len(item.truth.authors) == item.problem.n_paragraphs


def test_easy_press_notice_hinge_is_found():
    item = load_corpus().get("problem-01-press-then-notice")
    pred = QuoinDetector().predict(item.problem.paragraphs)
    assert pred[1] == 1
    assert safe_f1(item.truth.changes, pred) >= 0.5


def test_control_solo_press_stays_quiet():
    item = load_corpus().get("problem-27-solo-press")
    pred = QuoinDetector().predict(item.problem.paragraphs)
    assert pred == [0, 0, 0]
    assert safe_f1(item.truth.changes, pred) == 1.0


def test_trap_notice_three_topics_does_not_go_wild():
    item = load_corpus().get("problem-20-notice-three-topics")
    pred = QuoinDetector().predict(item.problem.paragraphs)
    assert sum(pred) <= 1


def test_never_fire_is_perfect_on_controls_and_weak_on_easy():
    corpus = load_corpus()
    control = corpus.get("problem-28-solo-bees")
    easy = corpus.get("problem-02-bees-then-claim")
    assert safe_f1(control.truth.changes, never_fire(control.problem.n_boundaries)) == 1.0
    assert safe_f1(easy.truth.changes, never_fire(easy.problem.n_boundaries)) == 0.0
    assert safe_f1(easy.truth.changes, always_fire(easy.problem.n_boundaries)) < 1.0


def test_quoin_beats_never_fire_on_easy_band():
    corpus = load_corpus()
    detector = QuoinDetector()
    quoin_scores = []
    never_scores = []
    for item in corpus.by_band("easy"):
        pred = detector.predict(item.problem.paragraphs)
        quoin_scores.append(safe_f1(item.truth.changes, pred))
        never_scores.append(safe_f1(item.truth.changes, never_fire(item.problem.n_boundaries)))
    assert sum(quoin_scores) / len(quoin_scores) > sum(never_scores) / len(never_scores)
