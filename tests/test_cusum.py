from examscd.cusum import ascii_cusum, cusum_points, cusum_series, mean


def test_memorised_series_from_docs() -> None:
    values = [4, 5, 4, 5, 18, 16, 17, 19]
    assert mean(values) == 11
    series = cusum_series(values)
    assert series[0] == 0.0
    assert series[4] == -26.0
    assert abs(series[-1]) < 1e-9
    assert cusum_points(values) == [3]


def test_flat_series_has_no_cusum_hit() -> None:
    values = [8, 8, 8, 8, 8, 8]
    assert cusum_points(values) == []
    assert all(abs(x) < 1e-9 for x in cusum_series(values))


def test_ascii_cusum_contains_axis() -> None:
    picture = ascii_cusum([4, 5, 18, 16])
    assert "CUSUM" in picture
    assert "*" in picture
