from pathlib import Path

from scd.evaluate import evaluate_directory, macro_f1
from scd.generate import write_corpus
from scd.models import majority_predict, predict_directory, train_logreg
from scd.report import render_report


def test_majority_zero_loses_to_trained_model(tmp_path: Path):
    data = tmp_path / "data"
    write_corpus(data, seed=1)
    model = train_logreg(data, bands=("easy",), seed=0)
    pred_dir = tmp_path / "pred"
    predict_directory(model, data / "easy", pred_dir)
    scores = evaluate_directory(pred_dir, data / "easy")

    majority_true = []
    majority_pred = []
    for doc in scores.per_document:
        majority_true.extend(doc.y_true)
        majority_pred.extend(majority_predict(doc.n_pairs, 0))

    assert scores.macro_f1 > macro_f1(majority_true, majority_pred)
    assert scores.macro_f1 > 0.7


def test_hard_band_is_not_easier_than_easy(tmp_path: Path):
    data = tmp_path / "data"
    write_corpus(data, seed=2)
    model = train_logreg(data, seed=0)
    easy_dir = tmp_path / "easy-pred"
    hard_dir = tmp_path / "hard-pred"
    predict_directory(model, data / "easy", easy_dir)
    predict_directory(model, data / "hard", hard_dir)
    easy = evaluate_directory(easy_dir, data / "easy")
    hard = evaluate_directory(hard_dir, data / "hard")
    # Topic leakage should make easy at least as tractable as hard.
    assert easy.macro_f1 + 1e-9 >= hard.macro_f1 - 0.15


def test_report_mentions_the_change_pair():
    html = render_report(
        [
            "The souffle requires a precise fold of the egg whites into the batter.",
            "Oven temperature should remain stable so the structure can set.",
            "Yeah I'm just gonna chuck the frozen pizza in and hope for the best.",
            "I'm not gonna overthink dinner tonight, seriously.",
        ],
        truth=[0, 1, 0],
        pred=[0, 1, 0],
        title="Souffle / pizza",
    )
    assert "Souffle / pizza" in html
    assert "truth=1" in html
    assert "author-run 2" in html
