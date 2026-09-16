from isogloss.features import extract


SKIFF = "I don't trust this. I'll fix it and I will sit. So I keep my knife."
ROLL = (
    "The committee shall receive the log. It was resolved that members "
    "must initial the sheet. The clerk shall retain a copy."
)
TWINE = "You'll want to wait a bit. Don't rush. Maybe check your gloves? Sort of listen."
VELLUM = (
    "We ought to refuse the easy story. One therefore waits. However, "
    "this does not imply silence."
)
FLINT = "Wind 12 kn. Tide 1.8 m. Bags 3 at 25 kg. Leak: none."
BRINE = "A stack shall be faced. Turves must be set. Water shall not stand."


def test_skiff_is_first_person_contracted() -> None:
    row = extract(SKIFF)
    assert row.i_rate > 0.1
    assert row.contraction_rate > 0.05
    assert row.you_rate == 0
    assert row.digit_rate == 0


def test_roll_is_minutes() -> None:
    row = extract(ROLL)
    assert row.i_rate == 0
    assert row.you_rate == 0
    assert row.contraction_rate == 0
    assert row.deontic_rate > 0
    assert row.past_copula_rate > 0
    assert row.the_rate > 0.1


def test_twine_is_you_and_hedge() -> None:
    row = extract(TWINE)
    assert row.you_rate > 0.05
    assert row.hedge_rate > 0
    assert row.question_rate > 0


def test_vellum_is_we_and_formal() -> None:
    row = extract(VELLUM)
    assert row.we_rate > 0 or row.one_rate > 0
    assert row.formal_rate > 0
    assert row.contraction_rate == 0


def test_flint_is_digits_without_person() -> None:
    row = extract(FLINT)
    assert row.digit_rate > 0.2
    assert row.i_rate == 0
    assert row.you_rate == 0
    assert row.we_rate == 0


def test_brine_is_shall_without_was() -> None:
    row = extract(BRINE)
    assert row.deontic_rate > 0.05
    assert row.past_copula_rate == 0
    assert row.contraction_rate == 0


def test_nouns_do_not_appear_as_channels() -> None:
    from isogloss.features import CHANNELS

    banned = {"eel", "hop", "kiln", "peat", "sett", "topic", "noun"}
    assert banned.isdisjoint(CHANNELS)
