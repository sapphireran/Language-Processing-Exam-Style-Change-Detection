"""Original toy documents. Nothing scraped, nothing shared-task, nothing workplace.

Each paragraph is written in one of six houses (see houses.md). Changes
are labelled at the paragraph hinge, PAN-style. Holdout ids are listed
in HOLDOUT so in-band F1 is not the same number as the revision score.
"""

from __future__ import annotations

from dataclasses import dataclass

HOLDOUT = frozenset({"04", "10", "15", "19", "23", "26", "28"})


@dataclass(frozen=True)
class Document:
    id: str
    band: str
    houses: tuple[str, ...]
    topics: tuple[str, ...]
    paragraphs: tuple[str, ...]
    changes: tuple[int, ...]
    note: str

    @property
    def slug(self) -> str:
        return self.id  # already slug-shaped, e.g. 01-caliper-stilling-control

    @property
    def code(self) -> str:
        return self.id.split("-", 1)[0]

    @property
    def holdout(self) -> bool:
        return self.code in HOLDOUT


def _d(
    id: str,
    band: str,
    houses: tuple[str, ...],
    topics: tuple[str, ...],
    paragraphs: tuple[str, ...],
    changes: tuple[int, ...],
    note: str,
) -> Document:
    if len(changes) != len(paragraphs) - 1:
        raise ValueError(f"{id}: {len(paragraphs)} paras, {len(changes)} hinges")
    return Document(id, band, houses, topics, paragraphs, changes, note)


