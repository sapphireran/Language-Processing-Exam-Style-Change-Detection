from examscd.cues import adjacent_same, assign_label, cue_scores, return_same, score_unit


def test_recipe_line_is_imperative() -> None:
    assert score_unit("Preheat the oven to 180 C.").label == "imperative"


def test_chat_line_is_slang() -> None:
    assert score_unit("omg my laptop just died mid raid and i lost the drop lol").label == "slang"


def test_we_versus_one_are_not_adjacent_aliases() -> None:
    assert not adjacent_same("academic_we", "academic_one")
    assert not return_same("academic_we", "academic_one")
    assert adjacent_same("academic", "academic_one")
    assert adjacent_same("slang", "personal")


def test_length_alone_is_not_academic() -> None:
    scores = cue_scores("The rest of the ride is quieter, just the click of the chain and whoever is overtaking on the left without a bell.")
    assert scores["academic"] < 0.40
    assert assign_label(scores) == "personal"


def test_version_is_not_a_nominalisation() -> None:
    scores = cue_scores("After that you can have the pedantic version.")
    assert scores["academic"] < scores["personal"]
