from scdkit.generate import load_author_bank, mix_document, write_mix
from scdkit.tokenize import split_paragraphs


def test_mix_aba_labels(author_dir) -> None:
    cards = load_author_bank(author_dir)
    text, truth = mix_document(cards, "ABA")
    assert truth.changes == (1, 1)
    assert truth.paragraph_authors == (1, 2, 1)
    assert len(split_paragraphs(text)) == 3


def test_write_mix(tmp_path, author_dir) -> None:
    cards = load_author_bank(author_dir)
    doc, gold = write_mix(cards, "AAB", tmp_path, "toy", seed=1)
    assert doc.is_file() and gold.is_file()
    assert gold.name.startswith("truth-")


def test_mix_uses_named_cards_in_letter_order(author_dir) -> None:
    cards = [
        next(c for c in load_author_bank(author_dir) if c.name == "minutes_voice"),
        next(c for c in load_author_bank(author_dir) if c.name == "slack_voice"),
    ]
    text, truth = mix_document(cards, "ABAB")
    assert truth.notes == "minutes_voice / slack_voice"
    assert truth.changes == (1, 1, 1)
    assert len(split_paragraphs(text)) == 4
