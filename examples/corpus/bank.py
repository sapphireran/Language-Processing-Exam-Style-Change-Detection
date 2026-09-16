"""Original 30-document bank. Not PAN data. Not scraped.

Each block is one analysis unit (blank-line paragraph) tagged with a
house and a topic. The detector sees only the text.
"""

from __future__ import annotations

from typing import TypedDict


class Block(TypedDict):
    house: str
    topic: str
    text: str


class Document(TypedDict):
    ident: int
    slug: str
    difficulty: str
    title: str
    holdout: bool
    blocks: list[Block]


def _b(house: str, topic: str, text: str) -> Block:
    return {"house": house, "topic": topic, "text": " ".join(text.split())}


def _d(
    ident: int,
    slug: str,
    difficulty: str,
    title: str,
    blocks: list[Block],
    holdout: bool = False,
) -> Document:
    return {
        "ident": ident,
        "slug": slug,
        "difficulty": difficulty,
        "title": title,
        "holdout": holdout,
        "blocks": blocks,
    }


DOCUMENTS: list[Document] = [
    _d(
        1,
        "skiff-eel-control",
        "control",
        "Skiff stays on the eel weir",
        [
            _b(
                "skiff",
                "eel",
                """
                I don't trust a stake that won't take a twist. I'll walk the
                weir at slack and I'll feel for the ones that have gone soft.
                My hands know the mud better than any chart. So I splice the
                broken withy and I get out before the flood.
                """,
            ),
            _b(
                "skiff",
                "eel",
                """
                I set the wings tighter than last week. I don't like the gap
                at the third pair. I'll drive one more stake and I'll lash it
                down with the wet cord. Then I sit on the bank and I wait for
                the run.
                """,
            ),
            _b(
                "skiff",
                "eel",
                """
                I hauled a thin catch at first light. I don't mind a thin
                morning if the mouths are clean. I'll ice them in the box and
                I'll keep the slime off my knife. So I rinse the boards and I
                start the next lift.
                """,
            ),
            _b(
                "skiff",
                "eel",
                """
                I won't leave the old net in the current. I'll roll it, I'll
                pick the sticks out, and I'll hang it where the wind can work.
                My shoulder is loud about it. Then I lock the hut and I walk
                the bank path home.
                """,
            ),
        ],
    ),
    _d(
        2,
        "roll-hop-control",
        "control",
        "Roll minutes stay in the oast",
        [
            _b(
                "roll",
                "hop",
                """
                The committee shall receive the oast temperature log before
                noon. Members must initial the kiln sheet when the cones have
                reached the agreed brittleness. It was resolved that no sack
                shall leave the loft until the moisture card has been filed.
                The clerk shall retain a second copy with the harvest date.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                The drying floor was inspected at two-hour intervals. The
                committee must be notified if the upper slats were found above
                the marked band. It was agreed that the fan shall remain on
                until the cones rattle. The minutes shall record the operator
                and the time of each check.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                Members were asked to confirm the bale weights against the
                warehouse book. The clerk shall enter any shortfall in red.
                It was resolved that mixed lots must not be stacked with the
                single-yard cones. The committee shall review the stack plan
                at the next sitting.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                The oast door was reported as warped on the west side. The
                committee shall commission a joiner before the next pick. It
                was noted that smoke was seen at the cowl on Tuesday. Members
                must not open the kiln while the cones are still in sweat.
                """,
            ),
        ],
    ),
    _d(
        3,
        "twine-lime-control",
        "control",
        "Twine stays on the lime kiln",
        [
            _b(
                "twine",
                "lime",
                """
                You'll want to check the draw hole before you light anything,
                maybe twice if the wind is a bit sideways. Don't rush the
                charge; you can sort of feel when the stone has taken the
                heat. If your gloves are damp you'll know it. Can you wait a
                little longer than the card says?
                """,
            ),
            _b(
                "twine",
                "lime",
                """
                You might riddle the small stuff before you feed the eye.
                Don't pack it tight; you'll choke the draught and then you'll
                get a sulky burn. Your best tell is a bit of white at the
                core, maybe not the whole charge. You can poke once if you're
                unsure.
                """,
            ),
            _b(
                "twine",
                "lime",
                """
                You'll see a crust if you draw too early. Don't chip at it
                like you're angry; you can sort of lift the baked layer and
                leave the rest. Your barrow will take a bit more if you wet
                the path. Maybe let it slack in the air before you bag it?
                """,
            ),
            _b(
                "twine",
                "lime",
                """
                You don't need a speech about safety. You'll keep your face
                off the eye and you'll step back when it coughs. If your
                boots are thin you'll feel the clinker. Maybe that's enough
                for one afternoon. Can you bank it and walk away?
                """,
            ),
        ],
    ),
    _d(
        4,
        "vellum-millrace-control",
        "control",
        "Vellum stays on the millrace",
        [
            _b(
                "vellum",
                "millrace",
                """
                We ought to treat the millrace as a single argument rather
                than a sequence of repairs. One therefore notes the ice
                shelf, the rack, and the drowned willow as parts of the same
                claim. This does not imply that every winter will repeat the
                last; however, the useful question is how the water is being
                asked to turn.
                """,
            ),
            _b(
                "vellum",
                "millrace",
                """
                We should refuse a patch that leaves the race unexplained.
                One can admire a new board and still ask what the old leak
                was doing to the wheel. Therefore the survey is not a list of
                faults. It is an attempt to keep the whole cut in view.
                """,
            ),
            _b(
                "vellum",
                "millrace",
                """
                Our habit has been to praise the miller and to ignore the
                bank. We ought to reverse that, at least for a season.
                However charming the wheel looks from the lane, the argument
                lives in the silt. One does not correct a race by painting
                the launder.
                """,
            ),
            _b(
                "vellum",
                "millrace",
                """
                We may then ask what a good winter would look like. One
                answer is a rack that can be lifted without drama and a bank
                that does not calve into the cut. Therefore the work is
                modest and the claim is large. This does not require a
                manifesto; it requires a season of looking.
                """,
            ),
        ],
        holdout=True,
    ),
    _d(
        5,
        "flint-salt-control",
        "control",
        "Flint stays on the salt pan",
        [
            _b(
                "flint",
                "salt",
                """
                Wind 12 kn, NE. Brine 23.8 Be at 05:15. Table 2 rake, 16 m.
                Foam line 0.4 m from sluice. Leak: none.
                """,
            ),
            _b(
                "flint",
                "salt",
                """
                Sun hard, 07:40. Crystal depth 3 cm west, 2 cm east. Rake
                pass 4. Bittern drawn 80 L. Bird prints on table 1: 6.
                """,
            ),
            _b(
                "flint",
                "salt",
                """
                Wind drop to 6 kn by 11:00. Gate 3 open 2 notches. Pan
                temperature 18 C. Sample jar 7 filled. Residue on flume:
                0.2 kg.
                """,
            ),
            _b(
                "flint",
                "salt",
                """
                Cover on at 16:20. Night forecast 4 C. Stack count 14 bags
                at 25 kg. Sluice pins checked: 8 of 8. End card.
                """,
            ),
        ],
    ),
    _d(
        6,
        "brine-peat-control",
        "control",
        "Brine stays on the peat stack",
        [
            _b(
                "brine",
                "peat",
                """
                A stack shall be faced on the windward side before the first
                frost. Turves must be set crown-out and no course shall
                exceed the marked gauge. Water shall not be permitted to
                stand at the foot. The inspector shall record the height in
                metres and the date of capping.
                """,
            ),
            _b(
                "brine",
                "peat",
                """
                Loose rind must be pinned before the next rain. A gap in the
                face shall be treated as a defect, not as a vent. The path
                around the stack shall be kept clear to the width of a barrow.
                No fire shall be lit within the marked ring.
                """,
            ),
            _b(
                "brine",
                "peat",
                """
                Capping sods shall overlap by not less than a hand. The tie
                poles must be driven to the firm. A stack that leans shall
                be restacked; it shall not be guyed as a substitute. The
                record shall name the cutter and the field.
                """,
            ),
            _b(
                "brine",
                "peat",
                """
                Cutting shall cease when the pit shows standing water above
                the last spit. Tools must be cleaned of seed before they
                leave the moss. A borrowed barrow shall be returned on the
                same day. The gate shall be shut and the latch dropped.
                """,
            ),
        ],
    ),
    _d(
        7,
        "skiff-eel-then-roll-hop",
        "easy",
        "Skiff eel weir, then Roll hop minutes",
        [
            _b(
                "skiff",
                "eel",
                """
                I walked the north wing in the dark. I don't like how the
                current talks there. I'll move two stakes tomorrow and I'll
                take the spare cord. So I mark the soft one with a rag.
                """,
            ),
            _b(
                "skiff",
                "eel",
                """
                I keep a spare needle in my hat. I don't lose it if I pin it
                right. I'll mend the bag on the bank and I'll test it with a
                stone. Then I coil the spare line and I sit.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                The committee shall approve the pickers list before Friday.
                Members must sign against their rows. It was resolved that
                children shall not work the upper kiln. The clerk shall post
                the hours on the oast door.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                The cones were sampled from three pockets. The committee must
                reject any lot that was found green at the core. It was
                agreed that the rejected sacks shall be returned to the yard.
                The minutes shall name the sampler.
                """,
            ),
        ],
    ),
    _d(
        8,
        "twine-lime-then-vellum-millrace",
        "easy",
        "Twine lime kiln, then Vellum millrace",
        [
            _b(
                "twine",
                "lime",
                """
                You'll hear the kiln change its voice when the charge is
                nearly done. Don't trust the first quiet; you can wait a bit
                and listen again. Your poker will tell you more than the
                smoke. Maybe give it one more hour?
                """,
            ),
            _b(
                "twine",
                "lime",
                """
                You can rake a path for the next load now. Don't leave the
                barrow where you'll trip. If your eyes are full of dust
                you'll miss the crack in the eye. Sort of circle it once
                before you go.
                """,
            ),
            _b(
                "vellum",
                "millrace",
                """
                We ought to admit that the millrace is a public sentence
                written in water. One therefore reads the debris as clauses,
                not as waste. However local the repair, the grammar belongs
                to the whole cut. This does not flatter the owner.
                """,
            ),
            _b(
                "vellum",
                "millrace",
                """
                Our maps still stop at the wheel. We should draw the race
                back to the first hatch. Therefore a walk in the rain is not
                a hobby. It is the cheapest way to keep the argument honest.
                """,
            ),
        ],
    ),
    _d(
        9,
        "flint-salt-then-brine-peat",
        "easy",
        "Flint salt card, then Brine peat statute",
        [
            _b(
                "flint",
                "salt",
                """
                Tide 1.8 m at 04:50. Intake open 3. Brine 22.1 Be. First
                rake 05:30, 12 m. Gulls: 9.
                """,
            ),
            _b(
                "flint",
                "salt",
                """
                Cloud 80 percent by 09:00. Halt rake. Cover 40 percent of
                table 2. Sample 3: 21.4 Be. Rain start 09:22.
                """,
            ),
            _b(
                "brine",
                "peat",
                """
                The face that sheds water shall be preferred to the face that
                looks even. The turves must be laid dry-side out on the
                windward wall. No person shall climb the finished stack. The
                inspector shall photograph the cap from the two named angles.
                """,
            ),
            _b(
                "brine",
                "peat",
                """
                The cutting line shall follow the last year's spit. A new
                pit must not be opened without a mark on the plan. Tools
                shall be counted out and counted in. The hut key must hang
                on the named hook.
                """,
            ),
        ],
    ),
    _d(
        10,
        "roll-hop-then-skiff-willow",
        "easy",
        "Roll hop minutes, then Skiff willow beds",
        [
            _b(
                "roll",
                "hop",
                """
                The committee shall set the start of pick for Monday. Members
                were reminded that the bins must be tagged before they leave
                the garden. It was resolved that late arrivals shall work the
                lower rows. The clerk shall keep the tally stick.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                The cowl was reported stiff. The committee must obtain a
                smith before the next sweat. It was noted that the ladder
                was cracked on the third rung. Members shall not use that
                ladder.
                """,
            ),
            _b(
                "skiff",
                "willow",
                """
                I cut the withies while they're still drinking. I don't wait
                for the book to say spring. I'll sort them by thickness on
                the grass and I'll tie the bundles myself. So I keep the
                crooked ones for the garden.
                """,
            ),
            _b(
                "skiff",
                "willow",
                """
                I peel a few to see the colour. I don't strip the whole bed
                in one go. I'll leave the stools a chance and I'll come back
                after rain. Then I stack the rods in the shade.
                """,
            ),
        ],
        holdout=True,
    ),
    _d(
        11,
        "vellum-cider-then-flint-charcoal",
        "easy",
        "Vellum cider press, then Flint charcoal clamp",
        [
            _b(
                "vellum",
                "cider",
                """
                We ought to talk about cider as a pressure, not as a festival.
                One therefore watches the cloths, the hair, and the first
                run as a single claim about patience. However sweet the
                smell, the argument is in the pomace. This does not need a
                speech at the orchard gate.
                """,
            ),
            _b(
                "vellum",
                "cider",
                """
                Our habit is to praise the vintage and to forget the press.
                We should reverse that. Therefore a stained screw is more
                interesting than a label. One does not make a year by naming
                it.
                """,
            ),
            _b(
                "flint",
                "charcoal",
                """
                Clamp 3.2 m long, 1.4 m high. Turf cover 12 cm. Vents: 7.
                Lighted 18:10. Smoke colour: pale. Wind 4 kn, W.
                """,
            ),
            _b(
                "flint",
                "charcoal",
                """
                Night check 01:00. Collapse at vent 2, 20 cm. Patched with
                8 sods. Temp stick 70 C at 0.4 m. No flame.
                """,
            ),
        ],
    ),
    _d(
        12,
        "brine-granite-then-twine-tide",
        "easy",
        "Brine granite setts, then Twine tide mill",
        [
            _b(
                "brine",
                "granite",
                """
                Setts shall be laid to the string and not to the eye. A
                course that wanders must be lifted. Sand shall be dry and
                the joints shall be packed before the next row. The inspector
                shall refuse a face that drums.
                """,
            ),
            _b(
                "brine",
                "granite",
                """
                Kerbs must be bedded before the first sett is placed. No
                offcut shall be used in the running bond. Water shall be
                kept off the bed until the day's work is covered. The bar
                shall not be left in the road.
                """,
            ),
            _b(
                "twine",
                "tide",
                """
                You'll want to read the race before you drop the paddles,
                maybe twice if the wind is pushing the pool. Don't force the
                wheel; you can wait a bit for the next lift. Your feet will
                tell you when the boards are taking water. Can you hear the
                slap change?
                """,
            ),
            _b(
                "twine",
                "tide",
                """
                You might grease the gudgeon while you've got slack. Don't
                leave the can on the walk; you'll kick it. If your gloves
                are wet you'll drop the pin. Sort of count the cogs once
                before you close the hatch.
                """,
            ),
        ],
    ),
    _d(
        13,
        "skiff-then-twine-coble",
        "medium",
        "Same coble, Skiff then Twine",
        [
            _b(
                "skiff",
                "coble",
                """
                I roll the coble and I find the weep above the garboard. I
                don't like a weep that talks after a dry week. I'll warm the
                pitch and I'll work it in with my thumb. So I keep the rag
                handy.
                """,
            ),
            _b(
                "skiff",
                "coble",
                """
                I set the boat on the chocks myself. I don't trust a boy
                with the keel. I'll check the scarf and I'll tap for a dull
                note. Then I light the pot and I wait.
                """,
            ),
            _b(
                "twine",
                "coble",
                """
                You'll smell the pitch before you see it take. Don't flood
                the seam; you can sort of feed it and watch it sit. Your
                thumb is better than a knife here. Maybe let it skin before
                you launch?
                """,
            ),
            _b(
                "twine",
                "coble",
                """
                You can walk the other side now. Don't lean on the gunwale
                while it's soft. If your boots are tarry you'll track it
                into the shed. A bit of sand on the path helps. Can you
                rinse the irons before they set?
                """,
            ),
        ],
    ),
    _d(
        14,
        "flint-then-brine-lime",
        "medium",
        "Same lime kiln, Flint then Brine",
        [
            _b(
                "flint",
                "lime",
                """
                Charge 1.6 t stone, 0.4 t culm. Lit 05:05. Draught good.
                Eye colour: rose. Wind 9 kn, SW.
                """,
            ),
            _b(
                "flint",
                "lime",
                """
                Draw 1 at 14:20, 180 kg. Fines 12 percent. Core white.
                Unburnt: 3 pieces. Banked 16:40.
                """,
            ),
            _b(
                "brine",
                "lime",
                """
                A kiln shall not be drawn until the core is white throughout.
                Stone must be of the named bed. Culm shall be stored dry.
                The inspector shall weigh the first draw and shall record
                the unburnt count.
                """,
            ),
            _b(
                "brine",
                "lime",
                """
                The eye shall be kept clear of clinker. No person shall
                stand in the fume. Tools must be quenched before they are
                hung. The yard gate shall be locked after the last barrow.
                """,
            ),
        ],
    ),
    _d(
        15,
        "roll-then-vellum-willow",
        "medium",
        "Same willow beds, Roll then Vellum",
        [
            _b(
                "roll",
                "willow",
                """
                The committee shall fix the cutting week before the flood
                calendar is printed. Members were shown the stools that were
                damaged last year. It was resolved that those stools shall
                be rested. The clerk must mark them with lime.
                """,
            ),
            _b(
                "roll",
                "willow",
                """
                The bundles were counted at the gate. The committee must
                reject any tie that was made with wire. It was agreed that
                the peelings shall stay on the bed. The minutes shall record
                the cutter and the yard.
                """,
            ),
            _b(
                "vellum",
                "willow",
                """
                We ought to treat a withy bed as a slow sentence, not as a
                crop that happens to be long. One therefore counts the stools
                as clauses. However convenient a clean cut looks, the
                argument is in what is left to drink. This does not license
                a greedy week.
                """,
            ),
            _b(
                "vellum",
                "willow",
                """
                Our maps call it waste ground. We should refuse that name.
                Therefore a walk among the rods is fieldwork. One does not
                understand a bed from the road.
                """,
            ),
        ],
    ),
    _d(
        16,
        "skiff-then-flint-peat",
        "medium",
        "Same peat moss, Skiff then Flint",
        [
            _b(
                "skiff",
                "peat",
                """
                I cut with the wind at my back. I don't fight a gust on the
                moss. I'll lay the turves to dry in little roofs and I'll
                turn them when I hear them skin. So I keep my tea in the
                tin.
                """,
            ),
            _b(
                "skiff",
                "peat",
                """
                I sank to the knee near the old pit. I don't go that way
                twice. I'll mark it with a stick and I'll tell the boy.
                Then I rinse the spade and I sit on the dry bank.
                """,
            ),
            _b(
                "flint",
                "peat",
                """
                Pit 4, spit 3. Depth 0.9 m. Water 0.2 m at face. Turves
                out: 240. Wind 11 kn, W. Break 10:15.
                """,
            ),
            _b(
                "flint",
                "peat",
                """
                Stack A: 1.8 m, lean 5 deg to east. Pins: 6. Cap sods 40.
                Rain 14:05, 20 min. Tools in: 4 of 4.
                """,
            ),
        ],
        holdout=True,
    ),
    _d(
        17,
        "twine-then-roll-salt",
        "medium",
        "Same salt works, Twine then Roll",
        [
            _b(
                "twine",
                "salt",
                """
                You'll want to walk the tables before the sun is high, maybe
                once more if last night was a bit damp. Don't scrape to the
                board; you can leave a skin. Your back will tell you when
                you have done enough. Can you feel the grit change?
                """,
            ),
            _b(
                "twine",
                "salt",
                """
                You might cover the west table first. Don't wait for the
                cloud to decide. If your rake is nicked you'll leave lines.
                Sort of test a corner and see. A bit of brine on the
                handle helps it slide.
                """,
            ),
            _b(
                "roll",
                "salt",
                """
                The committee shall receive the brine strengths each evening.
                Members were shown the tables that were left uncovered.
                It was resolved that those tables must be inspected at dawn.
                The clerk shall keep the Beaume book.
                """,
            ),
            _b(
                "roll",
                "salt",
                """
                The sluices were reported stiff. The committee must order
                grease before the next spring tide. It was noted that two
                bags were short. Members shall not release a load without
                the second weight.
                """,
            ),
        ],
    ),
    _d(
        18,
        "vellum-then-brine-hurdle",
        "medium",
        "Same wattle hurdles, Vellum then Brine",
        [
            _b(
                "vellum",
                "hurdle",
                """
                We ought to see a hurdle as a portable hedge, not as a
                rustic decoration. One therefore asks how the weave takes
                wind and how the feet take mud. However pretty a tight
                pattern looks, the claim is whether a ewe can lean. This
                does not require a catalogue.
                """,
            ),
            _b(
                "vellum",
                "hurdle",
                """
                Our hands remember the twist better than our notes. We
                should still write the notes. Therefore a day in the yard
                is both craft and record. One does not keep a skill by
                watching it from the gate.
                """,
            ),
            _b(
                "brine",
                "hurdle",
                """
                A hurdle shall be woven to the stated width and height. The
                sails must be of the named year's growth. No broken rod
                shall be hidden in the body. The inspector shall reject a
                frame that springs.
                """,
            ),
            _b(
                "brine",
                "hurdle",
                """
                Feet shall be bound before the first sail is started. The
                finished hurdle must stand without a wobble. Water shall not
                be used to force a dry rod. The stamp shall be placed on the
                top sail.
                """,
            ),
        ],
    ),
    _d(
        19,
        "skiff-then-vellum-eel",
        "hard",
        "Same eel weir, Skiff then Vellum",
        [
            _b(
                "skiff",
                "eel",
                """
                I know this bend by the way it pulls. I don't need the map.
                I'll reset the bag after the lift and I'll check the mouth
                for sticks. So I keep my lamp low.
                """,
            ),
            _b(
                "skiff",
                "eel",
                """
                I lost a glove in the mud last night. I don't go after it.
                I'll cut a new pair from the spare hide and I'll oil them.
                Then I go back to the wing.
                """,
            ),
            _b(
                "vellum",
                "eel",
                """
                We ought to read a weir as a negotiation with a tide, not as
                a trap that happens to work. One therefore watches the slack
                as carefully as the run. However local the stakes look, the
                argument is the whole bend. This does not make a romance of
                mud.
                """,
            ),
            _b(
                "vellum",
                "eel",
                """
                Our records treat the catch as the only fact. We should
                refuse that. Therefore a ruined wing is as informative as a
                full bag. One does not understand a weir by counting eels.
                """,
            ),
        ],
    ),
    _d(
        20,
        "roll-then-flint-oast",
        "hard",
        "Same hop oast, Roll then Flint",
        [
            _b(
                "roll",
                "hop",
                """
                The committee shall confirm the kiln schedule for the late
                garden. Members were advised that the upper floor was hotter
                than the band. It was resolved that the fan shall run an
                extra hour. The clerk must note the cone rattle time.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                The pockets were sewn in the loft. The committee must reject
                any pocket that was left untagged. It was agreed that the
                press shall be cleaned before the next lot. The minutes
                shall name the sewer.
                """,
            ),
            _b(
                "flint",
                "hop",
                """
                Floor 2: 62 C at 10:00, 58 C at 12:00. Fan on. Cone
                rattle at 13:40. Moisture card 9 percent. Bales: 6.
                """,
            ),
            _b(
                "flint",
                "hop",
                """
                Pocket tags 1-6. Press 0.8 t. Loft humidity 48 percent.
                Cowl free. Ladder rungs: 11 sound, 1 cracked. End.
                """,
            ),
        ],
    ),
    _d(
        21,
        "twine-then-brine-kiln",
        "hard",
        "Same lime kiln, Twine then Brine",
        [
            _b(
                "twine",
                "lime",
                """
                You'll know a good stone by the way it breaks, maybe more
                than by the colour. Don't feed the dusty stuff first; you
                can keep it for the top. Your ears do a bit of the work
                once the eye is loud. Can you hear a hollow in there?
                """,
            ),
            _b(
                "twine",
                "lime",
                """
                You might rest the barrow on the uphill side. Don't block
                the path you'll need at dusk. If your scarf is loose you'll
                catch a spark. Sort of tuck it and keep going.
                """,
            ),
            _b(
                "brine",
                "lime",
                """
                Stone shall be broken to the stated gauge before it is
                charged. Dust must not form the first layer. The eye shall
                remain visible from the marked stance. The inspector shall
                halt a burn that shows flame at the cap.
                """,
            ),
            _b(
                "brine",
                "lime",
                """
                Drawings shall be cooled on the named floor. No bag shall
                be filled from a hot heap. Water must be kept from the culm.
                The tally shall be closed before the gate is locked.
                """,
            ),
        ],
    ),
    _d(
        22,
        "flint-then-skiff-millrace",
        "hard",
        "Same millrace, Flint then Skiff",
        [
            _b(
                "flint",
                "millrace",
                """
                Hatch 1: 0.35 m open. Rack debris 4 kg. Ice shelf 8 cm on
                north bank. Wheel rpm 12. Leak at launder joint: drip.
                """,
            ),
            _b(
                "flint",
                "millrace",
                """
                Silt 0.22 m at bend 3. Willow lean 20 deg. Board 7
                sprung. Temp 1 C. Walk time 18 min.
                """,
            ),
            _b(
                "skiff",
                "millrace",
                """
                I poke the ice with a pole and I listen. I don't stand on
                it. I'll clear the rack with the long hook and I'll pile
                the sticks on the bank. So I keep my boots on the boards.
                """,
            ),
            _b(
                "skiff",
                "millrace",
                """
                I know the sprung board by the sound. I don't cross it
                loaded. I'll wedge it for today and I'll bring a new one
                tomorrow. Then I shut the hatch a little and I watch the
                wheel.
                """,
            ),
        ],
        holdout=True,
    ),
    _d(
        23,
        "brine-then-twine-withy",
        "hard",
        "Same withy beds, Brine then Twine",
        [
            _b(
                "brine",
                "willow",
                """
                Cutting shall follow the marked stools only. A rod thinner
                than the gauge must be left. Bundles shall be tied with
                withy, not with twine from the shop. The inspector shall
                count the stools before and after.
                """,
            ),
            _b(
                "brine",
                "willow",
                """
                Peelings shall remain on the bed. No fire shall be lit among
                the stools. The gate must be shut against stock. The date
                of cut shall be painted on the first post.
                """,
            ),
            _b(
                "twine",
                "willow",
                """
                You'll want to cut on a dull day, maybe after a bit of rain
                so the bark gives. Don't strip a stool bald; you can leave
                a few rods to drink. Your knife stays cleaner if you wipe
                it. Can you feel the green still in there?
                """,
            ),
            _b(
                "twine",
                "willow",
                """
                You might sort the crooked ones now. Don't throw them in
                the ditch; you'll want them for ties. If your hands are
                cold you'll nick the good rods. Sort of breathe on them and
                keep the pile in the shade.
                """,
            ),
        ],
    ),
    _d(
        24,
        "vellum-then-roll-setts",
        "hard",
        "Same granite setts, Vellum then Roll",
        [
            _b(
                "vellum",
                "granite",
                """
                We ought to treat a street of setts as a held argument, not
                as a surface that happens to be old. One therefore listens
                for the drum and watches the wander of the bond. However
                even a repaired patch looks, the claim is the whole face.
                This does not romanticise granite.
                """,
            ),
            _b(
                "vellum",
                "granite",
                """
                Our habit is to point at a puddle and call it a fault. We
                should ask what the bed is doing. Therefore a day with a
                string is more honest than a day with a speech. One does
                not level a street by wishing it flat.
                """,
            ),
            _b(
                "roll",
                "granite",
                """
                The committee shall inspect the east face before the market.
                Members were shown the courses that were laid off the string.
                It was resolved that those courses must be lifted. The clerk
                shall note the drumming bays.
                """,
            ),
            _b(
                "roll",
                "granite",
                """
                The sand was reported damp. The committee must halt the work
                until it was dried. It was agreed that the bar shall be
                stored off the carriageway. Members shall not accept a face
                that wanders.
                """,
            ),
        ],
    ),
    _d(
        25,
        "skiff-eel-then-skiff-hop",
        "trap",
        "Same Skiff, eel weir then hop garden",
        [
            _b(
                "skiff",
                "eel",
                """
                I rinse the bag in the slack. I don't beat it on a stone.
                I'll hang it and I'll watch for holes while it drips. So I
                keep the needle in my teeth.
                """,
            ),
            _b(
                "skiff",
                "eel",
                """
                I eat on the bank with my back to the wind. I don't mind
                the smell. I'll finish the tea and I'll go again. Then I
                check the wings one last time.
                """,
            ),
            _b(
                "skiff",
                "hop",
                """
                I pick the lower bine first. I don't stretch for the pretty
                cones. I'll fill my bin and I'll drag it to the alley. So I
                keep my knife shut until I need it.
                """,
            ),
            _b(
                "skiff",
                "hop",
                """
                I hate the kiln heat on my face. I don't stay up there long.
                I'll turn the cones when I'm told and I'll get down. Then I
                drink and I sit on the steps.
                """,
            ),
        ],
    ),
    _d(
        26,
        "roll-lime-then-roll-millrace",
        "trap",
        "Same Roll, lime kiln then millrace",
        [
            _b(
                "roll",
                "lime",
                """
                The committee shall receive the kiln log each Friday. Members
                were informed that the last charge was drawn late. It was
                resolved that the next burn must start at dawn. The clerk
                shall keep the culm weights.
                """,
            ),
            _b(
                "roll",
                "lime",
                """
                The eye was reported dirty. The committee must order a
                clearing before the next charge. It was noted that two barrows
                were left in the rain. Members shall not leave tools in the
                yard.
                """,
            ),
            _b(
                "roll",
                "millrace",
                """
                The committee shall walk the race after the next frost.
                Members were shown the boards that were sprung. It was
                resolved that those boards must be replaced. The clerk shall
                write to the miller.
                """,
            ),
            _b(
                "roll",
                "millrace",
                """
                The hatch gear was reported stiff. The committee must obtain
                grease and a spare pin. It was agreed that the willow shall
                be cut back. Members shall not stand on the ice shelf.
                """,
            ),
        ],
        holdout=True,
    ),
    _d(
        27,
        "flint-cider-then-flint-charcoal",
        "trap",
        "Same Flint, cider press then charcoal clamp",
        [
            _b(
                "flint",
                "cider",
                """
                Press start 08:10. Cloths: 12. Hair 4 cm. First run 40 L
                in 25 min. Screw turns: 18. Temp 11 C.
                """,
            ),
            _b(
                "flint",
                "cider",
                """
                Second cheese 09:05. Pomace 22 kg. Juice 35 L. Leak at
                tray corner: drip. Washed cloths 6. Break 09:40.
                """,
            ),
            _b(
                "flint",
                "charcoal",
                """
                Clamp 2.9 m, cover 10 cm. Vents 6. Lighted 17:50. Smoke
                pale to grey. Wind 3 kn, N. Watch 22:00: steady.
                """,
            ),
            _b(
                "flint",
                "charcoal",
                """
                Open 40 h. Yield 86 kg. Fines 8 percent. Unburnt ends: 5.
                Stored in bins 2 and 3. Rain after close: none.
                """,
            ),
        ],
    ),
    _d(
        28,
        "twine-peat-then-twine-salt",
        "trap",
        "Same Twine, peat moss then salt table",
        [
            _b(
                "twine",
                "peat",
                """
                You'll want to test the face with your heel, maybe more than
                once if it looks a bit shiny. Don't step where it gives.
                You can lay the next row on the drier strip. Can you hear
                the suck under there?
                """,
            ),
            _b(
                "twine",
                "peat",
                """
                You might turn the early turves this afternoon. Don't stack
                them wet; you'll get a sulky heap. If your back is loud
                you'll know to stop. Sort of count a smaller pile and leave.
                """,
            ),
            _b(
                "twine",
                "salt",
                """
                You'll see a skin if you wait a bit after the rake. Don't
                chase the last crystals into the dirt. You can leave a
                line for tomorrow. Maybe cover the corner the gulls like?
                """,
            ),
            _b(
                "twine",
                "salt",
                """
                You'll walk the east table the same way. Don't scrape the
                board if it is a bit damp. You can leave the last skin.
                Maybe that is enough for the light you have?
                """,
            ),
        ],
    ),
    _d(
        29,
        "skiff-eel-roll-hop-skiff-willow",
        "return",
        "ABA: Skiff eel, Roll hop, Skiff willow",
        [
            _b(
                "skiff",
                "eel",
                """
                I fix the mouth with a new hoop. I don't like how it sat
                overnight. I'll try it empty once and I'll watch the hang.
                So I keep the old hoop for scrap.
                """,
            ),
            _b(
                "skiff",
                "eel",
                """
                I talk to the dog and I ignore the road. I don't need
                company on the bank. I'll finish this splice and I'll go.
                Then I rinse my hands in the slack.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                The committee shall hear the kiln report in closed session.
                Members were told that the late garden was still wet. It was
                resolved that picking must wait. The clerk shall notify the
                gangs.
                """,
            ),
            _b(
                "roll",
                "hop",
                """
                The fans were run overnight. The committee must confirm the
                power cost. It was noted that one belt was glazed. Members
                shall not start the press until the loft was cleared.
                """,
            ),
            _b(
                "skiff",
                "willow",
                """
                I walk the withy bed after the meeting because I need quiet.
                I don't take their minutes with me. I'll cut a few ties and
                I'll sit on the stool. So I remember what my hands are for.
                """,
            ),
            _b(
                "skiff",
                "willow",
                """
                I bundle the thin rods for the garden. I don't sell those.
                I'll peel one to see the cream and I'll stop there. Then I
                lock the gate and I go home along the ditch.
                """,
            ),
        ],
    ),
    _d(
        30,
        "four-house-collage",
        "collage",
        "Flint salt, Brine peat, Twine kiln, Vellum millrace",
        [
            _b(
                "flint",
                "salt",
                """
                Dawn 05:02. Wind 15 kn, E. Brine 24.0 Be. Rake 1, 14 m.
                Bags filled: 3 at 25 kg.
                """,
            ),
            _b(
                "brine",
                "peat",
                """
                A stack shall be capped on a dry day only. Turves must not
                be laid on standing water. The inspector shall halt the work
                if rain begins. Tools shall be removed from the face.
                """,
            ),
            _b(
                "twine",
                "lime",
                """
                You'll want a smaller charge if the wind is this hard, maybe
                half of what you'd planned. Don't fight it; you can wait a
                bit. Your smoke will tell you if you're winning. Can you
                live with a short day?
                """,
            ),
            _b(
                "vellum",
                "millrace",
                """
                We ought to end a collage the way we end a survey: by
                admitting that four dialects have been asked to share one
                page. One therefore does not blend them. However convenient
                a summary would be, the useful fact is the seams. This does
                not require a fifth voice.
                """,
            ),
        ],
        holdout=True,
    ),
]


def changes_for(doc: Document) -> list[int]:
    houses = [block["house"] for block in doc["blocks"]]
    return [0 if a == b else 1 for a, b in zip(houses, houses[1:])]


def authors_for(doc: Document) -> int:
    return len({block["house"] for block in doc["blocks"]})


def holdout_ids() -> list[int]:
    return [doc["ident"] for doc in DOCUMENTS if doc["holdout"]]
