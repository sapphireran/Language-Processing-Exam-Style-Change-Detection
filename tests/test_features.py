from splicefind.features import extract_paragraph, extract_document, pairwise_feature_distance
from splicefind.function_words import FUNCTION_WORDS


CASUAL = "I don't want to wait. It's late and I'm tired!"
FORMAL = (
    "One may observe that the scheduled interval is insufficient. "
    "A later departure would therefore be advisable."
)


def test_contractions_and_first_person_higher_in_casual():
    casual = extract_paragraph(CASUAL)
    formal = extract_paragraph(FORMAL)
    assert casual.scalars["contraction_rate"] > formal.scalars["contraction_rate"]
    assert casual.scalars["first_person_rate"] > formal.scalars["first_person_rate"]
    assert formal.scalars["impersonal_rate"] > casual.scalars["impersonal_rate"]


def test_function_word_vector_covers_closed_class():
    vector = extract_paragraph(FORMAL)
    assert set(vector.function_words) == set(FUNCTION_WORDS)
    assert abs(sum(vector.function_words.values()) - 0) > 0
    assert vector.function_words["the"] >= 0


def test_document_pairwise_distance_nonempty():
    doc = extract_document(CASUAL + "\n\n" + FORMAL)
    distances = pairwise_feature_distance(doc.vectors)
    assert len(distances) == 1
    assert distances[0] > 0
