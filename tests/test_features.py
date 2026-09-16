from scdkit.features import extract_features


CASUAL = "I don't know, the rent here is mental lol. I'd rather wait."
FORMAL = (
    "However, one must first establish the original sewing structure; "
    "only thereafter may adhesive intervention be considered."
)


def test_contractions_are_closed_class_not_possessives() -> None:
    feat = extract_features("The vellum's response is nonlinear.")
    assert feat.contraction_rate == 0.0


def test_contractions_count_dont() -> None:
    feat = extract_features(CASUAL)
    assert feat.contraction_rate > 0.05
    assert feat.pronoun_i > 0


def test_impersonal_one_ignores_one_metre() -> None:
    feat = extract_features("I moved them one metre back from the radiator.")
    assert feat.pronoun_one == 0.0
    assert feat.pronoun_i > 0


def test_impersonal_one_matches_one_must() -> None:
    feat = extract_features(FORMAL)
    assert feat.pronoun_one > 0
    assert feat.formal_rate > 0
    assert feat.formality > extract_features(CASUAL).formality


def test_numeric_vector_is_finite() -> None:
    feat = extract_features(FORMAL)
    vec = feat.numeric_vector()
    assert vec
    assert all(x == x for x in vec)
