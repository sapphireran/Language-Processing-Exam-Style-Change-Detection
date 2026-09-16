from stylechange.features import extract
from stylechange.voices import classify_voice, cut_band, merge_singleton_runs, smooth_voices


def test_recipe_is_chat():
    assert classify_voice(extract("Preheat the oven and just chuck the butter in a pan.")) == "chat"


def test_student_hedge():
    assert classify_voice(extract("I think the bit I always forget is the local emission.")) == "student"


def test_textbook_academic():
    label = classify_voice(
        extract(
            "Conditional random fields specify a globally normalised "
            "distribution over label sequences, thereby avoiding label bias."
        )
    )
    assert label == "textbook"


def test_short_colon_line_is_notes():
    assert classify_voice(extract("CRF: P(y|x) ∝ exp Σ w · f")) == "notes"
    assert classify_voice(extract("CFG: S -> NP VP")) == "notes"


def test_chat_and_student_share_a_cut_band():
    assert cut_band("chat") == cut_band("student") == "personal"
    assert cut_band("textbook") == "textbook"


def test_singleton_blip_is_absorbed():
    assert merge_singleton_runs(["student", "textbook", "student", "textbook", "textbook"]) == [
        "student",
        "student",
        "student",
        "textbook",
        "textbook",
    ]


def test_smooth_fills_mixed_from_neighbours():
    assert smooth_voices(["mixed", "student", "student"]) == ["student", "student", "student"]
