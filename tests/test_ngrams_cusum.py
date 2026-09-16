from splicefind.cusum import ascii_sparkline, boundary_scores, cusum
from splicefind.delta import burrows_delta, most_shifted_words
from splicefind.features import extract_paragraph
from splicefind.ngrams import cosine, profile


def test_identical_profiles_have_cosine_one():
    text = "the same phrase repeated for a profile"
    assert cosine(profile(text), profile(text)) > 0.999


def test_cusum_returns_to_zero():
    trace = cusum([1.0, 2.0, 3.0, 4.0])
    assert abs(trace.cusum[-1]) < 1e-9
    assert len(boundary_scores(trace)) == 3
    assert ascii_sparkline(trace.cusum)


def test_delta_zero_on_identical_vectors():
    row = [0.1, -0.2, 0.3]
    assert burrows_delta(row, row) == 0.0


def test_shifted_function_words_surface_i_vs_one():
    left = extract_paragraph("I think I will take my own cup with me.")
    right = extract_paragraph("One may take the cup if one prefers the alternative.")
    shifted = most_shifted_words(left, right, k=6)
    names = {row[0] for row in shifted}
    assert "i" in names or "one" in names or "the" in names
