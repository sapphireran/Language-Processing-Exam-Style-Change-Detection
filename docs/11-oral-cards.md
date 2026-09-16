# Oral cards

Short prompts. Answer in four to eight sentences, then stop.

## Card 1 — Define the task

*Prompt:* What is intrinsic style-change detection?

*Aim:* One document, no candidates, find author seams. Paragraph
atoms, binary boundaries, F1. Contrast with attribution and
verification. Mention why 2023 split easy / medium / hard.

## Card 2 — Closed class

*Prompt:* Why do function words beat nouns here?

*Aim:* Frequent, weakly referential, reusable across topics.
Mosteller–Wallace as the citation. Nouns track aboutness. Hard band
as the test.

## Card 3 — Delta

*Prompt:* Explain Burrows' Delta as if I have not read the paper.

*Aim:* Relative frequencies, z-score, mean absolute difference.
Original use is attribution. We use it on adjacent paragraphs. Say
the adaptation out loud.

## Card 4 — n-grams

*Prompt:* Why character 3-grams on 80-word paragraphs?

*Aim:* Denser histogram than words; punctuation and morphology;
failure on named entities and tiny notes.

## Card 5 — Topic

*Prompt:* Your easy F1 is 0.91 and your hard F1 is 0.44. Diagnose.

*Aim:* Topic confound. Embeddings and content words. Hygiene:
closed class, stratified reporting, same-topic synthetic tests.

## Card 6 — Metrics

*Prompt:* Why not accuracy?

*Aim:* Class imbalance toward 0. Always-same dummy. F1 on the
positive "change" class. Macro vs micro.

## Card 7 — CUSUM

*Prompt:* A policeman shows you a kinked sentence-length plot.

*Aim:* Exploratory only. Genre, quotes, lists kink too. Would not
testify. Would evaluate as one feature with labelled F1.

## Card 8 — Transformers

*Prompt:* Why is there no BERT in this repository?

*Aim:* Exam kit, no GPU, no PAN dump. Pair classifier would be the
production model. Stylometry remains the explainer and the baseline.
Easy-band scepticism.

## Card 9 — Gift authorship

*Prompt:* How would you hunt a gift-authored abstract?

*Aim:* Hard-band geometry: same paper, different register. Look at
hedges, `we` vs `I`, nominalisations, citation scaffolding. Do not
claim you identified the professor.

## Card 10 — Error analysis

*Prompt:* Show me one false alarm and one miss you expect.

*Aim:* False alarm: single author switches from list to prose.
Miss: two careful academic writers on one topic. Point at corpus
items 01 and 04.

## Card 11 — Calibration

*Prompt:* Where does 0.55 come from?

*Aim:* Development sweep or an intra-document median+MAD rule. Not
theory. Accuracy peak ≠ F1 peak. Tiny corpus ⇒ demo, not leaderboard.

## Card 12 — Output contract

*Prompt:* What does PAN want on disk?

*Aim:* `problem-X.txt` in, `solution-problem-X.json` with
`{"changes":[...]}` out. Length \(k-1\). `newline=""`. TIRA-style
`-i` / `-o`.
