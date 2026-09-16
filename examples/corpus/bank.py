"""Original exam-bank prose. Running this file writes the .txt and truth JSON."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Document:
    stem: str
    title: str
    band: str
    note: str
    paragraphs: list[str]
    authors: list[str]

    @property
    def file(self) -> str:
        return f"{self.stem}.txt"

    @property
    def changes(self) -> list[int]:
        return [0 if left == right else 1 for left, right in zip(self.authors, self.authors[1:])]


def _join(paragraphs: list[str]) -> str:
    return "\n\n".join(paragraph.strip() for paragraph in paragraphs) + "\n"


DOCUMENTS: list[Document] = [
    Document(
        stem="problem-01-press-then-notice",
        title="Letterpress diary, then a noise ordinance",
        band="easy",
        note="Register and topic both jump after paragraph 2.",
        authors=["press", "press", "notice", "notice"],
        paragraphs=[
            "I locked the forme before dawn because the night had left a damp in the stone, and I would rather fight the paper than fight a warped chase. The quoins take a quarter turn past snug; any more and the furniture begins to climb, and then the impression walks toward the gripper. One must feel the give in the tympan rather than trust the numbered marks on the press bar. I have found that a sheet of newsprint under the tympan cloth will forgive a slightly proud rule, provided the frisket is cut honestly and the ink is not already skinning in the fountain.",
            "The job was a wedding invitation in 14-point Caslon, and the bride had asked for a second colour that I did not want to print wet. I let the black rest overnight and came back to the red with a harder packing and a lighter roll. The first dozen sheets kissed too faintly at the descenders; I added a tissue at the head and took them again. There is a moment, after the third correction, when the sheet looks as if it had always been that way. I keep those overs in a drawer marked with the date, because the next time someone asks how long a make-ready takes I would rather show the pile than invent a number.",
            "Members of the public are advised that, pursuant to Ordinance 14-7B, overnight operation of letterpress or other impact printing equipment is prohibited between the hours of 22:00 and 07:00. Complaints shall be lodged with the municipal clerk in writing. The department of environmental health shall inspect any premises named in two or more complaints within twenty-eight days. Failure to produce a current operating permit may result in a fine not exceeding four thousand kroner and an order to cease work until such permit is obtained.",
            "Premises used for small-scale printing shall maintain a log of press hours, ink types, and solvent disposal. The log shall be available for inspection without prior notice. Wash-up rags impregnated with petroleum distillates shall be stored in a closed metal container. Discharge of fountain waste into the municipal drain is not permitted. A copy of this notice shall be displayed at the principal entrance of any workshop to which it applies.",
        ],
    ),
    Document(
        stem="problem-02-bees-then-claim",
        title="Hive inspection, then an insurance claim",
        band="easy",
        note="Field first-person versus policy English.",
        authors=["field", "field", "claim", "claim"],
        paragraphs=[
            "The upper super was heavier than I wanted to lift with one hand, so I set the hive tool and waited for the foragers to settle. Brood pattern on the third frame was tight, a good sign after the cold snap, though I found two cells of chalkbrood on the sunny side. Smoke was kept thin; these bees punish a heavy puff by bearding under the lid. I marked the queen with a dot that will last the season if I do not knock her on the next inspection. The landing board still held a scatter of chewed cappings from yesterday's harvest.",
            "I walked the row before opening the next box because a tipped hive tells you more than a frame count. The third stand had a lean toward the ditch, and the entrance reducer had been chewed out. I packed a stone under the rear rail and smoked the hole until the guard bees came back to the porch. Stores looked even: sealed honey on the shoulders, pollen in a bright orange band, a palm of empty comb where I will put the next super if the flow holds. I wrote the notes on the lid in pencil so rain can take them if it must.",
            "The insured hereby reports a loss occurring on 12 May at the apiary located at Plot 6. Policy number AP-4419-C is current through 31 December. The claimed items comprise four destroyed supers, one cracked inner cover, and an estimated twelve kilograms of spoiled honey. The insured states that a vehicle left the lane and struck the stand. Photographs of the scene and of the damaged equipment are attached. Settlement is requested in accordance with schedule B of the policy.",
            "All items listed have been used solely for apiculture on the named premises. No prior claim has been filed against this policy. The insured undertakes to retain the damaged frames for inspection for a period of thirty days. Correspondence shall be directed to the address on file. Interest is not claimed except as provided under clause 9.2.",
        ],
    ),
    Document(
        stem="problem-03-funicular-then-complaint",
        title="Funicular night log, then a passenger complaint",
        band="easy",
        note="Operations log versus first-person complaint.",
        authors=["log", "log", "complaint", "complaint"],
        paragraphs=[
            "Car B was taken out of service at 21:10 after the lower sheave showed a heat mark on the outboard bearing. I locked the cabin at the mid-station, posted the barrier, and telephoned the duty engineer. Counterweight travel was within the painted marks; the haul rope had no visible broken wires in the inspection window. Wind on the ridge was 11 m/s gusting 16. I logged a reduced timetable for the remaining hour and kept Car A on a ten-minute headway. Passengers waiting at the lower hall were told the last trip would be 22:20.",
            "At 22:04 the ridge anemometer tripped the interlock for twelve seconds and then cleared. I held Car A at the upper landing until the needle stayed below the cut-out for a full minute. The cabin took the grade without slip. I walked the platform after the last passenger, checked both gates, and signed the book. Spare gloves and a torch were left on the hook for the morning shift. The heater in the lower hall was left on low because the tiles hold the cold.",
            "I want a refund for Tuesday night. We stood in that hall for forty minutes and nobody said the other car was broken until I asked twice. My kid was cold and the heater was basically off. Then you ran one car and packed us in like it was fine. The ticket said last trip 22:40 and we got pushed onto a 22:20 that felt rushed. I'm not trying to be dramatic. I just want the fare back and maybe a note that you tell people when a car is out.",
            "Also the barrier at the mid-station was half open so people kept walking toward a cabin that wasn't running. That's how you get someone on the track. I work mornings and I don't have time to file a long thing but I will if this is the reply I get. Email is fine. Don't call after eight.",
        ],
    ),
    Document(
        stem="problem-04-darkroom-then-invoice",
        title="Darkroom notes, then a gallery invoice",
        band="easy",
        note="Craft process versus billing English.",
        authors=["darkroom", "darkroom", "invoice", "invoice"],
        paragraphs=[
            "I mixed a fresh two litres of D-76 at 1+1 and let it stand until the bubbles left the graduate. The first sheet of HP5 was rated at 400 and I pulled it fifteen seconds because the street lamps had already done half the work. Developer at 20.1, stop in a quick bath, fixer for five and a wash that I timed with the tap I trust rather than the timer I do not. The highlights on the tram window held. I hung the roll on the left line, away from the heater, and wiped the clips so they would not drip into the next reel.",
            "The 8x10 of the harbour wall needed a two-stop burn at the sky and a breath of dodge on the ladder. I cut a card with a torn edge so the blend would not look like a lid. Paper was grade 3, selenium after the wash, two minutes until the black of the wet brick shifted. I still throw the first test strip away; it is a superstition and also a way of not talking myself into a bad print. The good one went into the blotter with a sheet of baking parchment because I was out of interleaving tissue.",
            "Invoice 1184 dated 18 June. As agreed, three silver-gelatin prints, 8x10, selenium toned, mounted on 11x14 board, at 900 kr each. One additional contact sheet at 250 kr. Delivery to the gallery on Tuesday as arranged. Payment is due within fourteen days of the invoice date. Bank details as previously supplied. Please quote the invoice number on the transfer.",
            "A late fee of 1.5 percent per month applies to balances unpaid after the due date. Title to the prints remains with the photographer until payment clears. The gallery may exhibit the work for the agreed run and shall not reproduce it without a separate licence. Please retain this invoice for your records.",
        ],
    ),
    Document(
        stem="problem-05-smokehouse-then-menu",
        title="Smokehouse log, then menu copy",
        band="easy",
        note="Process log versus fragmentary restaurant copy.",
        authors=["smoke", "smoke", "menu", "menu"],
        paragraphs=[
            "I lit the fire at four with last week's oak and a handful of apple that still smelled of the crate. The chamber was 18 degrees when I hung the mackerel; I want a slow climb to 75 over four hours, not a panic. Vents half open on the weather side. I turned the racks at ninety minutes because the left rail always runs hotter. The skins had taken a dull gold and the eyes were milky, which is when I stop poking them. I wrote the batch number on the slate and left the door alone.",
            "The pork belly from Thursday still had a soft patch at the thick end, so I gave it another two hours at 70 and a last half hour with the vents shut to set the bark. Internal at the bone was 68. I cooled it in the cage, not the walk-in, because condensation on a warm surface is how you dull a smoke line. Salt in this batch was 2.4 percent by green weight. I will cut it tomorrow and keep the end piece for staff, since the end piece is where I learn whether the cure moved.",
            "Smoked mackerel. Oak and apple. Horseradish cream. Rye crumbs. A lemon that has seen the coals. Pickled cucumber, thin.",
            "Pork belly, four days in the cage. Mustard seed. Wilted greens from the frost cloth. A sauce that is mostly the dripping and a little cider vinegar. Bread if you ask. Butter if you do not.",
        ],
    ),
    Document(
        stem="problem-06-planetarium-then-procurement",
        title="Planetarium script, then a procurement email",
        band="easy",
        note="Spoken public science versus office procurement.",
        authors=["script", "script", "procure", "procure"],
        paragraphs=[
            "Look up. Not at the painted dome — at the idea of a sky that is still moving while we sit still. The star that sits just above the winter tree on your street is not nailed there. It is sliding, very slowly, and the slide has a name we will use in a minute. For now I want you to hold one fact: the light arriving in your eye tonight left some of these stars before anyone in this room was born. That is not poetry. That is a distance dressed as a delay.",
            "We are going to dim the house lights and I will ask you not to take out a phone. The dome will show the sky as it is over this city at 22:00, clouds omitted because clouds are honest and also unhelpful. I will point out the ecliptic, then the plane of the galaxy, then one satellite that is not a star. If a child asks whether we can hear the satellite, the answer is no, and the better answer is that we can hear the engineers who keep it talking. We will get to that.",
            "Dear colleagues, please find attached the quotation for a replacement fisheye projector lamp, part number PL-9X, together with the service visit required to seat it. Kindly confirm that cost centre 441 may be charged. Lead time is quoted as five weeks. I should be grateful if the requisition could be raised before Thursday so that we do not lose the June slot. A second quote is attached for completeness.",
            "Please note that the vendor will not attend site unless a purchase order is visible in their portal. I have asked facilities to confirm dome access on the proposed morning. If the date is unsuitable, a reply by return would be appreciated. Best regards.",
        ],
    ),
    Document(
        stem="problem-07-thatcher-then-insurance",
        title="Thatching notes, then a roof insurance letter",
        band="medium",
        note="Same roof, two houses: craft versus insurer.",
        authors=["thatch", "thatch", "insurance", "insurance"],
        paragraphs=[
            "I started at the eaves because a rushed ridge is how you inherit a leak. The reed this year is shorter in the butt than I like, so I packed the first course tighter and pinned it with spars I split in the yard rather than the bought ones that twist. The old coat still had a sound shoulder on the north face; I combed it back and let the new work sit on it instead of stripping to the battens. Wind was off the marsh and the ladder needed a second tie. I keep a tally of bundles on the inside of the van door so I do not invent a number at the end of the day.",
            "The chimney flashing was tired where the previous coat had shrunk away from the lead. I lifted the apron, dressed a new piece, and tucked the reed under it so water has to work to get in. Spar ends I twisted toward the prevailing weather. A child from the lane asked if the roof was made of hair; I said yes, in a way, and then I said no, because that is how rumours start. I will ridge it tomorrow if the sky holds. The liggers are already soaking in the trough.",
            "We refer to policy HR-2201 and to the claim submitted on 3 April in respect of storm damage to the thatched roof at Lark Cottage. Our assessor attended on 9 April. The report finds that the north face had reached the end of its serviceable life and that the storm was an aggravating rather than a primary cause. Cover under section 4 is therefore limited to the ridge and the chimney apron. A payment of 18,400 kr is offered in full and final settlement of this head of claim.",
            "If the insured does not accept the offer within twenty-one days, the file will be reviewed by a second assessor. Alternative quotes obtained by the insured may be submitted but shall not bind the insurer. Please note that a thatched risk requires a current spark-arrestor certificate; this was not present in the file and must be supplied before any payment is released.",
        ],
    ),
    Document(
        stem="problem-08-tesserae-then-conservation",
        title="Mosaic inventory, then a conservation report",
        band="medium",
        note="Workshop inventory versus conservation-speak, same object.",
        authors=["mosaic", "mosaic", "conserve", "conserve"],
        paragraphs=[
            "I counted the remaining smalti by colour family because the last job ate the cobalt and I will not start a border I cannot finish. Blue in the left tin: 420 pieces, mostly 8 mm, a few 12 mm I have been saving for the water. Gold leaf on glass: 80, and three of those are scratched so they will go to the sky where a scratch reads as weather. I keep the whites in a cloth bag, not a tin, because they chip when they rattle. The cartoon is pinned to the board with the north edge marked so I do not lay the river upside down again.",
            "Yesterday I cut a run of terracotta for the path and the nippers left a burr I had to stone down. I set a metre of andamento before lunch, following the line of the old tesserae rather than fighting them. Where the bed had hollowed I injected a thin grout and waited. The work is slow on purpose. A mosaic that looks hurried from a metre away will look dishonest from the door.",
            "Condition report, pavement mosaic, north aisle, 14 June. The surface exhibits isolated loss of tesserae along a 1.2 m band parallel to the step, with associated powdering of the lime bedding. In situ consolidation with a reversible acrylic emulsion is recommended prior to any infill. Cleaning should be limited to aqueous methods; no chelating agents on the gold-glass. A fill using modern smalti, slightly recessed, will remain distinguishable under raking light.",
            "Intervention shall follow the principle of reversibility and of minimal loss of original material. Sampling of the bedding for binder analysis is proposed at two locations already damaged. Photography before, during, and after is required. The work is estimated at eight studio days plus two days on site. A full treatment proposal will follow this report.",
        ],
    ),
    Document(
        stem="problem-09-ropewalk-then-bulletin",
        title="Ropewalk diary, then a safety bulletin",
        band="medium",
        note="Craft diary versus mandatory safety voice.",
        authors=["rope", "rope", "bulletin", "bulletin"],
        paragraphs=[
            "The hemp came in damp from the barge, so I hung the bundles in the long loft and left the doors cracked. You cannot spin a fair yarn from a wet fibre and then pretend the lay will hold in January. I walked the jack the length of the walk twice before I trusted the hooks; one of them has a habit of dropping a half-turn when the floorboard lifts. The first strand I made today was for a 24 mm hawser, three-strand, a right-hand lay, the kind the harbour still asks for because the new synthetics slip on wet timber.",
            "I keep the tar kettle at a temperature I can hold my hand near but not on. Too hot and the fibre goes brittle; too cool and the coat sits on the surface and flakes. The boy from the next yard asked why we still smell like a ship. I told him that a smell is a record of oil meeting dust, and that the record is older than the crane they put on the quay. I tagged the finished coil with the date and the number of yarns. I do not trust a coil that cannot tell you how it was made.",
            "SAFETY BULLETIN 09 / ROPEWALK AND FIBRE LOFTS. All personnel MUST wear close-fitting clothing when working near rotating hooks or jacks. Loose scarves are prohibited. Hair that reaches the collar MUST be tied. A second person MUST be present whenever the walk is under power. Emergency stop lanyards shall be tested at the start of each shift and the test recorded in the book.",
            "Tar kettles shall not be left unattended. A charged extinguisher of the correct class MUST be within three metres. Spills shall be covered with sand, not water. Visitors are not permitted on the walk during spinning. Failure to follow this bulletin will be treated as a disciplinary matter. Read it. Sign the sheet. Put it back on the nail.",
        ],
    ),
    Document(
        stem="problem-10-cheese-then-copy",
        title="Cheese-cave log, then marketing copy",
        band="medium",
        note="Aging notes versus promotional second person.",
        authors=["cave", "cave", "copy", "copy"],
        paragraphs=[
            "Rack 4, wheel 11, day 47. The rind has taken a thin white that I like, not the felt that means I have been too kind with the humidity. I turned it and wiped a brine that was just under saturation. The cave sat at 11.2 degrees and 93 percent; I cracked the door for twenty minutes after I left because the last storm pushed the moisture up. A smell of cellar, not of ammonia. If ammonia shows I will move this wheel to the drier alcove and stop talking about it as if it were a plan.",
            "I tasted a plug from wheel 8. The paste has begun to shine at the edges and the salt has evened. Not ready. I wrote 'wait' on the slate and did not add a date, because a date on a slate becomes a dare. The younger wheels I did not touch. Curiosity is how you make a cave of opened faces. I replaced the plug and smeared the rind so the hole would not become a story.",
            "Discover a cave that does the waiting for you. Our wheels sit in the dark until the paste turns silk and the rind learns the stone. You bring bread. You bring a knife if you must. You leave with a wedge that remembers the weather of a particular week. Limited wheels this month. Taste at the counter. Take some home before we talk ourselves out of selling it.",
            "Meet the affineur. Or don't — the cave is the one doing the work. Subscribe to the note we send when a batch is ready, not when a calendar says so. Gift a whole wheel if you have a table that can stand the attention. We will pack it as if it were going further than the next street.",
        ],
    ),
    Document(
        stem="problem-11-wind-tunnel-then-blog",
        title="Wind-tunnel notes, then a popular-science blog",
        band="medium",
        note="Lab notes versus blog second-person energy.",
        authors=["lab", "lab", "blog", "blog"],
        paragraphs=[
            "Run 17. Model 4B, 1:24, trip dots at 5 percent chord. Tunnel speed 28.4 m/s, Reynolds on the reference chord 1.8e5. Balance zeroed after a five-minute soak. I discarded the first twenty seconds because the model still rang from the last yaw. Lift coefficient tracked the previous polar within 0.01 until twelve degrees, then the left tufts lifted and the moment arm wandered. I logged a note to check the port sting clamp; the last torque stripe looks tired.",
            "Oil flow on the upper surface showed a bubble that sat too far forward compared with the CFD I do not entirely trust. I photographed it under the raking LED and wiped the model before the oil skinned. Temperature in the circuit rose 0.6 degrees over the hour. I will not compare this polar to Tuesday's until I have the same oil batch and the same ambient. The notebook has a square where I write the things I almost fudged. It is empty today, which I like.",
            "Here's the thing about a wind tunnel: it is a lie we tell a model so the sky will later tell us the truth. You put a little wing in a tube, you blow air at it, and you pretend the tube is the whole world. It isn't. The walls are there. The sting is there. The Reynolds number is usually wrong. And still — if you are honest about the lies — the numbers start to mean something. That's the part the press release skips.",
            "You might ask why anyone still uses tufts of yarn in the age of pretty simulations. Because yarn does not care what you hoped the flow would do. It lifts, or it doesn't. I like instruments that can embarrass me. If you ever get a chance to stand behind the glass and watch a stall walk in from the tip, take it. There is no slide deck that replaces that particular kind of bad news.",
        ],
    ),
    Document(
        stem="problem-12-puppet-then-program",
        title="Marionette rigging notes, then a festival program",
        band="medium",
        note="Workshop first person versus festival present tense.",
        authors=["puppet", "puppet", "program", "program"],
        paragraphs=[
            "I re-strung the left shoulder because the old linen had glazed and the joint had started to hitch on the downbeat. The new line is waxed, a little longer than I first cut, because a tight string makes a proud puppet and a proud puppet cannot bow. I hung him from the rehearsal hook and walked the controls until the head arrived after the hand, which is the order I want. The painted eye still looks too awake; I will dull it before the hall lights hit the varnish.",
            "The bridge scene needs the second controller. I marked the floor with chalk so I do not cross the other operator's lines. We ran it four times and on the fourth the puppet sat without being told, which is either skill or a loose hip. I tightened the hip. I do not romanticise a loose joint. After rehearsal I coiled the controls in the figure-eight I was taught and hung them so the bars cannot knock. Tomorrow I will sew the tear in the cloak that only shows when he turns upstage.",
            "The Night Market opens at dusk with a procession of marionettes from the upper square to the hall. Follow the paper lanterns. Seating is unreserved; cushions may be hired at the door. Tonight's bill: The Baker's Shadow, a piece for two operators and a loaf that refuses to rise, followed by a short work for children in which the moon misbehaves. Latecomers will be held at the curtain until a blackout.",
            "Workshops on Saturday morning teach a simple control bar. No experience is assumed. Please wear shoes you can stand in. The evening performance is the same bill as Friday with one added scene. Tickets from the booth or from the website if the booth has already decided it is tired.",
        ],
    ),
]


def _more() -> list[Document]:
    """Second half kept as a function so the file stays editable in parts."""
    return [
        Document(
            stem="problem-13-two-pewtersmiths",
            title="Two pewtersmiths on the same tankard",
            band="hard",
            note="Same topic. A is periodic and reflective; B is clipped bench talk.",
            authors=["pewter_a", "pewter_a", "pewter_b", "pewter_b"],
            paragraphs=[
                "I turned the tankard on a stake that still carries the dent of my teacher's wrist, and I thought, as I always do at this point in a job, that the metal remembers more hands than it will admit. The body wanted to go oval when I planished the lower third; I let it go a little and then brought it back with a softer hammer, because pewter punished with steel will show the punishment in the highlight. One must listen for the change in pitch when the wall thins. I have found that a cloth between the stake and the work will hide a bruise that the customer will later call character.",
                "The handle I cast from a mould I do not love, and then I spent an hour making it look as if I had never used a mould. The solder line at the upper join is where a tankard tells the truth. I filed it until the light ran without a step, then I stopped, because a perfect lie is also a kind of noise. The inside I left slightly dull. A mirror finish in a drinking vessel is a boast, and I am not in the mood to boast for a stranger.",
                "Body still going oval. Hit it softer. Stake has that old dent, don't fight it. Wall pitch dropped on the lower third so I quit thinning. Cloth on the stake hid the bruise. Handle out of the mould I always complain about. Filed the upper join till the light stopped catching. Inside dull on purpose. If they want a mirror they can buy a different shop's work.",
                "Lid fit was tight on the right ear. Tapped the hinge pin, peened it, checked the drop. Thumbpiece sits a hair back; I'll live with it. Flux wiped, heat kept short, no pits. Stamped my mark under the base and the date. Put it on the shelf with the mouth covered so dust doesn't write on the inside. Job's done unless they come back about the oval, which they will.",
            ],
        ),
        Document(
            stem="problem-14-two-typesetters",
            title="Two typesetters on the same invitation",
            band="hard",
            note="Same job. A is hot-metal diary; B is modern production chat.",
            authors=["type_a", "type_a", "type_b", "type_b"],
            paragraphs=[
                "I set the names in Caslon because the pair had asked for something that looked as if a person had stood at a case. The ampersand I swapped twice; the first one was too clever and the second one sat in the line like a person who belongs there. Spacing after the comma in the date was the fight of the morning. I do not trust a digital proof to tell me whether a comma is lonely. I locked a galley, pulled a repro, and held it at arm's length in the window. The window is a better critic than I am before coffee.",
                "Ornaments I used sparingly. One rule above the names, hairline, and a second rule only if the paper can take the bite. I cut the frisket so the rule would not crush the deckle. There is a temptation, when a couple has paid for letterpress, to give them every flower in the case. I resist it. The job should look like a decision, not like a catalogue of what I own.",
                "ok so caslon for the names, they wanted that human-case look. ampersand v2 is fine, v1 was trying too hard. comma after the date still feels hungry but i'll live if the window test says so. locking up now, will shoot a phone proof because nobody waits for a wet repro anymore. if the couple slack me again about flowers i'm gonna say no in a nice way.",
                "frisket cut, rule is hairline only, second rule maybe if the deckle survives. i'm not dumping ornaments on this just because it's letterpress. export the pdf for their uncle anyway, he'll print it on a laser and that's not my problem. packing the chase, back in 20.",
            ],
        ),
        Document(
            stem="problem-15-two-thatchers",
            title="Two thatchers on the same ridge",
            band="hard",
            note="Same roof. A writes in long clauses; B writes in short site notes.",
            authors=["thatch_a", "thatch_a", "thatch_b", "thatch_b"],
            paragraphs=[
                "I set the ridge in wheat because the house sits in a wind that punishes reed at the crest, and I have learned, slowly, that a pretty ridge which fails in the second winter is a kind of theft. The liggers I soaked until they would bend without a white line. Each spar I twisted toward the weather so that a lifted end will still shed. A neighbour said it looked like sewing. I said it was sewing, and that the thread was older than the street. I packed the roll tighter than the last job because this one faces the marsh.",
                "At the chimney I let the reed climb a little higher than the lead so the water has a longer argument. I do not like a bald flashing. I stood back from the lane, which is the only view that matters, and I took a photograph I will not post, because a photograph of a half-finished ridge is how you get advice from people who have never climbed the ladder. I will dress the ends in the morning if the frost stays off the spars.",
                "Wheat ridge, not reed — wind off the marsh eats reed here. Liggers soaked, no white line when they bend. Spars twisted to weather. Packed the roll tighter than Lark Cottage. Chimney: reed a bit proud of the lead. Looked from the lane, not from the scaffold. Photo for me, not for the group chat. Ends tomorrow if it doesn't frost.",
                "Used 11 bundles on the ridge, 2 left in the van. Ladder ties checked after lunch because the ground is soft. Kid asked if it's hair again. I said reed and wheat and left it. Tools under the tarp. If the owner texts about the colour, tell them it will weather in.",
            ],
        ),
        Document(
            stem="problem-16-two-lantern-makers",
            title="Two lantern-makers on the same commission",
            band="hard",
            note="Same object. A is essayistic; B is a shop list with asides.",
            authors=["lantern_a", "lantern_a", "lantern_b", "lantern_b"],
            paragraphs=[
                "I cut the mica a little larger than the opening and then I dressed it back, because a pane that is born the right size will rattle in February. The tin I tinned again even though it already wore a coat; a second coat is cheaper than a complaint. The hinge I made from a strip I had saved for a smaller job, and I almost regretted the generosity until the door sat true. A lantern is a box that must lose as little wind as possible and still be opened by a cold hand. I keep that sentence on a card above the bench.",
                "The glass of the old commission had clouded from a fuel I no longer sell. I showed the owner the haze and offered mica, which will not cloud and will not give the same glitter. They chose mica. I was glad. I punched the vents in a pattern I have used since I was taught, not because I lack imagination, but because that pattern keeps a flame in a doorway. Imagination is for the piercing that nobody needs.",
                "Mica oversized, dressed back, won't rattle. Retinned the tin, yes again. Hinge from the scrap strip, door sits true. Vents in the old pattern — don't get clever, the clever pattern blew out last year. Owner picked mica over cloudy glass, good. Fuel note on the invoice so they don't run the wrong stuff. Wire handle, leather wrap, two rivets not one.",
                "Pierced a small star because they asked. One star. If I start a sky I'll still be here on Sunday. Solder looks clean, no peaks. Tested with a candle in the yard, flame held at the door. Packed with paper, not foam, foam sweats on mica. Bench swept. Next job is the hall pair.",
            ],
        ),
        Document(
            stem="problem-17-two-tram-drivers",
            title="Two tram drivers on the same diversion",
            band="hard",
            note="Same shift event. A is full sentences; B is radio-short.",
            authors=["tram_a", "tram_a", "tram_b", "tram_b"],
            paragraphs=[
                "I took the diversion at the bridge because the radio said the square was still blocked, and I told the car as if the car were a person who deserved the reason. Two stops would be missed. I repeated the next stop twice, once for the people standing and once for the people who only look up when the doors open. A man asked if his ticket was still good on the bus; I said yes, and I said it slowly, because a yes that is rushed sounds like a no. The points were sticky and I took them on a crawl.",
                "At the depot end I wrote the delay in the book and I added the thing the form does not ask for: that the square smelled of a burnt clutch and that the police tape was already slack, which meant we would be back on the old line before the evening peak if someone cut it. I do not like leaving a guess in a book, so I wrote 'slack tape, likely clear by 16:00' and signed it. Then I washed my hands, because the handrail on that unit is always a little oily.",
                "Diversion at the bridge, square still blocked. Missed two stops, called it twice. Ticket-to-bus question, said yes slow. Points sticky, crawled them. Radio knew. No argument from the car, one argument from a tourist, let it go.",
                "Booked the delay. Wrote slack tape, maybe clear by 16. Not a guess I love but better than nothing. Handrail oily again, washed up. Unit stays in unless they swap it. I'm on the 15:10 if the square opens. If not, same diversion, same two missed stops.",
            ],
        ),
        Document(
            stem="problem-18-two-cave-agers",
            title="Two affineurs on the same wheel",
            band="hard",
            note="Same cave. A is unhurried prose; B is slate-talk.",
            authors=["cave_a", "cave_a", "cave_b", "cave_b"],
            paragraphs=[
                "I have been turning this wheel longer than the calendar suggests, because the calendar does not taste. The rind had begun to tighten on the side that faces the door, and I moved it one place deeper so the draught would have to work. I do not rush a paste that is still shy of silk. There is a week, in every good wheel, when doing nothing is the skill. I wrote nothing on the slate except the number, which is a way of refusing a story.",
                "A visitor asked whether we 'add flavour'. I said we add time and a room that does not change its mind. I offered a plug from a neighbour wheel, not this one. This one is not a demonstration. After they left I sat with the door closed until the humidity came back to the number I trust. The cave is a conversation with stone. I would rather lose a sale than raise my voice in it.",
                "Wheel 11 still shy. Moved it off the door draught. No slate story, just the number. Didn't plug it. Visitor got a taste from 7 instead. Humidity back after they left. Don't open the door for a photo. If they ask again, same answer: time and a room.",
                "Brine wipe on 11, light. 93 percent, 11.1 degrees. Ammonia not invited. 8 can wait, shine at the edge isn't ready. I'm not cutting a face to satisfy a tour. Rack 4 stays as is. Out.",
            ],
        ),
        Document(
            stem="problem-19-press-three-topics",
            title="One compositor, three subjects",
            band="trap",
            note="Same press voice on ink, rent, and a bicycle. Must not fire.",
            authors=["press", "press", "press", "press"],
            paragraphs=[
                "I have been thinking about the ink I bought in March, which skins if I leave the fountain uncovered for an hour, and which, when it is honest, prints a black that does not try to be a photograph. One must stir it from the bottom. I have found that a small job will take more ink than the area suggests, because the rollers steal a share and do not give it back. I keep a note of the batch on the lid so that next March I do not invent a loyalty I do not feel.",
                "The rent letter arrived on a Tuesday, which is a day I dislike for letters. The figure is not impossible and it is not kind. I set it next to the press and looked at both, as if they might negotiate. They did not. I will print the invoices I have been avoiding and I will pay what I can in the first week. One must not let a landlord become the only person who writes in complete sentences in a workshop.",
                "My bicycle has a spoke that ticks when I lean left, and I have decided, after too many errands, that a tick is a sentence I can no longer ignore. I trued the wheel in the alley with the spoke key I keep in the apron pocket for no good reason. The rim still wanders a little. I have found that a wander is preferable to a buckle, and that a buckle is preferable to a bus. I rode home slowly, as if the street were a sheet I did not want to mark.",
                "Tomorrow I will wash the rollers and I will write a list that includes ink, rent, and the spoke, because a list is a way of admitting that three worries can share a hand. I do not expect the list to solve them. I expect it to keep them from pretending they are one worry. The press will be clean, the letter will still be on the bench, and the bicycle will tick only if I have lied to myself about the key.",
            ],
        ),
        Document(
            stem="problem-20-notice-three-topics",
            title="One clerk, three notices",
            band="trap",
            note="Same municipal voice on dogs, bins, and scaffolding.",
            authors=["notice", "notice", "notice", "notice"],
            paragraphs=[
                "Members of the public are advised that dogs shall be kept on a lead in the municipal park between 1 April and 30 September. The restriction applies to all paths and lawns. Exemptions may be granted in writing by the parks office for assistance dogs. Fixed-penalty notices shall be issued to persons who fail to comply. This notice is displayed pursuant to byelaw 9.",
                "Household waste shall be presented in closed bags in the designated containers. Collection will occur on Tuesdays except where a public holiday falls on a Monday, in which case collection shall occur on Wednesday. Side waste will not be taken. Contamination of the recycling stream may result in a missed collection and a written warning. Enquiries shall be directed to the waste desk.",
                "Scaffolding on the public highway requires a permit. Applications shall be submitted no fewer than ten working days before erection. Lights and warning signs shall be maintained from dusk until dawn. The pavement shall remain passable to a width of 1.2 metres unless a diversion has been approved. The permit shall be displayed on the outer standard.",
                "A copy of each of the above requirements is available from the civic office during advertised hours. Failure to comply may result in a fine as set out in the current schedule. This compilation is issued for convenience and does not replace the individual ordinances. The clerk's stamp appears below.",
            ],
        ),
        Document(
            stem="problem-21-chat-three-topics",
            title="One chatty voice, three subjects",
            band="trap",
            note="Same informal voice on lunch, a game, and a flat. Must not fire.",
            authors=["chat", "chat", "chat", "chat"],
            paragraphs=[
                "ok so lunch was a sad rice thing from the place by the bridge and i'm not doing that again. like it wasn't even hot. i told them and they were kinda whatever about it which, fine, but i'm still hungry and i've got a seminar at two. gonna grab a bun from the machine and pretend that's a plan. if you're in the building later i'll be the person eating a bun like it's a choice.",
                "also i finally finished that board game we started in march. the ending is kinda mean? not in a fun way, in a 'the designer wanted a thesis' way. i still liked the middle. would i play it again. maybe if someone else owns it and i don't have to punch the tokens. don't @ me about the expansion i already know.",
                "flat update: the tap still drips and the landlord still says he'll come 'this week' which is a season now. i put a bowl under it and i feel like a person in a comic. rent is due anyway. i'm not gonna start a war over a drip but i'm also not gonna pretend it's charming. if it stains the floor that's on him. idk. maybe i just need earplugs.",
                "anyway that's my whole brain: bun, mean game, drip. if we still on for thursday say something so i don't stand outside the wrong door again. i'll bring the extra tokens. i won't bring rice. see you or i won't, this chat is doing a lot of work for a person who is about to sit in a seminar and think about none of this.",
            ],
        ),
        Document(
            stem="problem-22-press-return",
            title="Compositor, clerk, compositor again",
            band="return",
            note="Author A returns. Two hinges, not three voices.",
            authors=["press", "press", "notice", "press"],
            paragraphs=[
                "I spent the morning on a card that should have been simple: a name, a date, a rule. The rule printed heavy on the left and I chased it with packing until the impression evened, which is a sentence I have written too many times and still mean. One must not hurry a rule. I have found that a hurried rule is the first thing a guest will notice, and the last thing a couple will forgive.",
                "The paper was a soft cotton that took the bite like a kindness. I held a sheet to the window and liked it enough to print the rest without another correction. That is rare and I do not trust rare things, so I printed six extras and put them under a board. If the couple asks for a reprint I will have something that still smells of the same ink.",
                "Persons operating a press in a mixed-use building shall ensure that vibration is not transmitted to adjoining dwellings between 20:00 and 08:00. Complaints shall be recorded by the clerk and forwarded to environmental health. Repeat complaints may result in a restriction of permitted hours. This notice is issued without prejudice to any existing licence.",
                "I read the notice on the stair and I set it on the imposing stone as if it were a proof I had not asked for. The hours it names are hours I already keep. Still, a notice is a kind of furniture: it takes space, it does not ink well, and it will be there in the morning. I locked up, washed the rollers, and left the extras under the board. Tomorrow I will print something that is not a notice, and I will try not to hear the stair in the tympan.",
            ],
        ),
        Document(
            stem="problem-23-four-voice-collage",
            title="Four houses in one file",
            band="collage",
            note="press, notice, chat, menu. Three hinges.",
            authors=["press", "notice", "chat", "menu"],
            paragraphs=[
                "I cut a frisket for a small mark that will sit in the corner of a title page, and I took more care with the knife than the mark deserves, because a careless hole is how you ink a margin you cannot later deny. The press was quiet. The stone was cold. I have found that a cold stone is honest about whether a forme is truly locked.",
                "A title page printed for commercial sale shall carry the name and address of the printer. Failure to identify the printer may result in the work being treated as unregistered. Copies shall be deposited as required by the relevant deposit scheme. Enquiries shall be directed to the clerk of publications.",
                "lol the title page thing is so small and they still sent a notice like i forged a passport. i'm gonna put the address on it, it's fine, i just wish they'd write like a person. anyway i'm heading out, wanna get noodles before the seminar? if the shop is closed i'll just eat a bun and be sad in a productive way.",
                "Noodles, evening. Broth that has seen a roast bone. Greens. A jammy egg if the pot allows. Chilli oil in a saucer, not in the bowl, so you can still taste the first idea. Sesame. Leave the last sip.",
            ],
        ),
        Document(
            stem="problem-24-gift-abstract",
            title="Student notes with a gifted abstract",
            band="trap",
            note="One formal paragraph inserted in a student voice. Mark only those hinges.",
            authors=["student", "student", "gift", "student"],
            paragraphs=[
                "I still get stuck on why we call this intrinsic. If I understand it, it means we don't get a pile of other texts by the same people — we only get the document and we have to argue from the inside. That feels unfair and also like the whole point. I wrote in the margin that style-change is what you do when you can't do authorship the usual way. Not sure that's how I should say it in the oral.",
                "For the easy PAN split I keep writing 'topic leak' and then I have to remember to say it politely. If the paragraphs jump from legal advice to world news, a bag of words will look like a genius. The hard split is same topic, different people, and that's where my little detector is supposed to be honest about failing. I want to say that out loud so I don't pretend the toy numbers are a paper.",
                "This paper presents a compression-based approach to intrinsic style-change detection. We estimate pairwise Normalized Compression Distance between adjacent paragraphs and combine it with a closed-class function-word profile. Experiments on a controlled corpus demonstrate that topic shift is a confounding factor and that macro-averaged F1 should be preferred to accuracy. Broader implications for multi-author analysis are discussed.",
                "That paragraph above is the kind of thing I would get if I asked a model to 'make it sound like a paper' and I need to be able to point at it in the oral. The sentences are even. Nobody is stuck. There is a 'we' that did experiments. I'm leaving it in the file as a gift-authorship toy: the hinge before and after should fire, and the student bits should stay together. If my detector eats the student bits too, that's a useful miss.",
            ],
        ),
        Document(
            stem="problem-25-exam-two-answers",
            title="Two exam answers on the same prompt",
            band="medium",
            note="Same question, two students. One hinge in the middle.",
            authors=["answer_a", "answer_a", "answer_b", "answer_b"],
            paragraphs=[
                "Style-change detection is intrinsic when the system cannot compare the disputed text to an external corpus of candidate authors. I would define a style change as a systematic shift in features that are more about how someone writes than about what they write: function words, punctuation habits, sentence length, maybe character n-grams. I would not treat a new named entity as proof of a new author, because a single author can change topic on purpose.",
                "If I had to pick a metric I would pick macro-F1 over accuracy. Most paragraph boundaries in a document are not changes, so a system that never fires looks accurate and is useless. I would also want to see a never-fire baseline on the same table so the number means something. For the oral I would add that hard documents, where topic is controlled, are the ones that tell you whether you measured style.",
                "ok definition first: intrinsic = no extra docs from the suspected writers, you only look inside the file. a style change is when the 'how' jumps. i care about function words and compression distance because they are less about nouns. if the nouns change and the habits don't, i don't call it a new author. that's the topic trap and i don't want to fall in it in the exam.",
                "metric: f1, and i'll say why accuracy is a trap if they let me. i'd show never-fire vs always-fire vs the actual system. if never-fire wins on accuracy i've made the point. for hard data i expect my thing to drop and i'll just say that instead of hiding it. also i'd mention gift authorship as a reason the task exists outside the shared task.",
            ],
        ),
        Document(
            stem="problem-26-minutes-letter-notice",
            title="Minutes, then a letter, then a notice",
            band="collage",
            note="Three civic registers in order.",
            authors=["minutes", "minutes", "letter", "notice"],
            paragraphs=[
                "The meeting opened at 18:32. Present: Holm, Vester, Khan. Apologies: Dahl. The minutes of 2 May were approved without amendment. Item 3, the funicular night service, was introduced by Holm. It was agreed that a written update would be requested from operations before the next meeting. Item 4, the noise complaint relating to the print workshop on Strandgade, was deferred pending a site visit. The meeting closed at 19:10.",
                "Under any other business, Vester asked whether the market stall licences would be reviewed before August. The chair said that a paper would be circulated. No vote was taken. The next meeting was set for 14 June in the usual room. Members were reminded to send papers three working days in advance.",
                "Dear neighbours, I am writing as the person who runs the small press on the ground floor. I heard the committee discussed our hours, and I would like to say, in ordinary sentences, that we already stop the motor before eight. If the vibration is travelling, I want to know, and I will pay for a better pad. I am not asking for a fight. I am asking for a measurement and a conversation that is not only a minute. Yours, M.",
                "Residents are advised that a vibration survey will be conducted at the Strandgade premises on 20 June between 09:00 and 12:00. Access shall be granted to the appointed contractor. A report will be circulated to the committee and to the occupier. This notice is issued for information and does not constitute a finding.",
            ],
        ),
        Document(
            stem="problem-27-solo-press",
            title="Single compositor, one job",
            band="control",
            note="All zeros. The never-fire baseline should look perfect here.",
            authors=["press", "press", "press", "press"],
            paragraphs=[
                "I spent an hour on the imprint line, which nobody reads and which I still treat as a place where a shop tells the truth. The type was worn in the counter of the 'e', and I almost let it go, and then I did not. One must not ship a worn 'e' on a page that claims to be careful. I have found that the jobs I regret are the ones where I decided that a stranger would not notice.",
                "The paper I chose is too soft for a long run and exactly right for this one. I damped it a little, which is an old habit and a way of asking the sheet to meet the type halfway. The first decent impression came on sheet fourteen. I kept sheets one through thirteen as a record of how long it takes me to stop fidgeting. The stack has a dog-ear I will not flatten; it is a date.",
                "Wash-up I did properly, even though it was only a black. The fountain had a skin I should have caught earlier. I scraped it, I reset the keys, and I told myself a story about being tired that I did not accept. Tomorrow's job is red, and red will show every lie I tell tonight. I left the rollers to rest and I wrote the hours on the card.",
                "I locked the door and I stood in the alley with the smell of solvent still on my hands, which is a smell I used to hate and now use as proof that the day happened. The bicycle ticked. I ignored it. There will be time to true a wheel when there is not a forme waiting. I have found that a shop is a set of postponements held together by a quoin.",
            ],
        ),
        Document(
            stem="problem-28-solo-bees",
            title="Single beekeeper, one inspection",
            band="control",
            note="All zeros. Same field voice the whole way.",
            authors=["field", "field", "field", "field"],
            paragraphs=[
                "I lit the smoker with a scrap of egg carton and a twist of dry grass, which is not elegant and is what works when the pellets have taken damp. The first hive was quiet in the way I like: a low sound, not a boil. I cracked the lid, waited, and lifted. The inner cover had propolis in a thick seam I was sorry to break. A few guards came up and I gave them a breath of smoke, not a punishment.",
                "Frame two had a queen cup I flattened because it was on the face, not the bottom, and I am not in the mood for a swarm this week. Stores were decent. Brood was even. I did not see her and I did not hunt until the last frame, which is when she usually turns up looking as if she had been busy with something more important than me. She was there, unmarked from last time, and I dotted her and felt the usual small relief.",
                "The second hive had a leaning stand I should have fixed in April. I packed a brick under it and told myself this was not neglect, which it was. Ants on the cover. I wiped them and I will put the stand in a water moat if I am a better person on Sunday. The colony was lighter. I gave them a frame of honey from the first hive and I wrote that down so I do not 'remember' it as a plan I only thought about.",
                "I closed up, scraped the tool, and sat on the box that is not a hive and is only a box. The field had that late light that makes the rape look louder than it is. I ate the apple I had put in the smoker pocket and then remembered why that is a bad place for an apple. The bees were already ignoring me, which is the goal. I will come back in eight days if the weather holds, and sooner if it does not.",
            ],
        ),
    ]


DOCUMENTS.extend(_more())


def manifest_payload() -> dict:
    return {
        "name": "quoin-personal-exam-bank",
        "description": "Original documents for a personal style-change exam lab. Not PAN data.",
        "documents": [
            {
                "file": doc.file,
                "stem": doc.stem,
                "title": doc.title,
                "band": doc.band,
                "note": doc.note,
                "n_paragraphs": len(doc.paragraphs),
                "n_changes": sum(doc.changes),
                "authors": doc.authors,
            }
            for doc in DOCUMENTS
        ],
    }


def emit(root: Path | None = None) -> None:
    root = root or HERE
    truth_dir = root / "truth"
    truth_dir.mkdir(parents=True, exist_ok=True)
    for doc in DOCUMENTS:
        (root / doc.file).write_text(_join(doc.paragraphs), encoding="utf-8")
        payload = {
            "changes": doc.changes,
            "authors": doc.authors,
            "band": doc.band,
            "title": doc.title,
            "note": doc.note,
        }
        (truth_dir / f"truth-{doc.stem}.json").write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )
    (root / "manifest.json").write_text(json.dumps(manifest_payload(), indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    del argv
    emit()
    print(f"wrote {len(DOCUMENTS)} documents under {HERE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
