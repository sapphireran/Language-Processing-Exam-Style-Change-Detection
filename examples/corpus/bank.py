"""Original teaching documents. Nothing here is from a shared task.

Each record is a dict:

    id, title, site, voices, units, authors, changes, return_author,
    expected_error, notes

``site`` is one of easy / medium / hard / control / return / collage / gift / paste.

Hard documents are written in the *same* house voice on purpose. The
default detector is allowed to miss them; that miss is the exam point.
"""

from __future__ import annotations

DOCUMENTS: list[dict] = []


def _add(**kwargs) -> None:
    DOCUMENTS.append(kwargs)


# ---------------------------------------------------------------------------
# Easy: loud register folds. Default detector should hit the middle cut.
# ---------------------------------------------------------------------------

_add(
    id="problem-01-kiln-then-notice",
    title="Community kiln daybook then fire-hall notice",
    site="easy",
    voices=["stall", "notice"],
    units=[
        "The kiln ran hot after lunch and I kept the damper cracked so Mira's bowls wouldn't pink.",
        "I told her I'd babysit the cone and I meant it; the copper blush still looks greedy.",
        "I'm heading home once the pyrometer drops under two hundred.",
        "Persons entering the firing hall shall wear closed footwear and a cotton apron.",
        "Dampers shall not be adjusted except by the duty technician listed on the rota.",
        "The kiln shall remain locked until the recorded temperature falls below ninety degrees Celsius.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Stall first person + contractions against shall/must notice. Clean exam hinge.",
)

_add(
    id="problem-02-dumpling-then-inspection",
    title="Night-market dumpling notes then inspection form",
    site="easy",
    voices=["stall", "notice"],
    units=[
        "I'm telling Mira the dough's too wet tonight and I can't get a clean pleat.",
        "Don't wait up; I'll freeze the extra filling and try the thinner skins tomorrow.",
        "Vendors shall maintain a probe thermometer at the point of sale.",
        "A written incident record must be completed if any customer reports undercooked filling.",
        "Pursuant to the night-market code, raw pork shall be held below five degrees Celsius.",
    ],
    authors=2,
    changes=[0, 1, 0, 0],
    notes="Food-stall chat versus health-code English. Same stall, new genre.",
)

_add(
    id="problem-03-marbling-then-accession",
    title="Paper-marbling studio then museum accession card",
    site="easy",
    voices=["letter", "notice"],
    units=[
        "You would have liked the size of the stone this morning; I floated a comb that finally behaved.",
        "I kept a corner of the sheet for you because the ochre vein looks like a river mouth.",
        "Don't let me forget to size another batch before Thursday.",
        "Object 14.2 shall be stored flat in a solander box lined with unbuffered tissue.",
        "Accession photographs must include a scale bar and the assigned catalogue number.",
        "Handling shall be restricted to staff listed on the paper-conservation rota.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Warm second-person letter into museum shall-language.",
)

_add(
    id="problem-04-icehut-then-thickness",
    title="Ice-hut journal then municipal thickness notice",
    site="easy",
    voices=["stall", "notice"],
    units=[
        "I drilled twice before I trusted the black ice; it's singing but I still don't like the south crack.",
        "I'll pull the hut back ten metres if the wind keeps stacking slush against the door.",
        "Public ice shall be considered unsafe below fifteen centimetres of clear measurement.",
        "Vehicles must not enter the marked zone until the harbourmaster posts a green board.",
        "A thickness log shall be filed by noon on each day the hut field is occupied.",
    ],
    authors=2,
    changes=[0, 1, 0, 0],
    notes="First-person ice journal versus municipal must/shall.",
)

_add(
    id="problem-05-glass-then-conservation",
    title="Stained-glass daybook then conservation report",
    site="easy",
    voices=["stall", "notice"],
    units=[
        "I lost a jewel in the south quatrefoil and I can't fake the cobalt with what I've got on the bench.",
        "Mira's coming by after lunch; I'll have her hold the cartoon while I re-lead the mitre.",
        "Panels shall be supported in a vertical rack with felted battens at each saddle bar.",
        "Replacement glass must be documented with a melt batch number and a rubbing of the original cut.",
        "No soldering shall proceed until the conservation file records the intended alloy.",
    ],
    authors=2,
    changes=[0, 1, 0, 0],
    notes="Workshop I/I'll versus conservation must/shall.",
)

_add(
    id="problem-06-radio-then-compliance",
    title="Late-night radio rundown then compliance note",
    site="easy",
    voices=["chat", "notice"],
    units=[
        "yeah I'm sliding the interview because the tape's a mess and I don't have a clean in-point.",
        "tell Jan I'll dump the weather bed under the second song if she still wants the sting.",
        "Licensees shall retain a timed log of all sponsored mentions for ninety days.",
        "A compliance officer must be notified before any live call is placed after twenty-three hundred.",
        "Profanity delay shall remain armed for the duration of unsupervised presentation.",
    ],
    authors=2,
    changes=[0, 1, 0, 0],
    notes="Wire/chat rundown versus broadcast-compliance English.",
)

_add(
    id="problem-07-climbing-then-incident",
    title="Route-setting chat then incident report",
    site="easy",
    voices=["chat", "notice"],
    units=[
        "I'm yanking the orange crimp on lane four; it's spinning and I don't trust it for the kids' night.",
        "Don't set the roof problem till I've swapped the bolt, yeah?",
        "Any spinning hold shall be taken out of service and tagged by the duty setter.",
        "An incident form must be completed if a hold rotates under load.",
        "Routes shall not be reopened until a second setter has torque-checked the hardware.",
    ],
    authors=2,
    changes=[0, 1, 0, 0],
    notes="Gym chat versus incident-form shall/must.",
)

_add(
    id="problem-08-seedlib-then-phyto",
    title="Seed-library checkout notes then phytosanitary notice",
    site="easy",
    voices=["letter", "notice"],
    units=[
        "You borrowed the speckled trout lettuce last May and I still remember how well it did in your wet bed.",
        "I've put aside a few extra beet seeds for you; don't worry about the packet date.",
        "Seed leaving the parish library shall be accompanied by a completed phytosanitary slip.",
        "Lots must be freeze-stored for seventy-two hours before any inter-county transfer.",
        "A recall notice shall be posted if germination falls below the published threshold.",
    ],
    authors=2,
    changes=[0, 1, 0, 0],
    notes="Second-person librarian warmth versus phytosanitary shall.",
)

# ---------------------------------------------------------------------------
# Medium: same topic, two genres. Still a register fold, slightly quieter.
# ---------------------------------------------------------------------------

_add(
    id="problem-09-cooper-invoice-then-letter",
    title="Barrel invoice then thank-you letter",
    site="medium",
    voices=["notice", "letter"],
    units=[
        "Invoice 441 shall be settled within fourteen days of the hoops being seated.",
        "The cask must be listed as toasted medium and the bung stave shall remain unmarked.",
        "Delivery charges shall be payable by the cellar prior to collection.",
        "You would have smiled at how quietly the last hoop went home; I've already set the offcut aside.",
        "I've kept that piece of oak for you; it still smells like the toasting fire.",
        "Don't thank me in a hurry — come see the cellar when the first fill is in.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Same cooperage, invoice English then a personal letter.",
)

_add(
    id="problem-10-lock-sop-then-chat",
    title="Mortise SOP then apprentice chat",
    site="medium",
    voices=["notice", "chat"],
    units=[
        "The mortise shall be cut square to the stile and the strike must sit flush with the jamb.",
        "A second key shall be bagged and labelled before the door is returned to service.",
        "Lubricant must be graphite only; oil is not permitted on the ward set.",
        "yeah I'm done with the church door, the ward's clean and I didn't nick the plate.",
        "tell the office I'll drop the spare key in the tin, don't leave it on the bench.",
    ],
    authors=2,
    changes=[0, 0, 1, 0],
    notes="Procedure then the apprentice reporting the same job in chat.",
)

_add(
    id="problem-11-bind-spec-then-zine",
    title="Binding specification then zine blurb",
    site="medium",
    voices=["notice", "stall"],
    units=[
        "Signatures shall be sewn on three tapes and the spine must be lined with unbleached linen.",
        "Endpapers are to be made of 120gsm laid stock; leather corners shall not extend past twenty millimetres.",
        "I'm sewing this one on tapes I dyed in onion skins and I can't stop touching the spine.",
        "Don't ask me for a clean edition number; I'll write the count on the colophon in pencil.",
        "If you want a copy, I'll hold one back from the Saturday table.",
    ],
    authors=2,
    changes=[0, 1, 0, 0],
    notes="Workshop spec versus the binder talking about the same book.",
)

_add(
    id="problem-12-harbour-minutes-then-skipper",
    title="Harbour minutes then skipper chat",
    site="medium",
    voices=["minutes", "chat"],
    units=[
        "The chair noted that the inner pontoon remains oversubscribed on Friday evenings.",
        "It was resolved that visiting yachts shall radio the harbour office before entering the cut.",
        "Action: the clerk will post the revised rafting rule on the board by Wednesday.",
        "yeah I'm rafting on the inside tonight, don't wait for the office if the VHF's busy.",
        "tell Jan I'll move if a visitor needs the face, I'm not precious about it.",
    ],
    authors=2,
    changes=[0, 0, 1, 0],
    notes="Committee minutes versus the skipper who will actually raft.",
)

# ---------------------------------------------------------------------------
# Hard: two specialists, same register. Expect same_register_miss.
# ---------------------------------------------------------------------------

_add(
    id="problem-13-two-bellfounders",
    title="Two bellfounders on the same tenor",
    site="hard",
    voices=["notebook", "notebook"],
    expected_error="same_register_miss",
    units=[
        "We recorded partials of the tenor after the second scrape and the hum note remained a little sharp.",
        "The waist metal appears consistent with the 1911 pour; we have not yet opened the crown.",
        "Our strike-note reading at the west door was approximately 438, perhaps shaded by the scaffolding.",
        "We then measured the soundbow thickness at six stations and found the south quadrant slightly proud.",
        "The same 1911 alloy is suggested by the file colour; our notes remain provisional until the mould is compared.",
        "Partial series after the scrape still appears consistent with a tenor that has not been put back in tune.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Gold hinge after unit 3. Both voices are hedged scientific we. Default cut should stay quiet.",
)

_add(
    id="problem-14-two-map-colourists",
    title="Two map colourists on the same parish sheet",
    site="hard",
    voices=["notebook", "notebook"],
    expected_error="same_register_miss",
    units=[
        "We washed the woodland tint in two dilute passes and the paper remained acceptably flat.",
        "Boundary lakes appear slightly greener than the 1890 exemplar; perhaps the lake pigment has shifted.",
        "Our notes record a possible offset of one millimetre at the north register mark.",
        "We followed the same wash order and found the woodland still a little high relative to the exemplar.",
        "The lake pigment is approximately consistent with a later bottle; our match remains tentative.",
        "Register at the north tick still appears to sit about a millimetre east.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Same parish sheet, two colourists, same hedges and we.",
)

_add(
    id="problem-15-two-organ-tuners",
    title="Two organ tuners on the same swell mixture",
    site="hard",
    voices=["notebook", "notebook"],
    expected_error="same_register_miss",
    units=[
        "We set the swell mixture from middle C and the tierce still seemed a little bright in the nave.",
        "Wind pressure at the trunk was approximately 75 mm; our gauge may be optimistic.",
        "We still find the twelfth consistent with last year's note, perhaps a shade keener on D.",
        "We repeated the middle-C set and still found the tierce bright when heard from the nave floor.",
        "Trunk pressure remains around 75 mm on our gauge; the reading is only approximate.",
        "We still find the twelfth on D a little keen, consistent with the previous service notes.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Same mixture, two tuners, notebook register throughout.",
)

_add(
    id="problem-16-two-fog-keepers",
    title="Two fog-signal keepers on the same horn",
    site="hard",
    voices=["notebook", "notebook"],
    expected_error="same_register_miss",
    units=[
        "We timed the horn at twelve seconds and the echo off the quarry still seemed late.",
        "Compressor temperature was approximately forty degrees; perhaps the shed door should stay shut.",
        "Our log suggests the character remains two blasts, consistent with the published list.",
        "We timed the same interval and the quarry echo still appeared delayed by a fraction.",
        "The compressor is still around forty degrees in our notes; the door question remains open.",
        "Character of the signal still appears to be two blasts, consistent with the list.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Same horn, two keepers, same hedges.",
)

_add(
    id="problem-17-two-night-clerks",
    title="Two night clerks on the same lodging house",
    site="hard",
    voices=["notebook", "notebook"],
    expected_error="same_register_miss",
    units=[
        "We recorded twenty-two beds occupied and the kitchen gas still appeared to be on a low flame.",
        "The back stair light is perhaps intermittent; our note is consistent with last Tuesday.",
        "A complaint about the cistern was logged at 02:10; we have not yet inspected the roof tank.",
        "Occupied beds were again twenty-two in our count; the kitchen flame still appears low.",
        "Intermittent lighting on the back stair remains consistent with the earlier note.",
        "The cistern complaint is still in the book; our inspection of the tank has not occurred.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Same lodging house, two night clerks, same notebook.",
)

_add(
    id="problem-18-two-coopers-notes",
    title="Two coopers measuring the same puncheon",
    site="hard",
    voices=["notebook", "notebook"],
    expected_error="same_register_miss",
    units=[
        "We measured the bulge at 890 mm and the croze still appeared true.",
        "We judged the toast colour approximately medium, perhaps a shade darker at the head.",
        "Our bung-hole diameter remains consistent with the cellar's requested 50 mm.",
        "We measured the bulge again at 890 mm and the croze still seemed true.",
        "We still judged the toast approximately medium, perhaps darker near the head stave.",
        "Our bung-hole diameter still appears consistent with the 50 mm request.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Same puncheon, two notebooks, no register fold.",
)

# ---------------------------------------------------------------------------
# Control: one author, three topics. Should stay quiet.
# ---------------------------------------------------------------------------

_add(
    id="problem-19-stall-three-topics",
    title="One stall voice: dumplings, a night bus, a cat",
    site="control",
    voices=["stall", "stall", "stall"],
    expected_error="topic_false_alarm",
    units=[
        "I'm folding slower tonight and I don't rush the first pleat.",
        "I'm freezing the leftover pork and I don't want to guess the fridge.",
        "I'm missing the night bus again and I can't face the hill in this rain.",
        "I'm skipping the stop and I don't want to wait in this wind.",
        "I'm watching the cat on the kiln roof and I don't know how she climbs.",
        "I'm leaving the landing window open and I don't want her stuck up there.",
    ],
    authors=1,
    changes=[0, 0, 0, 0, 0],
    notes="Topic changes at 2 and 4. Register does not. A content model should twitch; we should not.",
)

_add(
    id="problem-20-notice-three-topics",
    title="One notice voice: ice, kiln, seed lot",
    site="control",
    voices=["notice", "notice", "notice"],
    expected_error="topic_false_alarm",
    units=[
        "Public ice shall be considered unsafe below fifteen centimetres of clear measurement.",
        "Vehicles must not enter the marked zone until a green board is posted.",
        "The kiln shall remain locked until the recorded temperature falls below ninety degrees.",
        "Dampers must not be adjusted except by the duty technician.",
        "Seed leaving the parish shall be accompanied by a completed phytosanitary slip.",
        "Lots must be freeze-stored for seventy-two hours before inter-county transfer.",
    ],
    authors=1,
    changes=[0, 0, 0, 0, 0],
    notes="Three notice topics, one bureaucratic voice.",
)

_add(
    id="problem-21-chat-three-topics",
    title="One chat voice: kiln, bus, radio",
    site="control",
    voices=["chat", "chat", "chat"],
    expected_error="chat_jitter",
    units=[
        "yeah kiln's still screaming, don't come by till I text.",
        "I'll crack the damper and then I'm gone, lol.",
        "bus was late again and I didn't get a seat, typical.",
        "tell Jan I'm walking, don't wait.",
        "tape's a mess btw, I'll dump the weather bed if I have to.",
        "yeah I'm sliding the interview, don't @ me.",
    ],
    authors=1,
    changes=[0, 0, 0, 0, 0],
    notes="Short chat units jitter length and vocatives. A known false-alarm risk.",
)

# ---------------------------------------------------------------------------
# Return, collage, gift, paste.
# ---------------------------------------------------------------------------

_add(
    id="problem-22-kiln-return",
    title="Kiln stall, notice, stall again",
    site="return",
    voices=["stall", "notice", "stall"],
    return_author=True,
    expected_error="return_undercount",
    units=[
        "I kept the damper cracked after lunch and I still don't like that top-shelf pink.",
        "I'll babysit the cone till Mira gets back from the supply run.",
        "Persons entering the firing hall shall wear closed footwear and a cotton apron.",
        "The kiln shall remain locked until the recorded temperature falls below ninety degrees.",
        "I'm back and the pyrometer's kinder now; I told you the blush would settle.",
        "Don't lock me out, I'll write the cone time on the board before I go.",
    ],
    authors=2,
    changes=[0, 1, 0, 1, 0],
    notes="authors=2 but 1+sum(changes)=3. Naive author count over-counts the return.",
)

_add(
    id="problem-23-four-voice-collage",
    title="Four house voices on a Saturday in the parish",
    site="collage",
    voices=["stall", "notice", "notebook", "chat"],
    units=[
        "I'm taking the extra beet seeds to the Saturday table and I can't promise they'll last the morning.",
        "Seed leaving the parish library shall be accompanied by a completed slip and lots must remain freeze-stored.",
        "We recorded germination at approximately eighty percent; perhaps the wet drawer is consistent with the lower tray.",
        "yeah I'll grab a packet if there's any left, don't save me one.",
    ],
    authors=4,
    changes=[1, 1, 1],
    notes="One unit per voice. A collage, not a realistic letter.",
)

_add(
    id="problem-24-gift-abstract",
    title="Student notebook abstract then supervisor rewrite",
    site="gift",
    voices=["notebook", "notice"],
    expected_error=None,
    units=[
        "We measured thallus diameter on the south elevation and the values still seemed a little low.",
        "Perhaps the rain shadow of the buttress is consistent with the smaller discs we recorded.",
        "Our notes are only a first pass; we have not yet compared the north elevation.",
        "Thallus diameter shall be reported as a mean of six stations on each elevation.",
        "Results must be presented without conjecture about rain shadows until a second season is recorded.",
        "Comparison with the north elevation is required before the abstract is submitted.",
    ],
    authors=2,
    changes=[0, 0, 1, 0, 0],
    notes="Gift authorship: student hedges, supervisor deletes the hedges and installs must/shall.",
)

_add(
    id="problem-25-exam-two-answers",
    title="Two exam answers on the same style-change prompt",
    site="paste",
    voices=["notebook", "stall"],
    units=[
        "A style change is a fold in register, not a change of topic; we distinguish the two by closed-class rates.",
        "Accuracy is a poor metric here because most inter-sentential boundaries are seams, not folds.",
        "I'm just going to say it's when the writing starts sounding like someone else and I hope that's enough.",
        "I'm not overthinking it; I can hear the join and I hope that's the point.",
    ],
    authors=2,
    changes=[0, 1, 0],
    notes="Paste / two candidates. First answer is notebook-exam English; second is stall panic.",
)

_add(
    id="problem-26-minutes-then-letter-then-notice",
    title="Harbour minutes, personal letter, then a notice",
    site="collage",
    voices=["minutes", "letter", "notice"],
    units=[
        "The chair noted that visiting yachts continue to enter the cut without a radio call.",
        "It was resolved that a revised rafting rule shall be posted by Wednesday.",
        "You would have liked how quiet the inner pontoon was after the meeting; I stayed to watch the tide.",
        "I've left a sketch of the new rafting rule on your chart table; don't let the cat sit on it.",
        "Visiting yachts shall radio the harbour office before entering the cut.",
        "Rafting on the face must be offered to visitors before any resident takes a second berth.",
    ],
    authors=3,
    changes=[0, 1, 0, 1, 0],
    notes="Three voices, two folds. Minutes and notice are both formal-ish; the letter in the middle is the giveaway.",
)


def by_id() -> dict[str, dict]:
    return {d["id"]: d for d in DOCUMENTS}


def manifest() -> dict:
    return {
        "n_documents": len(DOCUMENTS),
        "sites": sorted({d["site"] for d in DOCUMENTS}),
        "documents": [
            {
                "id": d["id"],
                "title": d["title"],
                "site": d["site"],
                "voices": d["voices"],
                "authors": d["authors"],
                "n_units": len(d["units"]),
                "n_folds": sum(d["changes"]),
                "return_author": bool(d.get("return_author")),
                "expected_error": d.get("expected_error"),
            }
            for d in DOCUMENTS
        ],
    }
