from stylechange.detectors import AdaptiveDetector, ThresholdDetector, smooth_changes
from stylechange.topic import content_vector, topic_distance


CASUAL = (
    "I swear weeknight pasta is stupidly forgiving. You boil water, throw in way too "
    "much salt, and pretend you measured the noodles. I ate it cold from the container "
    "and I am not sorry!"
)
FORMAL = (
    "Municipal street design is often treated as a purely engineering problem, yet the "
    "distribution of shade, seating, and crossing time has measurable effects on who "
    "can comfortably use a corridor. Implementation is constrained by maintenance budgets."
)


def test_threshold_detector_flags_obvious_style_shift():
    detection = ThresholdDetector(threshold=0.40).predict_paragraphs([CASUAL, CASUAL, FORMAL])
    assert detection.changes == [0, 1]
    assert detection.distances[1] > detection.distances[0]


def test_adaptive_detector_uses_document_relative_cut():
    detection = AdaptiveDetector(k=0.2, floor=0.2).predict_paragraphs([CASUAL, FORMAL, FORMAL])
    assert detection.changes[0] == 1
    assert detection.changes[1] == 0


def test_smooth_changes_majority():
    assert smooth_changes([1, 0, 1], [0.9, 0.2, 0.8], radius=1) == [1, 1, 1]


def test_topic_distance_tracks_content_not_function_words():
    pasta = "Leftover pasta with chili flakes and a reckless splash of pasta water."
    also_pasta = "The noodles and tomato sauce made a forgiving pasta dinner."
    streets = "Sidewalk width and curb allocation change who can linger on the corridor."
    assert topic_distance(pasta, also_pasta) < topic_distance(pasta, streets)
    assert "pasta" in content_vector(pasta)
    assert "the" not in content_vector(pasta)
