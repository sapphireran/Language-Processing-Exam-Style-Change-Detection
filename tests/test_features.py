from seamtrace.features import FeatureTable, extract_unit_features


def test_first_person_moves() -> None:
    diary = extract_unit_features("I walked home and I burnt the oats again.")
    memo = extract_unit_features("It was agreed that the budget would remain ring-fenced.")
    assert diary.scalars["first_person_rate"] > memo.scalars["first_person_rate"]
    assert memo.scalars["first_person_rate"] == 0.0


def test_starts_lower() -> None:
    chat = extract_unit_features("ok so the track is packed by eight")
    prose = extract_unit_features("In contrast, the repair begins with a survey.")
    assert chat.scalars["starts_lower"] == 1.0
    assert prose.scalars["starts_lower"] == 0.0


def test_table_length() -> None:
    table = FeatureTable.from_units(["One.", "Two three."])
    assert len(table) == 2
    assert table.units[0].scalars["n_words"] == 1
