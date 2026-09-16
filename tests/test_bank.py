from examples.corpus.bank import DOCUMENTS, authors_for, changes_for, holdout_ids


def test_thirty_documents() -> None:
    assert len(DOCUMENTS) == 30
    assert [doc["ident"] for doc in DOCUMENTS] == list(range(1, 31))


def test_holdout_codes() -> None:
    assert holdout_ids() == [4, 10, 16, 22, 26, 30]


def test_changes_follow_houses() -> None:
    for doc in DOCUMENTS:
        houses = [block["house"] for block in doc["blocks"]]
        assert changes_for(doc) == [int(a != b) for a, b in zip(houses, houses[1:])]
        assert authors_for(doc) == len(set(houses))


def test_traps_do_not_change_house() -> None:
    traps = [doc for doc in DOCUMENTS if doc["difficulty"] == "trap"]
    assert len(traps) == 4
    for doc in traps:
        assert authors_for(doc) == 1
        assert sum(changes_for(doc)) == 0


def test_controls_are_single_house() -> None:
    for doc in DOCUMENTS:
        if doc["difficulty"] == "control":
            assert authors_for(doc) == 1
            assert sum(changes_for(doc)) == 0


def test_collage_has_three_seams() -> None:
    collage = next(doc for doc in DOCUMENTS if doc["ident"] == 30)
    assert changes_for(collage) == [1, 1, 1]


def test_aba_returns() -> None:
    aba = next(doc for doc in DOCUMENTS if doc["ident"] == 29)
    houses = [block["house"] for block in aba["blocks"]]
    assert houses[0] == houses[-1] == "skiff"
    assert "roll" in houses
    assert changes_for(aba) == [0, 1, 0, 1, 0]


def test_no_empty_blocks() -> None:
    for doc in DOCUMENTS:
        for block in doc["blocks"]:
            assert len(block["text"].split()) >= 12
            assert block["house"] in {"skiff", "roll", "twine", "vellum", "flint", "brine"}
