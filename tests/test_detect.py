from examscd.detect import detect_document, pair_distance, threshold_distances


def test_quiet_pairs_stay_uncut_when_below_floor() -> None:
    distances = [0.05, 0.07, 0.04, 0.06]
    thr = threshold_distances(distances, abs_min=0.18)
    assert thr == 0.18
    assert all(d < thr for d in distances)


def test_gap_heuristic_finds_a_lonely_spike() -> None:
    distances = [0.08, 0.09, 0.55, 0.10]
    thr = threshold_distances(distances, abs_min=0.18, gap_min=0.07)
    pred = [1 if d >= thr else 0 for d in distances]
    assert pred == [0, 0, 1, 0]


def test_recipe_cut_is_detected() -> None:
    text = (
        "Preheat the oven to 180 C.\n"
        "Chop two yellow onions.\n"
        "Warm a thin film of oil in the pan.\n"
        "Stir until the edges brown.\n"
        "The Maillard reaction comprises a family of non-enzymatic browning pathways "
        "in which reducing sugars condense with free amino groups.\n"
        "Elevated surface temperature accelerates the formation of melanoidins.\n"
    )
    result = detect_document(text, granularity="sentence")
    assert result.changes.count(1) == 1
    assert result.changes[3] == 1


def test_pair_distance_is_higher_across_registers() -> None:
    sms = "hey r u coming to the library later"
    essay = (
        "A library is not merely a warehouse of copies; it is a negotiated public space "
        "in which attention itself is rationed."
    )
    near = "hey r u still at the library later"
    assert pair_distance(sms, essay)["combined"] > pair_distance(sms, near)["combined"]
