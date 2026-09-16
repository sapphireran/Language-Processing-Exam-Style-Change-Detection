from stylechange.features import extract_features, merge_span
from stylechange.register import register_axes


def test_capital_i_is_first_person_lowercase_is_not():
    student = extract_features("I think the tagset is too big.")
    formula = extract_features("CKY fills spans [i,j] for each i.")
    named_s = student.as_named_dense()
    named_f = formula.as_named_dense()
    assert named_s["first_person_ratio"] > 0
    assert named_f["first_person_ratio"] == 0


def test_student_register_is_more_personal_than_textbook():
    student = extract_features(
        "I'm never sure about this, and I always forget the exam number."
    )
    textbook = extract_features(
        "Therefore the chain rule is approximated by a Markov assumption."
    )
    assert register_axes(student)["personal"] > register_axes(textbook)["personal"]
    assert register_axes(textbook)["academic"] > register_axes(student)["academic"]


def test_notes_register_is_telegram():
    notes = extract_features("n-gram: P(w_i | w_{i-n+1}..w_{i-1}).")
    prose = extract_features(
        "An n-gram language model estimates the probability of the next token."
    )
    assert register_axes(notes)["telegram"] > register_axes(prose)["telegram"]


def test_merge_is_word_weighted_and_pools_counts():
    short = extract_features("I agree.")
    long = extract_features(
        "Nevertheless the subsequent derivation remains entirely impersonal and Latinate."
    )
    merged = merge_span([short, long], 0, 2)
    assert merged.n_words == short.n_words + long.n_words
    assert merged.n_chars == short.n_chars + long.n_chars
    assert sum(merged.function_counts) == sum(short.function_counts) + sum(
        long.function_counts
    )
