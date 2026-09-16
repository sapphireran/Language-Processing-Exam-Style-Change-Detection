from scdkit.cusum import cusum, svg_polyline, word_length_cusum
from scdkit.delta import burrows_delta, zscore_rows
from scdkit.features import extract_many
from scdkit.ngrams import char_ngrams, cosine_distance, l2_normalize


def test_zscore_zero_mean() -> None:
    rows = zscore_rows([[1.0, 2.0], [3.0, 2.0], [5.0, 2.0]])
    col0 = [row[0] for row in rows]
    assert abs(sum(col0)) < 1e-9
    assert all(row[1] == 0.0 for row in rows)


def test_delta_identical_is_zero() -> None:
    assert burrows_delta([0.0, 1.0, -1.0], [0.0, 1.0, -1.0]) == 0.0
    assert burrows_delta([0.0, 1.0], [1.0, 0.0]) == 1.0


def test_identical_ngrams_have_zero_distance() -> None:
    profile = l2_normalize(char_ngrams("the same string"))
    assert cosine_distance(profile, profile) == 0.0


def test_cusum_ends_near_zero() -> None:
    series = cusum([1.0, 2.0, 3.0, 4.0])
    assert abs(series.cusum[-1]) < 1e-9
    assert series.mean == 2.5


def test_svg_contains_polyline() -> None:
    feats = extract_many(
        [
            "I write short notes. They stay short.",
            "However, one must subsequently consider a much longer academic sentence.",
        ]
    )
    markup = svg_polyline(word_length_cusum(feats))
    assert "<polyline" in markup
    assert "mean_word_len" in markup
