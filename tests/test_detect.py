from splicefind.detect import detect_text
from splicefind.evaluate import score_document
from splicefind.generate import stitch


def test_detects_obvious_register_cut():
    casual = (
        "I can't believe the kettle's broken again. I'm just going to boil water in a pan "
        "and hope the morning sorts itself out."
    )
    formal = (
        "The heating element appears to have failed after repeated limescale accumulation. "
        "Replacement, rather than further descaling, is the more economical course."
    )
    text = casual + "\n\n" + casual + "\n\n" + formal + "\n\n" + formal
    detection = detect_text(text, threshold=0.50)
    assert detection.changes[1] == 1
    assert detection.n_authors_lower_bound >= 2


def test_synthetic_easy_splice_has_a_true_cut():
    doc = stitch(
        ("casual_first", "casual_first", "formal_impersonal", "formal_impersonal"),
        problem_id="syn",
        difficulty="easy",
        title="easy",
        seed=1,
    )
    detection = detect_text(doc.problem.text, threshold=0.45)
    score = score_document(doc.truth.changes, detection.changes, "syn")
    assert doc.truth.changes == [0, 1, 0]
    # The easy register cut should be recoverable; allow one cheap miss.
    assert score.true_positives >= 1
