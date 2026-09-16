from quoin.ncd import compressed_len, cross_gain, ncd, ncd_matrix


def test_identical_strings_are_cheap():
    text = "the same compositor locked the same forme twice and washed the same rollers."
    assert ncd(text, text) < 0.25


def test_unrelated_strings_are_dearer_than_related_ones():
    press = (
        "I locked the forme before dawn and felt the give in the tympan. "
        "One must not hurry a rule; I have found that a hurried rule shows."
    )
    press2 = (
        "I locked the chase after dusk and felt the give in the tympan. "
        "One must not hurry a quoin; I have found that a hurried quoin walks."
    )
    notice = (
        "Members of the public are advised that overnight operation is prohibited. "
        "Complaints shall be lodged with the clerk. Permits shall be produced."
    )
    assert ncd(press, press2) < ncd(press, notice)


def test_ncd_is_symmetric_and_bounded():
    left, right = "alpha beta gamma", "the ordinance shall apply"
    assert abs(ncd(left, right) - ncd(right, left)) < 1e-9
    assert 0.0 <= ncd(left, right) <= 1.5


def test_gain_is_higher_for_repeated_text():
    text = "function words are frequent and half conscious in a stable ratio"
    other = "pursuant to ordinance the insured shall produce the permit"
    assert cross_gain(text, text) > cross_gain(text, other)


def test_compressed_len_is_positive():
    assert compressed_len("x") >= 1
    assert compressed_len("") >= 1


def test_ncd_matrix_is_square_and_symmetric():
    texts = ["aaa bbb", "aaa bbb ccc", "ordinance shall"]
    matrix = ncd_matrix(texts)
    assert len(matrix) == 3
    assert matrix[0][1] == matrix[1][0]
