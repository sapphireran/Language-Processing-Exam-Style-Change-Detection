from isogloss.detect import detect_paragraphs


SKIFF_A = (
    "I don't like the gap. I'll drive a stake and I'll lash it. "
    "So I sit on the bank and I wait."
)
SKIFF_B = (
    "I rinse the bag. I don't beat it on a stone. I'll hang it and "
    "then I keep the needle."
)
ROLL_A = (
    "The committee shall receive the log before noon. Members must "
    "initial the sheet. It was resolved that no sack shall leave."
)
ROLL_B = (
    "The clerk shall retain a second copy. It was noted that the door "
    "was warped. Members shall not open the kiln."
)


def test_same_house_stays_quiet() -> None:
    det = detect_paragraphs([SKIFF_A, SKIFF_B, SKIFF_A])
    assert det.changes == [0, 0]


def test_skiff_to_roll_fires() -> None:
    det = detect_paragraphs([SKIFF_A, SKIFF_B, ROLL_A, ROLL_B])
    assert det.changes[1] == 1
    assert det.hinges[1].votes >= 3


def test_empty_and_single() -> None:
    assert detect_paragraphs([]).changes == []
    assert detect_paragraphs(["Only one unit."]).changes == []
