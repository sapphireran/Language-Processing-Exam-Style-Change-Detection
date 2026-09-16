from kerf.distance import cosine, euclidean, hellinger, js_divergence


def test_identical_is_zero() -> None:
    v = [0.2, 0.3, 0.5]
    assert euclidean(v, v) == 0.0
    assert hellinger(v, v) == 0.0
    assert js_divergence(v, v) == 0.0
    assert abs(cosine(v, v) - 1.0) < 1e-12


def test_hellinger_bounds() -> None:
    p = [1.0, 0.0, 0.0]
    q = [0.0, 1.0, 0.0]
    assert 0.9 < hellinger(p, q) <= 1.0 + 1e-12
