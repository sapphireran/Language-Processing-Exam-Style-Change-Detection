from splicefind.calibrate import best_threshold, sweep_thresholds
from splicefind.generate import make_split
from splicefind.io import Collection


def test_sweep_finds_a_usable_threshold():
    docs = make_split(n_easy=3, n_medium=2, n_hard=1, seed=3)
    collection = Collection(
        problems=[doc.problem for doc in docs],
        truths={doc.truth.problem_id: doc.truth for doc in docs},
    )
    points = sweep_thresholds(collection, thresholds=[0.30, 0.45, 0.60, 0.80])
    winner = best_threshold(points)
    assert winner.macro_f1 >= 0.0
    assert winner.threshold in {0.30, 0.45, 0.60, 0.80}
    assert any(point.macro_f1 > 0 for point in points)
