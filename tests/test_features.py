from stylechange.features import extract, register_flags


def test_capital_i_is_first_person():
    vector = extract("I think the emission is local.")
    assert vector.first_person_sg > 0
    assert vector.student_phrase >= 1


def test_formula_i_is_not_first_person():
    vector = extract("The model defines P(w_i) for each dummy index i in the sequence.")
    assert vector.first_person_sg == 0


def test_we_and_one_flags_differ():
    we = extract("We therefore train the bilinear scorer on the gold tree.")
    one = extract("One may treat the scorer as a function of the configuration.")
    assert register_flags(we)["we"] == 1.0
    assert register_flags(we)["one"] == 0.0
    assert register_flags(one)["one"] == 1.0
    assert register_flags(one)["we"] == 0.0


def test_notes_flags_on_production():
    vector = extract("CFG: S -> NP VP")
    flags = register_flags(vector)
    assert flags["notes"] == 1.0
    assert vector.arrow_rate > 0
    assert vector.colon_rate > 0


def test_contraction_and_informal():
    vector = extract("Don't worry, yeah it always looks messy.")
    assert vector.contraction_rate > 0
    assert vector.informal_rate > 0
