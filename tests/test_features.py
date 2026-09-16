from style_change.features import FeatureExtractor, FUNCTION_WORDS, feature_names, style_axes
from style_change.tokenize import split_paragraphs


FORMAL = (
    "The argument proceeds, therefore, from a measured observation; however, "
    "the conclusion remains tentative. Moreover, the writer avoids addressing "
    "the reader directly and withholds contraction."
)
CASUAL = (
    "Okay I'm not doing the lecture voice. You're gonna see contractions, "
    "questions, and a lot of I. Pretty different, right? Yeah."
)


def test_feature_name_stable_and_unique() -> None:
    names = feature_names()
    assert len(names) == len(set(names))
    assert names[:3] == ("words_per_sentence", "std_words_per_sentence", "chars_per_word")
    assert all(f"fw_{word}" in names for word in ("the", "however", "you"))
    assert len(names) == len(FUNCTION_WORDS) + 38


def test_casual_text_has_higher_contraction_and_person() -> None:
    extractor = FeatureExtractor(min_words=1)
    table = extractor.extract_document(split_paragraphs(f"{FORMAL}\n\n{CASUAL}"))
    index = {name: i for i, name in enumerate(table.names)}
    assert table.matrix[1, index["contraction_ratio"]] > table.matrix[0, index["contraction_ratio"]]
    assert table.matrix[1, index["first_person"]] > table.matrix[0, index["first_person"]]
    assert table.matrix[1, index["second_person"]] > table.matrix[0, index["second_person"]]
    assert table.matrix[1, index["discourse_casual"]] > table.matrix[0, index["discourse_casual"]]


def test_zscore_zero_mean_unit_std() -> None:
    extractor = FeatureExtractor(min_words=1)
    table = extractor.extract_document(split_paragraphs(f"{FORMAL}\n\n{CASUAL}\n\n{FORMAL} again, with therefore."))
    scaled = table.zscored()
    assert abs(float(scaled.mean())) < 1e-8
    # columns with no variance stay at sd=1 after the guard, so they are 0
    variances = scaled.var(axis=0)
    assert (variances < 1e-8).any() or abs(float(variances.mean()) - 1.0) < 0.25


def test_top_differences_surface_register_cues() -> None:
    extractor = FeatureExtractor(min_words=1)
    table = extractor.extract_document(split_paragraphs(f"{FORMAL}\n\n{CASUAL}"))
    names = {row[0] for row in table.top_differences(0, 1, k=10)}
    assert names & {
        "contraction_ratio",
        "first_person",
        "second_person",
        "discourse_casual",
        "question_per_word",
        "fw_you",
        "fw_the",
    }


def test_style_axes_flip_formality_and_address() -> None:
    extractor = FeatureExtractor(min_words=1)
    table = extractor.extract_document(split_paragraphs(f"{FORMAL}\n\n{CASUAL}"))
    axes = style_axes(table)
    # formality, address, rhythm, procedure
    assert axes[0, 0] > axes[1, 0]
    assert axes[1, 1] > axes[0, 1]
