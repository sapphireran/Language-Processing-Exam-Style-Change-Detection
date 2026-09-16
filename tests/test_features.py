from kerf.features import SAW_WEIGHTS, extract


def test_placard_has_second_person() -> None:
    vec = extract("You will open your page. You will see the number.")
    assert vec.rates["second_person"] > 0.1
    assert vec.rates["first_person"] == 0.0


def test_statute_has_shall() -> None:
    vec = extract("The attendant shall not walk. Any defect shall be entered.")
    assert vec.rates["fw:shall"] > 0.05


def test_saw_vector_length_matches_weights() -> None:
    vec = extract("The well was opened. The staff was recorded.")
    assert len(vec.saw_values()) == len(SAW_WEIGHTS)
    assert vec.saw_names() == [name for name, _ in SAW_WEIGHTS]


def test_nouns_do_not_have_their_own_rate() -> None:
    well = extract("The stilling well was opened at dawn. The float was recorded.")
    booth = extract("The cinema booth was opened at dusk. The lamp was recorded.")
    # Closed-class skeleton is the same on purpose.
    assert abs(well.rates["fw:was"] - booth.rates["fw:was"]) < 0.08
    assert "fw:stilling" not in well.rates
    assert "fw:cinema" not in booth.rates