DOCUMENTS: tuple[Document, ...] = (
    # ------------------------------------------------------------------
    # Controls: one house, one topic. The saw must stay shut.
    # ------------------------------------------------------------------
    _d(
        "01-caliper-stilling-control",
        "control",
        ("caliper",),
        ("stilling-well",),
        (
            "The stilling well was opened at 06:40. The float cable showed fourteen millimetres of play. The chart drum had slipped by one hour, so the overnight peak was recorded against the wrong abscissa. A new pen was fitted. The old nib was filed in the tin marked spent. The observer noted a film of algae on the intake strainer and flushed the pipe with a kettle of boiled water. The staff gauge at the wing wall read 0.86 metres. The value was entered twice, once in the book and once on the card that travels with the chart.",
            "The intake strainer was lifted at 07:05 and laid on the coping. Fine silt had packed the mesh on the downstream face. The silt was washed into the bucket, not into the well. The mesh was examined against the sky and two broken wires were noted. A spare strainer was fitted from the store crate. The damaged mesh was tagged and left on the shelf above the oilcans. The well was closed and the padlock was tested twice. The key was returned to the hook labelled river.",
            "The clockwork in the recorder was wound at 07:18. Forty turns were counted aloud. The governor ran true after the third turn. A drop of clock oil was placed on the rear bearing and the surplus was wiped. The chart was aligned to the hour line with a straightedge. A small pencil tick was made at the alignment so a later check could see it. The house thermometer read six degrees. The reading was entered under remarks and underlined once.",
            "The wing-wall staff was photographed at 07:26 with the date slate held against the stone. The slate had been wiped. The camera was held level against the ranging rod. Two frames were taken in case the first caught glare off the water. The slate was returned to the dry box. The observer walked the left bank for thirty metres and noted no fresh slump. The visit card was signed and posted through the depot letter-slot on the way back.",
        ),
        (0, 0, 0),
        "Single Caliper visit. Topic stays on the gauge. Zero hinges must stay zero.",
    ),
    _d(
        "02-placard-cinema-control",
        "control",
        ("placard",),
        ("cinema-booth",),
        (
            "You can start the first reel without waiting for a lecture. Your booth already knows the changeover marks. Open the magazine, seat the film on the sprocket you always use, and you will hear the same soft click the old hands wait for. No mystery. No delay. If the xenon is warm, you will see it in the ammeter before you dim the house. Keep the cue sheet in your pocket. Share it with the person on the second machine. Today is a good day to stop guessing at the joins.",
            "You will treat the carbon stub as a spent tool, not as a souvenir. Your tray is on the right of the lamphouse. Drop the stub, close the lid, and you will keep the floor clear for the next change. If a spark jumped, you will smell it. Open the vent a notch. Your lungs are not part of the lamp. Keep water away from the contacts. Keep a dry rag where your hand already goes.",
            "You can time a changeover on the second machine while the first still runs. Your mark is the circle in the upper right. When it flashes, you will hit the dowser and the motor together. The audience will not thank you. That is the point. Keep the volume where last night left it unless the trailer was loud. Your job is the join they do not notice.",
            "You will log the lamp hours before you lock the booth. Your book is on the nail. Write the number, write the title, and you will save the morning argument. If the rectifier hummed, you will add a line. Small notes keep the big ones from arriving. Take the stairs. The lift can wait. Your night is done when the last frame is in the can and the key is on the hook.",
        ),
        (0, 0, 0),
        "Single Placard booth. You/your stays loud on purpose.",
    ),
    _d(
        "03-pocket-icehouse-control",
        "control",
        ("pocket",),
        ("icehouse",),
        (
            "I got to the icehouse late — the hasp was stiff and my torch kept dying — and the sawdust on the top tier had slumped toward the drain. I could smell wet pine before I saw the leak. I stood there with the rake, feeling slightly foolish, and pulled the upper cakes back into line anyway. The drip from the roof vent made a fat mark on the dirt floor that I will have to explain. I keep thinking about the block I left proud last week. It is only a block. It is also the one that will fuse to its neighbour by Friday.",
            "I wrote the tally on the inside of the door because the slate by the road is always missing. Twenty-eight cakes on the north wall, nineteen on the south, and a gap where I had promised the dairy three more. I ran my hand along the straw and it came away cold and a little green. I do not like that green. I packed fresh sawdust into the gap and told myself it would hold until the next cart. The rake handle is still too short. I keep meaning to splice it.",
            "I ate the apple on the threshold so I would not take crumbs inside. The juice froze on my wrist. I watched a wren use the vent as a door and decided not to chase it — the bird knows the cold better than I do. I checked the thermometer twice because the first reading felt like flattery. Minus two. That will do if the door stays shut. I kicked the threshold clear of ice so the next person will not swear at me.",
            "I left a note under the brick: sawdust topped, leak marked, dairy still owed three. My handwriting looks hurried because it was. I locked the hasp and then tested it, which is the sort of double gesture I only make when I already distrust the morning. Walking back I could hear the river under the path. I keep that sound as proof that the icehouse is not the whole world, even in January.",
        ),
        (0, 0, 0),
        "Single Pocket. Dashes and I/my should not look like a second author.",
    ),
    _d(
        "04-statute-signal-control",
        "control",
        ("statute",),
        ("signal-box",),
        (
            "The signalman shall not leave the box while a train is within the section unless a competent relief has accepted the instruments. Any lever that has been reversed shall be replaced only after the corresponding block indication has been observed and entered. A failed needle shall be treated as a stop signal. The occupation of the section shall be recorded in ink. Pencil shall not be used for the train register except to mark a later correction, and such a mark shall be initialled.",
            "The block bell shall be answered without delay. Any call that is not understood shall be repeated, and shall not be acted upon until the repetition agrees. Food shall not be placed on the instrument shelf. A window shall remain open far enough to hear a detonator. The fire shall be kept such that the room is warm enough for the instruments and not so warm that the paint on the lever leads softens. Oil shall be applied to a lever lead only from the approved can.",
            "A token shall not be issued unless the section is clear and the receiving box has acknowledged. Any token that cannot be accounted for shall be reported at once. The spare tokens shall remain in the locked cupboard. Keys to that cupboard shall not leave the box. If a train is to be divided, the signalman shall not accept a second portion until the first has been reported clear of the points. Such a movement shall be written in the register before it is authorised.",
            "At the end of a turn the signalman shall count the tokens, wind the clock, and enter the lamp hours for the distant. Any defect noted during the turn shall be written on the defect card and shall not be left as a spoken remark. The relief shall read the last six register lines aloud. Acceptance of the box shall be signified by a signature. Until that signature exists the outgoing signalman shall remain.",
        ),
        (0, 0, 0),
        "Holdout control. Statute throughout; deontic verbs must not be read as cuts.",
    ),
    # ------------------------------------------------------------------
    # Easy: house changes and the topic changes with it.
    # ------------------------------------------------------------------
    _d(
        "05-caliper-well-then-placard-booth",
        "easy",
        ("caliper", "placard"),
        ("stilling-well", "cinema-booth"),
        (
            "The stilling well was opened at 06:52. The float sat lower than the previous card had suggested. The observer measured the freeboard with the folding rule and recorded 1.12 metres. A spider had built across the clock face; the web was removed with the dry brush, not with a finger. The chart was changed. The used chart was rolled, labelled, and slid into the tin. Wind on the open water was noted as a light ripple. No boat was seen.",
            "The rain-gauge funnel was inspected on the same visit. A leaf had bridged the knife-edge. The leaf was lifted and the funnel was wiped. The inner can held four millimetres. The amount was poured into the glass measure and read at eye level. The can was replaced dry. The observer stood back from the enclosure so the next photograph would show the whole fence. The padlock was locked. The key was tagged.",
            "You can learn the booth in an evening if you stop treating it like a shrine. Your left hand finds the fire shutter. Your right hand finds the dowser. Open the lamphouse only when the switch is down. You will see the xenon like a small sun and you will not stare at it. Keep the goggles on the hook you can reach without looking. If the ammeter sits where last week sat, you are ready. If it does not, you wait. Waiting is part of the job.",
            "You will finish the night with the same little ritual every time. Your cans go on the rack in title order. Your floor gets a slow look for film chips. You will write the lamp hours before you want to. The morning person will believe the book and not your memory. Take the side stair. Leave the house lights to the usher. Your work ends at the door with the brass plate.",
        ),
        (0, 1, 0),
        "Caliper hydrology then Placard booth. Topic and house jump together.",
    ),
    _d(
        "06-pocket-ice-then-statute-filter",
        "easy",
        ("pocket", "statute"),
        ("icehouse", "slow-sand-filter"),
        (
            "I cracked the icehouse door just enough to feel whether the cold was still honest. It was. I stepped in and the sawdust moved under my boot like dry snow. I had meant to bring a longer rake — I brought the short one again — and I spent a useless minute swearing at the back tier. The cakes along the north wall had a white bloom I do not trust. I scraped one with a nail. Sugar ice, or something that wants to be. I packed it deeper and hoped the dairy would not ask awkward questions.",
            "I sat on the threshold to write the numbers because the interior is too dim for pride. North twenty-six, south eighteen, and the dairy still owed two if I am kind, three if I am exact. I am trying to be exact. A drip from the vent landed on the page and opened the ink. I blotted it with my sleeve. Walking out I left the door ajar for one breath so the wren could leave, then I shut it as if I had not.",
            "The filter attendant shall not walk on the sand while the bed is in service. Any disturbance of the schmutzdecke shall be treated as a fault and shall be entered on the bed card. Scraping shall be carried out only after the water has been drawn down to the approved mark. The scrapings shall be placed in the designated barrow and shall not be returned to the bed. Tools shall be rinsed at the wash-cock and shall be hung so that grit does not fall back onto the sand.",
            "A sample of filtered water shall be taken at the outlet cock at the start of each scrape and at the return to service. The bottle shall be labelled with the bed number and the hour. Any bottle that has been left unstoppered shall be discarded. The attendant shall not return a bed to service until the superintendent has seen the first clear water and has initialled the card. Such initials shall be in ink.",
        ),
        (0, 1, 0),
        "Notebook ice then by-law sand filter. Easy on purpose.",
    ),
    _d(
        "07-bench-box-then-seminar-compass",
        "easy",
        ("bench", "seminar"),
        ("signal-box", "compass-swing"),
        (
            "Anyway the 14:10 was late and the needle stuck in the middle, which is exactly the sort of thing that makes the register look cursed. Don't ask me why the fire went down; I fed it at noon. It's probably fine. I answered the bell twice because the first time I wasn't sure I'd heard five. Honestly the tea tasted of the coal scuttle. If the token is in the wrong cupboard I'll hear about it before the relief even sits down.",
            "Anyway I wrote the 14:10 as delayed and then I wrote a second line because last month I didn't and I got a note. Don't start about the window; it's stiff on the yard side so I left it open a crack. You have to hear a detonator even if you don't want to. It's a small box. It smells of oil and bread. I'm not complaining. Honestly the needle needs a look before someone decides I'm the problem.",
            "We might treat a compass deviation card as a finished object, but a swing against a new cargo suggests a more awkward possibility: the card is a statement about last week's magnetism, not this week's. This does not imply that the pelorus is unusable. It does, however, recommend a pause before we fold the residual into any course that later supports a landfall. Variation of this kind is ordinary in a steel hull. The useful question is whether our correction was stated before we disliked the bearing.",
            "We should also resist the temptation to average an ugly swing until it looks polite. A single wild heading may be a sighting error; a run of them may be the funnel staying in the field. This is not a reason to abandon the trial. It is a reason to write down which heading we trust, and which we are keeping only so the plot has enough points to look like work.",
        ),
        (0, 1, 0),
        "Bench box chatter then Seminar on swinging ship.",
    ),
    _d(
        "08-placard-fognet-then-caliper-marbling",
        "easy",
        ("placard", "caliper"),
        ("fog-net", "paper-marbling"),
        (
            "You can harvest fog without a river if you site the mesh where the cloud already walks. Your ridge is the one with the wet stones at dawn. Stake the net, tension the head rope, and you will hear the first drops before you see them. No pump. No speech. If the wind is along the ridge, you will fill the drum by noon. Keep the hose off the goat path. Share the first litre with the person who minds the cistern. Today is a good day to stop carrying water up the hill.",
            "You will check the mesh for tears after every blow. Your hand finds the hole the same way it finds a snag in a jumper. Tie it, do not patch it with hope. You will keep a spare toggle in the tin. If the drum tastes of the mesh, you will flush it. If it tastes of the hill, you will drink. Label the day on the lid so the next person does not guess.",
            "The size bath was prepared at 09:10. Carrageenan was sprinkled onto cold water and left to stand for twenty minutes. The bath was then stirred with the long rod until the surface showed no lumps. A drop of ox-gall was added and the surface was tested with a single vein of colour. The vein opened slowly. The observer noted that the room was colder than yesterday and moved the bath away from the window. The combs were laid out in order of fineness. The waste jar was empty at the start.",
            "The first sheet was laid at 09:41. The paper was held by opposite corners and lowered until the whole face met the size. A pause of three seconds was counted. The sheet was lifted in one motion and racked. The pattern was a stone drop with a fine comb through the right third. Two faults were noted: a hair on the left edge and a starved corner. The hair was lifted with the needle. The corner was left as evidence. The sheet was labelled on the back in pencil.",
        ),
        (0, 1, 0),
        "Placard fog harvest then Caliper marbling shop.",
    ),
    _d(
        "09-statute-piano-then-pocket-herbarium",
        "easy",
        ("statute", "pocket"),
        ("piano-regulation", "herbarium"),
        (
            "The regulator shall not alter let-off on an instrument that is to be used the same evening unless the player has been told. Any change of aftertouch shall be written on the card inside the keyslip. A broken hammer shank shall be replaced with a part of the same pattern. Glue shall be allowed to set for the time stated on the tin. The lid shall not be closed on an unset repair. Tools shall be counted before the stool is returned to its mark.",
            "The pitch shall be left as found if the room is more than three degrees from the last recorded temperature, except where a rehearsal makes a partial lift unavoidable. Such a lift shall be confined to the unisons most in use and shall be described as temporary on the card. The regulator shall not claim a full concert pitch after a partial lift. Felts that have been treated with any solvent shall be left to air.",
            "I opened the mounting folder and the specimen had shifted — of course it had, I had used too little glue on the thick stem — and a small shower of florets landed on the blotter. I swore under my breath. The label was still honest: river shingle, 12 May, my own hand. I teased the stem back with the needle and felt the paper give. I hate that give. I mixed a fresh drop of paste and told myself this was why we keep duplicates.",
            "I wrote a second label because the first had a thumb-print in the lower corner. Species, place, date, and the fact that the plant was already fruiting, which I keep forgetting to say. I let the paste dry with a square of waxed paper over the junction so I would not glue the genus to my sleeve. Walking home I kept thinking about the florets I lost. They were only florets. They were also the reason I had stopped.",
        ),
        (0, 1, 0),
        "Piano by-law then a herbarium notebook.",
    ),
    _d(
        "10-seminar-grain-then-bench-bells",
        "easy",
        ("seminar", "bench"),
        ("grain-elevator", "change-ringing"),
        (
            "We might treat a dust reading as a local inconvenience, but a run of high figures on the same leg of the house suggests a more structural claim: the leg is making dust, not merely holding it. This does not imply that the house must stop. It does, however, recommend that we stop talking about housekeeping as if a broom were a design. Variation between shifts is ordinary. The useful question is whether our sampling points were chosen before the numbers embarrassed us.",
            "We should write down what we mean by a safe interval. A figure that is acceptable at the boot can be less acceptable at the headhouse, where the air is already doing more work. This is not an argument for panic. It is an argument against averaging the house into one polite number and then being surprised by a bearing.",
            "Anyway the tenor's stay kissed the slider again and I felt it in the floor, which is exactly how you know you've been sloppy. Don't look at me like that; I did pull it off. It's a heavy bell and the rope's newer than my hands. Honestly the treble was late for a whole course and nobody said. If the captain wants a restart I'll take it. I'd rather restart than pretend the row was music.",
            "I coiled the rope the way I was taught and then I recoiled it because the first coil looked like an excuse. The tower smells of dust and wet wool. I'm not romantic about it. I'm just saying the sally's worn on one side and if we ignore that we'll argue about striking when the real argument is a rope. Anyway tea after. That's the part I can do without a lecture.",
        ),
        (0, 1, 0),
        "Holdout easy. Seminar dust then Bench tower.",
    ),
    # ------------------------------------------------------------------
    # Medium: same topic, different house. Topic cannot help.
    # ------------------------------------------------------------------
    _d(
        "11-stilling-caliper-then-placard",
        "medium",
        ("caliper", "placard"),
        ("stilling-well",),
        (
            "The stilling well was opened at 06:37. The float cable showed nine millimetres of play. The observer tightened the clamp and recorded the new freeboard. The chart drum had not slipped. A thin film of oil from the previous visit was wiped from the glass. The staff gauge read 0.79 metres. The figure was entered in the book and again on the travelling card. Wind was noted as nil. The intake sounded clear when the pipe was tapped.",
            "The rain-gauge can was emptied into the measure at 06:48. Two millimetres were recorded. The funnel was free of debris. The enclosure fence had a loose staple on the east post; the staple was hammered home. The observer photographed the staff with the date slate. The slate was returned to the dry box. The padlock was locked. The key was hung on the river hook at the depot.",
            "You can read last night's river without waiting for a clerk. Your phone already knows the staff gauge. Open the page, tap the station you walk past, and you will see the same number the stilling well wrote down. No account. No delay. If the water jumped, you will know before you lock the bike. Keep the station in your pocket. Share it with the person who minds the cellar. Today is a good day to stop guessing.",
            "You will treat a skipped visit as a hole, not as a story. Your note should say that the lock stuck, or that the path was under water. You will not invent a reading. If the app is down, you will write the staff in the paper book and you will take a photograph. The photograph is not art. It is the argument you will need later. Keep the slate clean. Keep the hook honest.",
        ),
        (0, 1, 0),
        "Same well. Caliper visit then Placard app copy.",
    ),
    _d(
        "12-cinema-pocket-then-statute",
        "medium",
        ("pocket", "statute"),
        ("cinema-booth",),
        (
            "I got to the booth early — the street door stuck and my coffee went cold on the stair — and the xenon was already ticking as it cooled from the matinee. I could smell the hot dust in the lamphouse before I opened it. I stood there with the cue sheet, feeling slightly ceremonial, and checked last night's lamp hours anyway. The 2 was written like a 7. I keep thinking about the join I almost missed in the second reel. It is only a mark. It is also the mark the audience would have used to remember us.",
            "I wiped the gate and found a chip of film the size of a nail clipping. I put it in the tin, not on the floor. The take-up was a little proud; I eased it. I wrote a real 2 over the maybe-7 and initialled it, which looks precious until you have been blamed for a lamp. Walking down for the house lights I could hear the usher arguing with a bag. I kept out of it.",
            "The projectionist shall not strike the xenon without the protective glass in place. Any lamp that has exceeded the posted hours shall be treated as due for change and shall not be run as a favour to a late programme. The fire shutter shall be tested at the start of a turn. Film shall not be left threaded on a machine that is to be left unattended. A carbon stub, where such lamps remain, shall be placed in the metal tray and shall not be pocketed.",
            "A changeover shall be executed at the marked cue and shall not be anticipated for convenience. The volume shall be left as set unless a trailer has been logged as loud, in which case the approved drop shall be used and restored. The projectionist shall enter lamp hours, title, and any unusual noise before leaving the booth. Such an entry shall be in ink. The key shall be returned to the hook.",
        ),
        (0, 1, 0),
        "Same booth. Pocket night then Statute rules.",
    ),
    _d(
        "13-filter-seminar-then-bench",
        "medium",
        ("seminar", "bench"),
        ("slow-sand-filter",),
        (
            "We might treat the schmutzdecke as a nuisance layer, but the time it takes to recover after a scrape suggests a more useful claim: the layer is the filter, and the sand is only the furniture. This does not imply that we should never scrape. It does, however, recommend that we stop counting a bed as idle simply because the water is drawn down. Variation between beds is ordinary. The useful question is whether our scrape depth was chosen before we disliked the run time.",
            "We should also be cautious about calling the first clear water a proof. A sample taken at the cock can look better than the water that still sits in the underdrain. This is not an argument against returning a bed to service. It is an argument for writing down which cock we used, and for not averaging two beds into one polite story.",
            "Anyway I scraped bed three this morning and the barrow was heavier than I wanted to admit, which is how you know you went a bit deep. Don't tell the superintendent yet; I wrote the depth honest on the card. It's probably fine? The outlet ran cloudy for twenty minutes and then it didn't. Honestly the wash-cock still drips on my boot. If the sample's ugly I'll hear about it. I rinsed the tools. I hung them. That's the part I can defend.",
            "I took the bottle at the outlet like we're supposed to and then I took a second one because last time I didn't and I got a look. The bed smells of pond and iron. I'm not poetic about it. I'm just saying the schmutzdecke isn't dirt to me anymore, it's the thing doing the work, and if we scrape it for tidiness we'll be here again on Thursday. Anyway tea in the pump house. The kettle's louder than the engine.",
        ),
        (0, 1, 0),
        "Same filter. Seminar caution then Bench scrape.",
    ),
    _d(
        "14-bells-caliper-then-pocket",
        "medium",
        ("caliper", "pocket"),
        ("change-ringing",),
        (
            "The tenor was raised at 19:02. The stay met the slider cleanly. The rope was inspected at the garter hole and no broken strand was found. A chalk mark was placed on the sally at the length used last week. The treble was raised second. The clock in the ringing room was compared with the church clock and a difference of two minutes was noted. The difference was entered on the board. Eight ringers were present. The first course began at 19:11.",
            "The rope of the fifth was re-tied at 19:28 after a slip at the tail. The knot was a double. The old whipping was left in place. A spare sally was not required. The ringing was stood after the course and the ropes were checked in order from treble to tenor. Dust on the fifth box was swept into the tin, not onto the stairs. The board was updated. Tea was noted as available in the vestry.",
            "I took the tenor and felt the stay kiss sooner than I wanted — my own fault, I was showing off a little — and the slider made that dry sound I hate. I stood there with the rope, feeling the floor still moving, and told myself it was only a kiss. It is only a kiss. It is also how stays break. I shortened my pull and I did not look at the captain. The next whole pull was cleaner. I could smell the wet wool of someone's coat.",
            "I coiled my rope at the end and then uncoiled it because the first coil had a twist I would have judged in someone else. I wrote nothing on the board; Caliper already had. Walking down the stair I kept one hand on the wall. I always do that in this tower. The stones sweat. I like them for it, which is a sentence I will not say aloud.",
        ),
        (0, 1, 0),
        "Same tower. Caliper minutes then Pocket guilt.",
    ),
    _d(
        "15-compass-statute-then-placard",
        "medium",
        ("statute", "placard"),
        ("compass-swing",),
        (
            "The vessel shall be swung in a location free from local magnetic disturbance so far as such a location can be obtained. Any heading that cannot be sighted shall be omitted and shall not be invented. The residual shall be recorded for each heading that is observed. A pelorus shall be checked against the standard compass before the trial begins. Food tins and portable radios shall be removed from the vicinity of the binnacle. Such items shall not be returned until the card is complete.",
            "A deviation card shall be dated and shall name the cargo state. Any later change of cargo that is likely to affect the magnetism shall void the card for navigation until a new swing is made. The card shall be posted where the watch can read it. Pencil shall not be used for the residuals. A copy shall be filed with the log. The original shall remain on board.",
            "You can swing the ship without turning the morning into a seminar. Your pelorus is already on the wing. Take the heading, call it, and you will have a point. No speech. If a heading is blind, you skip it. You will not invent a pretty rose. Keep the tins off the binnacle. Share the card with the person who actually steers. Today is a good day to stop using last month's magnetism.",
            "You will date the card before you admire it. Your cargo line is the one that keeps you honest. Write full, write light, write what you have. If the funnel sat in the field, you will say so in a short note. The note is not shame. It is how the next watch avoids your mistake. Pin the card where a hand can find it in the dark. That is the whole job.",
        ),
        (0, 1, 0),
        "Holdout medium. Same swing, Statute then Placard.",
    ),
    # ------------------------------------------------------------------
    # Hard: same topic, houses that share some formal habits.
    # ------------------------------------------------------------------
    _d(
        "16-stilling-caliper-then-seminar",
        "hard",
        ("caliper", "seminar"),
        ("stilling-well",),
        (
            "The stilling well was opened at 06:41. The float cable showed fourteen millimetres of play. The chart drum had slipped by one hour, so the overnight peak was recorded against the wrong abscissa. A new pen was fitted. The old nib was filed in the tin marked spent. The observer noted algae on the intake and flushed the pipe. The staff gauge read 0.86 metres. The value was entered twice. Wind was a light ripple. No correction was applied on site.",
            "The clockwork was wound at 06:55. Forty turns were counted. The chart was aligned to the hour line. A pencil tick marked the alignment. The house thermometer read six degrees. The reading was entered under remarks. The wing-wall staff was photographed with the date slate. Two frames were taken. The visit card was signed. The padlock was locked.",
            "We might treat the overnight peak as a measurement, but the slipped chart drum suggests a more awkward possibility: the peak is a labelling event rather than a hydrological one. This does not imply that the stilling well is unusable. It does, however, recommend a pause before we fold the value into any series that later supports a threshold. Variation of this kind is ordinary in analogue records. The useful question is whether our correction rule is stated in advance.",
            "We should also resist correcting the peak until the tick on the chart has been seen by a second person. A single observer can be sure and still be wrong about an hour. This is not a reason to discard the card. It is a reason to keep the uncorrected trace visible, so that later we can see what we did and not only what we wished the river had done.",
        ),
        (0, 1, 0),
        "Hard: two formal houses on one well. Topic cannot help; I/you are scarce in both.",
    ),
    _d(
        "17-icehouse-pocket-then-bench",
        "hard",
        ("pocket", "bench"),
        ("icehouse",),
        (
            "I got to the icehouse late — the hasp was stiff and my torch kept dying — and the sawdust on the top tier had slumped toward the drain. I could smell wet pine before I saw the leak. I stood there with the rake, feeling slightly foolish, and pulled the upper cakes back into line anyway. The drip from the roof vent made a fat mark on the dirt floor that I will have to explain. I keep thinking about the block I left proud last week.",
            "I wrote the tally on the inside of the door because the slate by the road is always missing. Twenty-eight cakes on the north wall, nineteen on the south, and a gap where I had promised the dairy three more. I ran my hand along the straw and it came away cold and a little green. I packed fresh sawdust into the gap. The rake handle is still too short. I keep meaning to splice it.",
            "Anyway I got there late and the hasp was being itself, which is to say stuck, and the top tier had gone slack toward the drain. Don't ask me why the torch died; I changed the cells on Sunday. It's probably fine? I could smell the pine. Honestly the drip on the floor looks worse than it is. If the dairy counts the cakes I'll hear about the missing three. I shoved the upper ones back. I didn't write a poem about it.",
            "I put the numbers on the door because the roadside slate walks. Twenty-eight, nineteen, and a hole. I'm not proud of the hole. I stuffed sawdust in and told myself Friday is still a real day. The rake's too short, I've said that, I know. Anyway I locked the hasp twice. That's the part I can defend when someone asks why the cakes fused.",
        ),
        (0, 1, 0),
        "Hard: Pocket vs Bench, both first-person, same icehouse. Contractions and anyway should carry it.",
    ),
    _d(
        "18-filter-statute-then-seminar",
        "hard",
        ("statute", "seminar"),
        ("slow-sand-filter",),
        (
            "The filter attendant shall not walk on the sand while the bed is in service. Any disturbance of the schmutzdecke shall be treated as a fault and shall be entered on the bed card. Scraping shall be carried out only after the water has been drawn down to the approved mark. The scrapings shall be placed in the designated barrow and shall not be returned to the bed. Tools shall be rinsed at the wash-cock. A sample shall be taken at the outlet cock at the start of each scrape.",
            "The attendant shall not return a bed to service until the superintendent has seen the first clear water and has initialled the card. Such initials shall be in ink. Any bottle that has been left unstoppered shall be discarded. Food shall not be placed on the filter gallery. A window shall remain open far enough to smell a wrong bed. Oil shall not be stored beside the sample crate.",
            "We might treat a scrape as a housekeeping interval, but the recovery time after an eager barrow suggests a more awkward possibility: we have removed the filter and left the furniture. This does not imply that the rule against walking on the sand is decorative. It does, however, recommend that we write the depth before we start, so that later we cannot pretend the bed asked to be punished. Variation between beds is ordinary. The useful question is who chose the mark.",
            "We should keep the unstoppered-bottle rule even when the gallery is busy. A sample that has breathed the room is not a sample of the bed. This is not an argument for more bottles. It is an argument for treating the cock as a place where we decide what will later be called evidence.",
        ),
        (0, 1, 0),
        "Hard: Statute vs Seminar. Both long and formal; shall vs we/however.",
    ),
    _d(
        "19-signal-caliper-then-statute",
        "hard",
        ("caliper", "statute"),
        ("signal-box",),
        (
            "The box was accepted at 06:00. The tokens were counted and agreed with the cupboard board. The clock was compared with the station clock and no difference was noted. The fire was made up. The distant lamp hours were read and entered. A smear of oil on the instrument shelf was wiped. The last six register lines were read aloud by the outgoing man and initialled. The window on the yard side was opened two notches. No train was in section.",
            "The 06:42 was offered and accepted. The token was issued and the time was entered in ink. The train was reported clear at 06:51. The token was locked back. A goods in the opposite direction was offered at 06:58 and held because the section was not yet quiet in the observer's judgement; a second look at the line was taken. The goods was then accepted. The register shows both times. The fire was fed at 07:05.",
            "The signalman shall not leave the box while a train is within the section unless a competent relief has accepted the instruments. Any lever that has been reversed shall be replaced only after the corresponding block indication has been observed and entered. A failed needle shall be treated as a stop signal. The occupation of the section shall be recorded in ink. Pencil shall not be used for the train register except to mark a later correction, and such a mark shall be initialled.",
            "The block bell shall be answered without delay. Any call that is not understood shall be repeated and shall not be acted upon until the repetition agrees. A token shall not be issued unless the section is clear. Food shall not be placed on the instrument shelf. At the end of a turn the tokens shall be counted, the clock wound, and the distant lamp hours entered. The relief shall read the last six lines aloud.",
        ),
        (0, 1, 0),
        "Holdout hard. Caliper log then Statute of the same box. No you, little I.",
    ),
    # ------------------------------------------------------------------
    # Traps: topic jumps, house stays. The saw must refuse.
    # ------------------------------------------------------------------
    _d(
        "20-caliper-well-then-caliper-booth",
        "trap",
        ("caliper",),
        ("stilling-well", "cinema-booth"),
        (
            "The stilling well was opened at 06:44. The float cable showed eleven millimetres of play. The chart drum had not slipped. A new pen was not required. The observer noted a clean intake and a staff reading of 0.81 metres. The value was entered in the book and on the travelling card. Wind was nil. The rain-gauge can held one millimetre. The amount was measured at eye level and recorded. The padlock was locked.",
            "The clockwork was wound at 06:58. Thirty-eight turns were counted. The chart was aligned. A pencil tick marked the hour line. The house thermometer read five degrees. The reading was entered under remarks. The wing wall was photographed with the date slate. The slate was returned to the dry box. The key was hung on the river hook.",
            "The booth was opened at 17:40. The xenon hours were read from the meter and entered in the book. The gate was inspected and no chip was found. A spare reel was placed on the bench in title order. The fire shutter was tested and returned. The ammeter was noted as steady. The cue sheet was aligned with the first reel. The house telephone was checked. No fault was entered.",
            "The changeover was made at the marked cue. The dowser and the motor were used together. The take-up was observed for one minute after the join. The volume was left as found. At the end of the programme the lamp hours were entered a second time. The cans were racked. The floor was inspected. The key was returned to the hook. The visit card was signed.",
        ),
        (0, 0, 0),
        "Trap: Caliper on a well, then Caliper on a booth. Nouns move; house should not.",
    ),
    _d(
        "21-placard-fog-then-placard-piano",
        "trap",
        ("placard",),
        ("fog-net", "piano-regulation"),
        (
            "You can harvest fog without a speech if you put the mesh where the cloud already walks. Your ridge is the wet one. Stake the net, tension the rope, and you will hear drops before you see them. No pump. If the wind is along the hill, you will fill the drum. Keep the hose off the path. Share the first litre. Today is a good day to stop carrying water.",
            "You will check the mesh after every blow. Your hand finds a hole the way it finds a snag. Tie it. You will keep a spare toggle in the tin. If the drum tastes of mesh, you will flush it. Label the lid. Leave the hill cleaner than you found it. That is the whole instruction.",
            "You can regulate a piano without turning the evening into a legend. Your card is inside the keyslip. Write the let-off, write the aftertouch, and you will save the next visit. No mystery. If the room is cold, you will not chase concert pitch for pride. Keep the solvents off the felts you need tonight. Share the card with the player. Today is a good day to stop guessing at the touch.",
            "You will count the tools before you close the lid. Your stool goes back to the mark. If a shank was replaced, you will say so in a short line. The line is not a confession. It is how morning avoids your surprise. Take the spare glue with you. Leave the keyslip honest.",
        ),
        (0, 0, 0),
        "Trap: Placard fog then Placard piano. You/your throughout.",
    ),
    _d(
        "22-pocket-ice-then-pocket-herbarium",
        "trap",
        ("pocket",),
        ("icehouse", "herbarium"),
        (
            "I cracked the icehouse door and the cold was still honest. I stepped in — the sawdust moved like dry snow — and I saw the slump on the top tier before I wanted to. I had brought the short rake again. I spent a minute I will not get back. The north cakes had that white bloom I do not trust. I scraped one with a nail and packed it deeper. I keep thinking about the dairy.",
            "I sat on the threshold to write the numbers because the interior is too dim for pride. North twenty-six, south eighteen. I blotted a drip of ink with my sleeve. Walking out I left the door ajar for the wren, then I shut it as if I had not. The path sounded like the river. I like that sound more than I like being right about cakes.",
            "I opened the mounting folder and the specimen had shifted — of course it had, I had used too little glue — and a small shower of florets landed on the blotter. I swore under my breath. The label was still honest: river shingle, 12 May, my own hand. I teased the stem back with the needle and felt the paper give. I hate that give. I mixed a fresh drop of paste.",
            "I wrote a second label because the first had my thumb in the corner. Species, place, date, and the fruiting, which I keep forgetting. I let the paste dry under waxed paper so I would not glue the genus to my sleeve. Walking home I kept thinking about the florets. They were only florets. They were also the reason I had stopped.",
        ),
        (0, 0, 0),
        "Trap: Pocket ice then Pocket plants. Dashes stay; topic does not.",
    ),
    _d(
        "23-seminar-compass-then-seminar-grain",
        "trap",
        ("seminar",),
        ("compass-swing", "grain-elevator"),
        (
            "We might treat a compass deviation card as a finished object, but a swing against a new cargo suggests a more awkward possibility: the card is a statement about last week's magnetism. This does not imply that the pelorus is unusable. It does, however, recommend a pause before we fold the residual into any course that later supports a landfall. Variation of this kind is ordinary in a steel hull. The useful question is whether our correction was stated in advance.",
            "We should resist averaging an ugly swing until it looks polite. A single wild heading may be a sighting error; a run of them may be the funnel staying in the field. This is not a reason to abandon the trial. It is a reason to write down which heading we trust, and which we are keeping only so the plot has enough points to look like work.",
            "We might treat a dust reading as a local inconvenience, but a run of high figures on the same leg of the house suggests a more structural claim: the leg is making dust, not merely holding it. This does not imply that the house must stop. It does, however, recommend that we stop talking about housekeeping as if a broom were a design. Variation between shifts is ordinary. The useful question is whether our sampling points were chosen before the numbers embarrassed us.",
            "We should write down what we mean by a safe interval. A figure that is acceptable at the boot can be less acceptable at the headhouse, where the air is already doing more work. This is not an argument for panic. It is an argument against averaging the house into one polite number and then being surprised by a bearing.",
        ),
        (0, 0, 0),
        "Holdout trap. Seminar on a compass, then Seminar on grain dust.",
    ),
    # ------------------------------------------------------------------
    # Returns: ABA. The first saw should still find a side.
    # ------------------------------------------------------------------
    _d(
        "24-stilling-caliper-placard-caliper",
        "return",
        ("caliper", "placard", "caliper"),
        ("stilling-well",),
        (
            "The stilling well was opened at 06:33. The float cable showed eight millimetres of play. The observer tightened the clamp. The staff gauge read 0.77 metres. The figure was entered twice. The rain-gauge can held three millimetres. The amount was read at eye level. The enclosure staple on the east post was firm. The padlock was locked at the end of the first look. The key remained in the hand.",
            "The chart was changed at 06:46. The used chart was rolled and labelled. A pencil tick marked the new alignment. The house thermometer read four degrees. The reading was entered under remarks. The wing wall was photographed. Two frames were taken. The observer stood off the coping so the slate would be readable. No boat was seen. Wind was a light ripple.",
            "You can read this station without waiting for the depot. Your phone already has the staff. Open the page. Tap the name you walk past. You will see the number the well just wrote. No account. If the water jumped, you will know before you lock the bike. Keep your photograph. Share it with the person who minds your cellar. Today is a good day to stop inventing a reading in the kitchen. You do not need a clerk for that.",
            "The well was opened again at 18:10 for the evening card. The float sat where the morning had left it, within a centimetre. The observer recorded 0.78 metres. The intake was tapped and sounded clear. The chart drum had not slipped. A moth was removed from the glass and filed, not in a tin, in the remarks as present. The padlock was locked. The key was hung on the river hook.",
            "The evening rain-gauge can was empty. The fact was recorded as a zero and not as an omission. The fence was felt for the loose staple found last week; the staple was still home. The date slate was wiped and returned. The visit card was signed. The observer walked thirty metres of bank and noted no slump. The depot letter-slot received the card.",
        ),
        (0, 1, 1, 0),
        "ABA on one well: Caliper, Placard, Caliper. Two real hinges.",
    ),
    _d(
        "25-cinema-pocket-statute-pocket",
        "return",
        ("pocket", "statute", "pocket"),
        ("cinema-booth",),
        (
            "I unlocked the booth and the xenon was still faintly warm — leftover from the school show — and I stood there longer than I needed, smelling the dust. I checked the book. The 4 looked like a 9. I wrote over it and felt pedantic. I threaded the first reel slowly so I would not drop a loop. I keep thinking about the usher's argument in the aisle. It is not my argument. It is the sound I start a night with.",
            "The projectionist shall not strike the lamp without the glass in place. Any lamp over the posted hours shall be treated as due for change. The fire shutter shall be tested. Film shall not be left threaded on an unattended machine. A changeover shall be executed at the marked cue and shall not be anticipated. The volume shall be restored after any approved drop. Entries shall be in ink. The key shall return to the hook.",
            "I shut the book harder than the rule deserved — I know that — and I still followed it, which is a kind of truce. The join in reel two was clean. I heard the audience do nothing, which is the review I want. I wiped the gate. I put a chip in the tin. Walking down after the last can I kept my hand on the rail. The brass plate was cold. I like it for that.",
        ),
        (1, 1),
        "ABA booth: Pocket, Statute, Pocket. Short on purpose; both hinges fire.",
    ),
    _d(
        "26-filter-bench-seminar-bench",
        "return",
        ("bench", "seminar", "bench"),
        ("slow-sand-filter",),
        (
            "Anyway I drew bed two down and the schmutzdecke looked like a wet suede coat, which is my way of saying I didn't want to scrape it. Don't start. I scraped it. It's the job. Honestly the barrow wasn't terrible. If the outlet stays cloudy I'll say so. I rinsed the shovel. I hung it. I wrote the depth before I could invent a kinder number.",
            "I took the bottle at the cock and then I stood there like the water was going to congratulate me. It didn't. I'm not offended. I labelled the bottle with the bed and the hour, which is the part that saves me later. The gallery's cold. The window's open because it has to be. Anyway I washed my hands in the same cock, which I probably shouldn't say.",
            "We might treat that scrape as complete because the barrow has left the gallery, but the recovery of the bed is the actual interval. This does not imply that the attendant was idle. It does, however, recommend that we stop calling the drawn-down hour a gap in the work. Variation after a shallow scrape is ordinary. The useful question is whether the depth on the card will still be believed tomorrow.",
            "Anyway the bed came back clearer than I deserved and I wrote that too, because I'm trying not to be the person who only files the ugly hours. Don't make it a moral. It's a card. Honestly the kettle in the pump house is still the loudest machine we have. If the superintendent initials it I'll go home. If not I'll wait. I can wait. I've done worse afternoons.",
        ),
        (0, 1, 1),
        "Holdout return. Bench, Seminar, Bench on one filter.",
    ),
    # ------------------------------------------------------------------
    # Collages: more than two houses.
    # ------------------------------------------------------------------
    _d(
        "27-stilling-four-houses",
        "collage",
        ("caliper", "placard", "seminar", "pocket"),
        ("stilling-well",),
        (
            "The stilling well was opened at 06:29. The float cable showed ten millimetres of play. The staff gauge read 0.74 metres. The figure was entered twice. The rain-gauge can held two millimetres. The amount was measured at eye level. The chart drum had not slipped. A pencil tick marked the hour line. The padlock remained open for the rest of the visit. The key stayed in the observer's pocket, on a string.",
            "You can skip the depot and still be exact. Your phone has the staff. Open the page. Tap this station. You will see the number before your kettle boils. No account. If the number jumps, you will know. Keep your photograph of the slate. Share it with the person under your stairs. Today is a good day to stop copying a neighbour and calling it care. You already have the well in your pocket.",
            "We might treat the agreement between the book and the phone as reassurance, but two copies of one glance are not two measurements. This does not imply that the app is a toy. It does, however, recommend that we keep the staff photograph as the thing we can still argue with. Variation between glances is ordinary. The useful question is which glance we decided to trust before we liked the plot.",
            "I stood on the coping longer than the card needed — the river was doing that pewter thing it does when the wind dies — and I almost did not lock the well. I did lock it. I keep thinking about the neighbour's reading. It is only a number. It is also how a flood story starts. I hung the key on the river hook and felt the string mark my finger.",
        ),
        (1, 1, 1),
        "Four houses, one well. Three hinges, all real.",
    ),
    _d(
        "28-mixed-statute-bench-caliper-placard",
        "collage",
        ("statute", "bench", "caliper", "placard"),
        ("slow-sand-filter", "weather-balloon", "paper-marbling", "soap-kettle"),
        (
            "The filter attendant shall not walk on the sand while the bed is in service. Any disturbance of the schmutzdecke shall be entered on the bed card. Scraping shall wait until the water has been drawn down to the approved mark. Scrapings shall go to the designated barrow. Tools shall be rinsed at the wash-cock and hung so that grit does not return to the sand. A sample bottle shall be labelled with the bed number and the hour.",
            "Anyway the balloon went left of the theodolite and I lost the first minute, which is exactly how a flight becomes a story instead of a plot. Don't ask me why the hydrogen hissed; I tightened the neck twice. It's probably fine? Honestly the sun was in the glass. If the rate of ascent is ugly I'll say so. I wrote the angles I actually saw. I didn't write the ones I wanted.",
            "The size bath was prepared at 10:05. Carrageenan was sprinkled onto cold water and left to stand. The bath was stirred until the surface showed no lumps. A drop of ox-gall was added. The first vein opened slowly. The room was colder than the previous day; the bath was moved from the window. The combs were laid out by fineness. The first sheet was laid at 10:36 and racked after a counted pause. Two faults were noted on the back in pencil.",
            "You can finish a kettle without turning the yard into a legend. Your tallow is already rendered. Add the lye the way your card says, not the way an aunt said, and you will get a soap you can stamp. No speech. If it traces early, you will take it off the fire. Keep the vinegar near your left hand. Share the first bar with the person who cut your wood. Today is a good day to stop guessing at the boil. You will know the trace when you see it.",
        ),
        (1, 1, 1),
        "Holdout collage. Four houses and four topics. Every hinge is a cut.",
    ),
)


def by_code() -> dict[str, Document]:
    return {d.code: d for d in DOCUMENTS}


def in_band() -> tuple[Document, ...]:
    return tuple(d for d in DOCUMENTS if not d.holdout)


def holdout() -> tuple[Document, ...]:
    return tuple(d for d in DOCUMENTS if d.holdout)
