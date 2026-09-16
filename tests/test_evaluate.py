from isogloss.evaluate import always_fire, confusion, macro_f1, never_fire, score_changes


def test_perfect() -> None:
    gold = [0, 1, 0, 1]
    assert macro_f1(gold, gold) == 1.0


def test_never_fire_kills_change_f1() -> None:
    gold = [0, 0, 1, 0]
    pred = never_fire(4)
    table = confusion(gold, pred)
    assert table.f1(1) == 0.0
    assert table.accuracy == 0.75
    assert macro_f1(gold, pred) < table.accuracy


def test_always_fire_kills_same_f1() -> None:
    gold = [0, 0, 1, 0]
    table = confusion(gold, always_fire(4))
    assert table.f1(0) == 0.0


def test_score_keys() -> None:
    scored = score_changes([0, 1], [0, 1])
    assert scored["tp"] == 1
    assert scored["tn"] == 1
    assert scored["macro_f1"] == 1.0
