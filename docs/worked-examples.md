# Worked examples

All eight files live in `examples/documents/`. Gold labels are locked
by `tests/test_detector_examples.py`. Walk one of them with:

```bash
python examples/explain_document.py examples/documents/problem-exam-takehome.txt
```

## easy-kitchen-and-syntax

Nine sentences, two cuts.

1. Three recipe lines (`chuck`, `Don't`, `yeah`, `I`). Voices: chat,
   chat, student. Same **personal** band, so no cut yet.
2. Three syntax-textbook lines. Voice jump personal → textbook.
3. Three CFG productions (`S -> NP VP`). Voice jump textbook → notes.

Topic *and* register move. A bag-of-nouns baseline would also get this
one; that is why it is called easy.

## medium-embeddings

Six sentences, one cut, **same topic** (word embeddings).

- Three student lines (`I keep`, `I expect`, `I think`)
- Three academic lines (`Distributional semantics…`, `therefore`)

If the middle student sentence forgets to say *I*, the voice classifier
briefly calls it textbook. `merge_singleton_runs` absorbs that blip so
we do not emit two fake cuts around one sentence.

## hard-we-vs-one

Six textbook sentences, one cut, **same topic and same named voice**.

- Left: *we / our / therefore / moreover*
- Right: *one may / subsequently / consequently*

Every unit is classified `textbook`. The cut is a **span** cut on
binary register flags, not a voice jump. This is the document to put on
the projector if someone asks "what do you do when register does not
change?"

## exam-takehome

Ten sentences, two cuts. The story the repo is named after:

| lines | what it is pretending to be |
| --- | --- |
| 1–3 | a student revising HMMs (`I still get lost`, `For me`, `I think`) |
| 4–7 | a pasted textbook block on CRFs |
| 8–10 | lecture shorthand (`CRF:`, `Z(x):`, `train:`) |

`--explain` should print `CHANGE (voice)` at the two joins and `same`
everywhere else.

## single-author

Six morphology-textbook sentences, **zero** cuts. This is the negative
control. If a change-point on mean word length is left in the metric,
this file is the first to break.

## paragraph-gift

The take-home story again, but as three blank-line paragraphs. Gold
`changes` is `[1, 1]`. This is the PAN 2023 shape (paragraph pairs).

## questions-vs-exposition

Three Socratic questions (`What` / `Why` / `Can`) then three
declarative LM definitions. Same topic, chat → textbook.

## notes-after-prose

Four parsing-textbook sentences, then four labelled notes
(`trans:`, `oracle:`, `feat:`, `dev:`). Close topic; the cut is
textbook → notes. The notes block is not carved into further authors.

## Reading a miss

If a new file comes out wrong, run:

```bash
stylechange detect path/to/problem.txt --explain --debug-voices
```

`--debug-voices` prints the four raw scores per unit. Most mistakes are
either a unit sitting on the wrong side of the chat/student/textbook
margin, or a span threshold that is too eager. Do not "fix" a miss by
editing the gold file to match the bug.
