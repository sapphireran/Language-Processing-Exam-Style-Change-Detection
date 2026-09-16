#!/usr/bin/env python3
"""Write the original synthetic exam corpus under data/synthetic/.

Texts are house-authored for this personal repo. Re-run only if you are
intentionally regenerating the study set.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "synthetic"

# Each problem: difficulty, split, topic, list of (author_id, sentence)
# Sentences must stay one author each and end in terminal punctuation.

CORPUS: list[dict] = [
    # ---------------------------------------------------------------------
    # EASY: topic and style move together
    # ---------------------------------------------------------------------
    {
        "difficulty": "easy",
        "pid": "001",
        "split": "train",
        "topic": "reef ecology → ruined dinner → gear inches",
        "turns": [
            (
                "mira",
                "A growing body of observational work suggests that branching coral cover remains relatively sensitive to brief marine heatwaves, although local recovery appears uneven.",
            ),
            (
                "mira",
                "However, the same surveys indicate that herbivorous fish density may modestly buffer bleaching stress when turf algae are already established.",
            ),
            (
                "mira",
                "These associations are generally treated as provisional, because night-time temperature logs were somewhat sparse across the outer reef flat.",
            ),
            (
                "jules",
                "I don't even know how the pasta water boiled over that fast, I looked away for like ten seconds.",
            ),
            (
                "jules",
                "The sauce was pretty decent until I dumped in the salt twice and then pretended that was a choice.",
            ),
            (
                "jules",
                "Anyway I ate it standing at the counter and it still counted as dinner, you know?",
            ),
            (
                "hale",
                "Chainstay length was 430 mm. Gear inches were recorded at 46/16.",
            ),
            (
                "hale",
                "Cadence at 18 km/h was 74 rpm. Tire pressure was 4.2 bar.",
            ),
        ],
    },
    {
        "difficulty": "easy",
        "pid": "002",
        "split": "train",
        "topic": "balcony plants → tram rain → urban heat",
        "turns": [
            (
                "jules",
                "I keep meaning to water the balcony plants before they go crispy, and then I remember right as I'm leaving.",
            ),
            (
                "jules",
                "The basil is really dramatic about it; one skipped day and it looks personally betrayed.",
            ),
            (
                "jules",
                "I'm not buying another pot until I can keep this one alive, that's the deal.",
            ),
            (
                "nell",
                "Rain stitched itself across the tram glass until the streetlights smeared into long pale coins.",
            ),
            (
                "nell",
                "A wet coat at the next pole held the smell of iron and oranges; nobody spoke.",
            ),
            (
                "nell",
                "By the river stop the droplets had slowed into a patient ticking, as if the window were counting us.",
            ),
            (
                "mira",
                "Recent canopy inventories suggest that late-evening surface temperatures remain relatively elevated where street trees are sparse, although the magnitude varies by canyon width.",
            ),
            (
                "mira",
                "A modest increase in crown cover appears associated with cooler asphalt, yet the observational design cannot isolate traffic volume.",
            ),
            (
                "mira",
                "These results are therefore presented as associations rather than as a general causal claim.",
            ),
        ],
    },
    {
        "difficulty": "easy",
        "pid": "003",
        "split": "train",
        "topic": "titration → library lighting → missed bus",
        "turns": [
            ("hale", "Endpoint volume was 18.4 mL. Indicator change was recorded at 21 C."),
            ("hale", "Blank correction was 0.12 mL. Replicate spread was 0.3 mL."),
            ("hale", "Normality was computed as 0.101 N. Glassware class was A."),
            (
                "mira",
                "However, the lighting logs suggest that late opening hours are associated with a relatively higher rate of unfinished reading sessions.",
            ),
            (
                "mira",
                "The pattern appears somewhat stronger on upper floors, although occupancy sensors were only recently calibrated.",
            ),
            (
                "mira",
                "One should therefore treat the floor-level contrast as provisional pending a longer observation window.",
            ),
            (
                "jules",
                "I ran for the bus and still missed it, which is very on brand for a Tuesday.",
            ),
            (
                "jules",
                "That's fine, I'll walk and complain about it the whole way, I'm good at both.",
            ),
        ],
    },
    {
        "difficulty": "easy",
        "pid": "004",
        "split": "train",
        "topic": "bakery dawn → oven temperatures",
        "turns": [
            (
                "nell",
                "Before the street had a colour, the bakery window was already a soft gold rectangle in the dark.",
            ),
            (
                "nell",
                "Flour hung in the doorway like weather; a tray of loaves ticked as they cooled.",
            ),
            (
                "nell",
                "Someone laughed once in the back room, then the laugh folded itself away.",
            ),
            (
                "nell",
                "I stood long enough for the glass to mist where my breath met it, and the loaves kept their small crackling conversation.",
            ),
            ("hale", "Deck temperature was 240 C. Steam injection lasted 8 s."),
            ("hale", "Load mass was 12.6 kg. Crust colour target was 65 on the bake scale."),
            ("hale", "Cooling rack time was 40 min. Internal crumb temperature was 32 C at bag."),
        ],
    },
    {
        "difficulty": "easy",
        "pid": "005",
        "split": "val",
        "topic": "wetland birds → neighbours → river fog",
        "turns": [
            (
                "mira",
                "Point counts suggest that reed warbler detections are relatively higher after prolonged southerly winds, although observer fatigue may contribute.",
            ),
            (
                "mira",
                "The association appears modest once water level is included, and it should not be read as a migration forecast.",
            ),
            (
                "mira",
                "However, the same transect continues to yield a fairly stable dawn chorus despite weekend disturbance.",
            ),
            (
                "jules",
                "The people upstairs are moving a wardrobe again and I don't think they like the floor more than I do.",
            ),
            (
                "jules",
                "It's pretty late for furniture to have opinions, I'm just saying.",
            ),
            (
                "jules",
                "I put a podcast on and lost the argument anyway.",
            ),
            (
                "nell",
                "Fog took the river by the elbows and walked it out of sight.",
            ),
            (
                "nell",
                "A single oar-knock carried, then the water remembered how to be quiet.",
            ),
        ],
    },
    {
        "difficulty": "easy",
        "pid": "006",
        "split": "test",
        "topic": "thrift jacket → dye chemistry → tensile numbers",
        "turns": [
            (
                "jules",
                "I found this jacket in a thrift place and it's a little huge, which I decided is the style.",
            ),
            (
                "jules",
                "There's a bus ticket from 2014 in the pocket and I'm not throwing that away, obviously.",
            ),
            (
                "jules",
                "If anyone asks, I bought it for the lining, not because I was cold and impulsive.",
            ),
            (
                "mira",
                "Vat dyeing of cellulose is generally described as a reduction–oxidation sequence, although practical shade control remains relatively sensitive to liquor ratio.",
            ),
            (
                "mira",
                "These notes suggest that incomplete reduction appears as dullness rather than as a simple depth error.",
            ),
            (
                "mira",
                "The account is therefore framed as a classroom summary, not as a mill specification.",
            ),
            ("hale", "Grab strength was 420 N. Elongation at break was 18%."),
            ("hale", "Gauge length was 100 mm. Crosshead speed was 50 mm/min."),
        ],
    },
    {
        "difficulty": "easy",
        "pid": "007",
        "split": "train",
        "topic": "greenhouse → basil → water potential",
        "turns": [
            (
                "nell",
                "The abandoned greenhouse still held a weather of its own: warmer, greener, faintly sweet with old tomato dust.",
            ),
            (
                "nell",
                "Broken panes made a keyboard of light across the path; I stepped only on the dark keys.",
            ),
            (
                "nell",
                "Somewhere a tap ticked, counting a garden that had already left.",
            ),
            (
                "jules",
                "I'm trying to grow basil again and I swear it wilted out of spite.",
            ),
            (
                "jules",
                "I watered it, I turned it, I talked to it, I'm not proud of the talking.",
            ),
            (
                "jules",
                "If this one dies I'm switching to the plastic kind and I won't apologise.",
            ),
            (
                "mira",
                "Leaf water potential is typically reported as a relatively more negative value under midday vapour-pressure deficit, although pot size may confound the comparison.",
            ),
            (
                "mira",
                "The present notes merely suggest that a predawn reading remains the cleaner baseline when stomatal behaviour is of interest.",
            ),
        ],
    },
    {
        "difficulty": "easy",
        "pid": "008",
        "split": "test",
        "topic": "GPS survey → ridge walk → getting lost",
        "turns": [
            ("hale", "Control point A was 54.3721 N, 2.7014 W. Horizontal RMS was 0.08 m."),
            ("hale", "Occupation time was 12 min. PDOP was 1.9."),
            ("hale", "Antenna height was 1.82 m. Epoch interval was 1 s."),
            (
                "nell",
                "The same ridge, walked without a number, kept offering the same unrecorded generosity of wind.",
            ),
            (
                "nell",
                "Heather gave way to stone; the stone gave way to a view that refused to stay still.",
            ),
            (
                "nell",
                "I did not take a mark; I took the cold in my teeth and called that a record.",
            ),
            (
                "jules",
                "I got lost on that hike, which is impressive because there's basically one path.",
            ),
            (
                "jules",
                "My phone said I was in a lake and I was pretty sure I wasn't, but I did sit down.",
            ),
            (
                "jules",
                "Don't follow me if you actually want to get anywhere, I'm a cautionary tale with snacks.",
            ),
        ],
    },
    # ---------------------------------------------------------------------
    # MEDIUM: one subject (city cycling), leftover lexical cues
    # ---------------------------------------------------------------------
    {
        "difficulty": "medium",
        "pid": "001",
        "split": "train",
        "topic": "city cycling — geometry, commute, measurements",
        "turns": [
            (
                "mira",
                "Frame geometry is often discussed as if trail and wheelbase were independent levers, although their combined effect on low-speed stability remains relatively entangled.",
            ),
            (
                "mira",
                "A somewhat steeper head angle appears associated with quicker steering, yet the observational literature is generally cautious about declaring a preferred city setup.",
            ),
            (
                "mira",
                "These remarks are therefore offered as a reading of trade-offs, not as a fitting prescription.",
            ),
            (
                "jules",
                "I take the painted lane until it vanishes, which it always does right where the vans like to park.",
            ),
            (
                "jules",
                "This morning a driver opened a door and I didn't have a speech prepared, so I just made a noise.",
            ),
            (
                "jules",
                "I'm still going to bike it tomorrow, I'm just going to be slightly more dramatic about the gloves.",
            ),
            ("hale", "Head angle was 72.5 deg. Trail was 58 mm. Wheelbase was 1045 mm."),
            ("hale", "Tire width was 35 mm. Rolling circumference was 2160 mm."),
        ],
    },
    {
        "difficulty": "medium",
        "pid": "002",
        "split": "train",
        "topic": "city cycling — red light, infrastructure, lock",
        "turns": [
            (
                "nell",
                "At the red light the whole street inhaled; pedals hung like stopped clock hands.",
            ),
            (
                "nell",
                "A bus sighed beside me, close enough that the paint seemed to warm.",
            ),
            (
                "nell",
                "When green arrived it was less permission than a held note finally released.",
            ),
            (
                "mira",
                "Protected intersections are generally associated with fewer turning conflicts, although the available before–after studies remain relatively small.",
            ),
            (
                "mira",
                "However, paint-only treatments appear less stable once kerbside loading is allowed to return.",
            ),
            (
                "mira",
                "The present summary therefore treats physical separation as the more plausible default, pending better counts.",
            ),
            (
                "jules",
                "I locked the bike to the stand that isn't leaning and then I locked it again because I don't trust Tuesdays.",
            ),
            (
                "jules",
                "If someone steals it I'm going to be really boring about how I told myself this would happen.",
            ),
        ],
    },
    {
        "difficulty": "medium",
        "pid": "003",
        "split": "train",
        "topic": "city cycling — spokes, rain scene, café stop",
        "turns": [
            ("hale", "Spoke tension was 110 kgf on the drive side. Lateral true was 0.4 mm."),
            ("hale", "Nipple count was 32. Rim wear indicator was still visible."),
            ("hale", "Rotor thickness was 1.8 mm. Pad compound was organic."),
            (
                "nell",
                "Rain found the gaps in my coat and wrote cold commas down my spine.",
            ),
            (
                "nell",
                "The wheels threw a thin silver from the gutters; every doorway offered a different weather.",
            ),
            (
                "jules",
                "I stopped for a bun I didn't need and stood under the awning like that was a plan.",
            ),
            (
                "jules",
                "My socks were done for, I'm not going to pretend otherwise.",
            ),
        ],
    },
    {
        "difficulty": "medium",
        "pid": "004",
        "split": "train",
        "topic": "city cycling — returning Mira around Hale",
        "turns": [
            (
                "mira",
                "Modal share estimates for inner-city cycling remain relatively sensitive to how access trips are counted, although several inventories now attempt a consistent definition.",
            ),
            (
                "mira",
                "A modest rise in winter riding appears in the newer counts, yet weather normalisation is still only partly standardised.",
            ),
            ("hale", "Count site 4 recorded 612 cycles between 07:00 and 09:00."),
            ("hale", "Mean speed on the link was 18.4 km/h. Fifth-percentile speed was 12.1 km/h."),
            (
                "mira",
                "However, those two numbers should be read against a somewhat wet morning, which generally suppresses discretionary trips.",
            ),
            (
                "mira",
                "The safer claim is simply that the corridor continues to carry a non-trivial commuter load.",
            ),
        ],
    },
    {
        "difficulty": "medium",
        "pid": "005",
        "split": "val",
        "topic": "city cycling — night ride, scene, lamp spec",
        "turns": [
            (
                "jules",
                "I biked home in the dark and every taxi seemed personally interested in my elbows.",
            ),
            (
                "jules",
                "My light is pretty bright until I remember I didn't charge it, which is a classic me move.",
            ),
            (
                "jules",
                "Don't do this if you have better hobbies, I don't.",
            ),
            (
                "nell",
                "Shopfronts laid gold planks across the wet asphalt; I rode the brighter ones like a dare.",
            ),
            (
                "nell",
                "A fox crossed without hurry, as if the lane had always belonged to it.",
            ),
            ("hale", "Front lamp output was 400 lm. Beam cutoff was set to low."),
            ("hale", "Battery remaining was 38%. Flash mode was not used."),
        ],
    },
    {
        "difficulty": "medium",
        "pid": "006",
        "split": "test",
        "topic": "city cycling — cargo, groceries, alley",
        "turns": [
            (
                "mira",
                "Cargo bicycles are sometimes presented as a relatively complete substitute for short van trips, although kerb space and secure parking remain only partly solved.",
            ),
            (
                "mira",
                "The literature generally suggests a useful role for household errands, yet it is somewhat quieter on winter hills.",
            ),
            (
                "jules",
                "I tried to carry the shopping on the rack and a lemon escaped at the lights, I'm not a logistics company.",
            ),
            (
                "jules",
                "Someone handed it back and I said thanks like that was a normal way to meet people.",
            ),
            (
                "nell",
                "The alley smelled of cardboard and rain-warmed brick; the rack ticked as the bags settled.",
            ),
            (
                "nell",
                "I took the long way because the short way had already used up its kindness.",
            ),
        ],
    },
    {
        "difficulty": "medium",
        "pid": "007",
        "split": "train",
        "topic": "city cycling — brake numbers then policy voice",
        "turns": [
            ("hale", "Front stopping distance from 20 km/h was 4.1 m on dry asphalt."),
            ("hale", "Lever reach was 3 turns out. Hose length was 900 mm."),
            ("hale", "Pad wear was 1.2 mm remaining. Rotor runout was 0.15 mm."),
            (
                "mira",
                "Emergency stopping performance is often quoted without a wet-surface counterpart, which makes city comparisons relatively fragile.",
            ),
            (
                "mira",
                "However, even a cautious reading suggests that poorly adjusted levers remain a more common limitation than exotic compounds.",
            ),
            (
                "mira",
                "A maintenance reminder may therefore do more than a new specification sheet, although that claim is only modestly supported here.",
            ),
        ],
    },
    {
        "difficulty": "medium",
        "pid": "008",
        "split": "test",
        "topic": "city cycling — Nell, Jules, Nell again",
        "turns": [
            (
                "nell",
                "Sunday emptied the ring road until the painted bike glyphs looked almost ceremonial.",
            ),
            (
                "nell",
                "I rode the wide quiet as if it might be revoked for talking too loudly.",
            ),
            (
                "jules",
                "I went out for 'just twenty minutes' and came back with a pastry and a new opinion about bells.",
            ),
            (
                "jules",
                "That's not exercise, that's errands with extra narrative, I'm aware.",
            ),
            (
                "nell",
                "Later the bells of an unseen church stitched the afternoon back together.",
            ),
            (
                "nell",
                "The bike leaned in the hall and ticked, cooling, like a kettle that had done enough.",
            ),
        ],
    },
    # ---------------------------------------------------------------------
    # HARD: one subject (pour-over coffee), style only
    # ---------------------------------------------------------------------
    {
        "difficulty": "hard",
        "pid": "001",
        "split": "train",
        "topic": "pour-over coffee",
        "turns": [
            (
                "mira",
                "A modest bloom generally suggests that degassing remains relatively active, although the visual rise is only a rough proxy for roast age.",
            ),
            (
                "mira",
                "However, a somewhat cooler kettle appears associated with a slower drawdown, and one should not treat a single mug as a replication.",
            ),
            (
                "mira",
                "These notes therefore stay at the level of kitchen observation rather than a claimed extraction model.",
            ),
            (
                "jules",
                "I don't wait for the bloom to finish looking impressive, I just pour when the kettle's ready.",
            ),
            (
                "jules",
                "If it tastes bitter I add a splash of water and call it intentional, I'm not running a cafe.",
            ),
            (
                "jules",
                "The mug is the chipped one and that's part of the ritual, don't @ me.",
            ),
            ("hale", "Dose was 15.0 g. Water mass was 250 g. Grind was marked 16."),
            ("hale", "Bloom was 45 s at 50 g. Total time was 3:10. Yield was 220 g."),
        ],
    },
    {
        "difficulty": "hard",
        "pid": "002",
        "split": "train",
        "topic": "pour-over coffee",
        "turns": [
            (
                "nell",
                "The paper filter took on the faint sweet smell of a wet envelope; even the mug looked briefly ceremonial.",
            ),
            (
                "nell",
                "Water darkened through the bed in a slow eclipse, and the kettle clicked as if closing a parenthesis.",
            ),
            (
                "nell",
                "I held the mug with both hands and let the steam write nothing in particular.",
            ),
            ("hale", "Water temperature was 94 C. Filter rinse used 80 g."),
            ("hale", "Bed depth was approximately 18 mm. Pour height was 5 cm."),
            ("hale", "Brix was not measured. TDS was not measured."),
            (
                "nell",
                "Numbers would have stood in the doorway and refused to take their shoes off.",
            ),
            (
                "nell",
                "The last sip was quieter than the first, which is all I keep asking of a morning.",
            ),
        ],
    },
    {
        "difficulty": "hard",
        "pid": "003",
        "split": "train",
        "topic": "pour-over coffee",
        "turns": [
            (
                "jules",
                "I rinsed the filter because a video told me to, and I'm pretty sure I did it wrong anyway.",
            ),
            (
                "jules",
                "The grounds clumped like they were shy and I stirred them with a spoon like that was advanced.",
            ),
            (
                "mira",
                "Rinsing is typically justified as a way to reduce papery notes, although the effect appears relatively small once the filter is already well made.",
            ),
            (
                "mira",
                "A gentle stir during the bloom is sometimes said to improve wetting; the claim remains only modestly supported in casual kitchen tests.",
            ),
            (
                "mira",
                "However, channeling after an uneven pour is still a fairly plausible source of sharp cups.",
            ),
            (
                "jules",
                "See, that's a lot of words for 'pour slower', which is what I was going to do after I burned my tongue.",
            ),
            (
                "jules",
                "I still like it. I'm not becoming a person who owns a scale that talks.",
            ),
        ],
    },
    {
        "difficulty": "hard",
        "pid": "004",
        "split": "train",
        "topic": "pour-over coffee",
        "turns": [
            ("hale", "Kettle set point was 96 C. Gooseneck inner diameter was 5 mm."),
            ("hale", "Pulse pours were 50 g each. Interval was 15 s."),
            ("hale", "Final drawdown ended at 3:05. Bypass was 0 g."),
            (
                "mira",
                "Pulse pouring is often described as a relatively controllable way to manage bed height, although it can also introduce a somewhat staged extraction.",
            ),
            (
                "mira",
                "The safer laboratory-style claim is simply that consistent pulses reduce one source of between-mug variance.",
            ),
            (
                "mira",
                "Taste talk should probably remain separate from that bookkeeping, unless a triangle test is actually run.",
            ),
            ("hale", "Triangle tests were not run. Preference was not scored."),
            ("hale", "Notes were limited to time, mass, and grind mark."),
        ],
    },
    {
        "difficulty": "hard",
        "pid": "005",
        "split": "val",
        "topic": "pour-over coffee — Mira vs Nell stress pair",
        "turns": [
            (
                "mira",
                "Paper filters are generally credited with a cleaner cup, although they may also hold back a relatively larger share of oils.",
            ),
            (
                "mira",
                "However, cloth is sometimes preferred when mouthfeel is the stated aim, and the comparison remains somewhat under-specified in home notes.",
            ),
            (
                "mira",
                "A single morning mug cannot decide the argument; it can only keep the vocabulary honest.",
            ),
            (
                "nell",
                "The cloth filter, stained the colour of an old river map, softened the light as much as the drink.",
            ),
            (
                "nell",
                "Oil starred the surface; the bitterness arrived late, like a guest who knew the door would stay open.",
            ),
            (
                "nell",
                "I rinsed it carefully, as if the cloth remembered every kettle better than I did.",
            ),
            (
                "mira",
                "If those two descriptions disagree, the disagreement is probably register rather than a hidden variable in the grind.",
            ),
            (
                "mira",
                "Still, a repeated cloth brew would be the more responsible next step, should anyone insist on a conclusion.",
            ),
        ],
    },
    {
        "difficulty": "hard",
        "pid": "006",
        "split": "test",
        "topic": "pour-over coffee",
        "turns": [
            (
                "jules",
                "I ground the beans too fine again and the water just sat there like it was sulking.",
            ),
            (
                "jules",
                "I poked it. That's not in the instructions, I checked later.",
            ),
            (
                "jules",
                "It still woke me up, so I'm calling the experiment a messy success.",
            ),
            ("hale", "Grind was stepped two marks coarser. Drawdown then completed at 2:48."),
            ("hale", "Dose remained 15.0 g. Water remained 250 g."),
            (
                "nell",
                "Coarser, the bed opened like wet sand after a wave and the kettle's thin stream finally had somewhere to go.",
            ),
            (
                "nell",
                "The cup came back from the brink of mud and tasted, briefly, of citrus peel and patience.",
            ),
        ],
    },
    {
        "difficulty": "hard",
        "pid": "007",
        "split": "train",
        "topic": "pour-over coffee",
        "turns": [
            (
                "nell",
                "Dawn was only a rumour in the courtyard when the first pour found the dark grounds.",
            ),
            (
                "nell",
                "Steam lifted and unwrote itself against the window; a spoon waited like a quiet oar.",
            ),
            (
                "jules",
                "I'm not awake enough for poetry about coffee, I just want the mug to exist.",
            ),
            (
                "jules",
                "If it's too hot I do the inelegant sip and regret it, that's the whole method.",
            ),
            (
                "mira",
                "Waiting for a slightly lower serving temperature is a relatively cheap way to taste more than heat, although it is easily skipped.",
            ),
            (
                "mira",
                "The present habit, if one can call it that, is to let the mug stand while a kettle is refilled for later tea.",
            ),
            (
                "mira",
                "No claim is made that this improves extraction; it merely reduces the likelihood of an uninformative first sip.",
            ),
        ],
    },
    {
        "difficulty": "hard",
        "pid": "008",
        "split": "test",
        "topic": "pour-over coffee — Mira / Nell / Mira",
        "turns": [
            (
                "mira",
                "Resting roasted coffee for a few days is often said to tame carbon dioxide, although the useful window appears relatively roast-dependent.",
            ),
            (
                "mira",
                "A very fresh bag may bloom dramatically without therefore guaranteeing a preferable cup.",
            ),
            (
                "mira",
                "These kitchen notes treat rest as a controllable nuisance rather than as a moral stance about freshness.",
            ),
            (
                "nell",
                "The bag, opened, smelled like warm cedar and a sweeter smoke that would not name itself.",
            ),
            (
                "nell",
                "I counted no days; I counted the way the bloom lifted and then remembered gravity.",
            ),
            (
                "nell",
                "Freshness, in that kitchen, was simply the hour I happened to be kind to the kettle.",
            ),
            (
                "mira",
                "If a reader wants a number, a three-to-ten-day rest is a commonly repeated heuristic, not a result of this page.",
            ),
            (
                "mira",
                "The more cautious close is that bloom height and taste drifted together only loosely in these few mugs.",
            ),
        ],
    },
]


def changes_from_authors(authors: list[str]) -> list[int]:
    return [0 if left == right else 1 for left, right in zip(authors, authors[1:])]


def write_problem(entry: dict) -> dict:
    difficulty = entry["difficulty"]
    pid = entry["pid"]
    folder = OUT / difficulty
    folder.mkdir(parents=True, exist_ok=True)
    authors = [author for author, _ in entry["turns"]]
    sentences = [sentence for _, sentence in entry["turns"]]
    problem_path = folder / f"problem-{pid}.txt"
    truth_path = folder / f"truth-problem-{pid}.json"
    problem_path.write_text("\n".join(sentences) + "\n", encoding="utf-8", newline="\n")
    payload = {
        "authors": len(set(authors)),
        "changes": changes_from_authors(authors),
        "author_ids": authors,
        "difficulty": difficulty,
        "split": entry["split"],
        "topic": entry["topic"],
        "n_sentences": len(sentences),
    }
    truth_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {
        "key": f"{difficulty}/problem-{pid}.txt",
        "split": entry["split"],
        "difficulty": difficulty,
        "topic": entry["topic"],
        "authors": payload["authors"],
        "n_sentences": len(sentences),
        "n_changes": int(sum(payload["changes"])),
        "change_rate": round(sum(payload["changes"]) / max(1, len(payload["changes"])), 3),
    }


def main() -> int:
    manifest_problems = {}
    summary = []
    for entry in CORPUS:
        row = write_problem(entry)
        manifest_problems[row["key"]] = row
        summary.append(row)
    manifest = {
        "title": "Original synthetic style-change study set",
        "license": "MIT, texts original to this repository",
        "problems": manifest_problems,
        "counts": {
            "documents": len(summary),
            "by_difficulty": {
                name: sum(1 for row in summary if row["difficulty"] == name)
                for name in ("easy", "medium", "hard")
            },
            "by_split": {
                name: sum(1 for row in summary if row["split"] == name)
                for name in ("train", "val", "test")
            },
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(summary)} problems under {OUT}")
    for row in summary:
        print(
            f"  {row['key']:28} {row['split']:5} "
            f"sents={row['n_sentences']:2} changes={row['n_changes']} rate={row['change_rate']:.2f}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
