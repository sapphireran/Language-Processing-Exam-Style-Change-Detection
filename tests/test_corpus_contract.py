from collections import Counter

from seamtrace.corpus import load_teaching_corpus, write_manifest


def test_every_file_has_matching_labels() -> None:
    docs = load_teaching_corpus()
    assert len(docs) == 22
    for doc in docs:
        assert len(doc.changes) == len(doc.units) - 1
        assert set(doc.changes) <= {0, 1}
        assert doc.authors >= 1
        assert doc.tier in {"easy", "medium", "hard", "control", "collage"}


def test_control_is_all_stay() -> None:
    for doc in load_teaching_corpus():
        if doc.tier == "control":
            assert doc.authors == 1
            assert sum(doc.changes) == 0


def test_collage_author_count_is_not_naive() -> None:
    collages = [d for d in load_teaching_corpus() if d.tier == "collage"]
    assert collages
    for doc in collages:
        naive = 1 + sum(doc.changes)
        assert doc.authors < naive


def test_tier_inventory() -> None:
    counts = Counter(doc.tier for doc in load_teaching_corpus())
    assert counts["easy"] == 5
    assert counts["medium"] == 7
    assert counts["hard"] == 5
    assert counts["control"] == 3
    assert counts["collage"] == 2


def test_manifest_roundtrip(tmp_path) -> None:
    dest = write_manifest(tmp_path / "manifest.json")
    text = dest.read_text(encoding="utf-8")
    assert "problem-14-two-bakers.txt" in text
    assert text.count('"file"') == 22
