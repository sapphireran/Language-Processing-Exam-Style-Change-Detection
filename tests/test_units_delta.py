from seamtrace.cusum import cusum_scores
from seamtrace.delta import burrows_delta
from seamtrace.features import FeatureTable
from seamtrace.units import split_units


def test_auto_prefers_lines() -> None:
    text = "First sentence.\nSecond sentence.\n"
    assert split_units(text) == ["First sentence.", "Second sentence."]


def test_paragraph_mode() -> None:
    text = "Para one still here.\nStill.\n\nPara two."
    assert split_units(text, mode="paragraphs") == ["Para one still here. Still.", "Para two."]


def test_delta_zero_on_identical_units() -> None:
    table = FeatureTable.from_units(["The of and to the of and to.", "The of and to the of and to."])
    value = burrows_delta(table.units[0], table.units[1], table)
    assert value == 0.0


def test_cusum_length() -> None:
    table = FeatureTable.from_units(["Aaa.", "Bbb ccc.", "Ddd eee fff."])
    assert len(cusum_scores(table)) == 2
