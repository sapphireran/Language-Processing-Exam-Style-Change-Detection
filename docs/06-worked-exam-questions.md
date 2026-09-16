# Worked exam questions

Answers are written at the level expected in a closed-book language
processing exam. Numbers you can recompute with the library are marked
**checkable**.

---

## Q1. Formalise the output

**Prompt.** A document has paragraphs \(p_1\ldots p_5\). Authors are
A, A, B, B, A. Write the gold change array and the number of authors.
Is the last `1` a mistake?

**Answer.** Boundaries: AA, AB, BB, BA → `[0, 1, 0, 1]`. Authors = 2
(A returns). The last 1 is required: a return is still a change. The
task does not ask you to say “this is the same A as paragraph 1”.

---

## Q2. Intrinsic vs extrinsic

**Prompt.** In at most four sentences, contrast intrinsic style change
detection with authorship attribution. Give one application that
*requires* the intrinsic setting.

**Answer.** Attribution compares a questioned text to named candidate
authors who have already supplied writing samples (extrinsic). Style
change detection looks only at variation *inside* one document and
emits boundary labels, not names. It is required when you suspect
unattributed contribution or plagiarism but have no comparison corpus
— the intrinsic-plagiarism / gift-authorship setting. Using an
attribution model here would be answering a different question.

---

## Q3. Type–token ratio by hand  **checkable**

**Prompt.** Compute TTR for each line. Is the comparison fair?

```
A: The cat sat on the mat. The cat was sad.
B: I can't even. This is just wild, honestly.
```

**Answer.**

Tokenise with the exam convention (lowercase, keep internal
apostrophes, split on whitespace/punctuation):

- A tokens (10): `the cat sat on the mat the cat was sad`
  types (7): `the, cat, sat, on, mat, was, sad`
  TTR = \(7/10 = 0.70\)
- B tokens (8): `i can't even this is just wild honestly`
  types (8): all unique
  TTR = \(8/8 = 1.00\)

The comparison is **not** fair as evidence of style. B is shorter, so
TTR is inflated. Also B’s higher TTR is partly “fewer repeated
function words”, which *is* stylistic, and partly length. In the
baseline, TTR is inspected but not put into the distance for this
reason.

Check:

```bash
PYTHONPATH=src python - <<'PY'
from stylechange.features import extract_profile
a = extract_profile("The cat sat on the mat. The cat was sad.")
b = extract_profile("I can't even. This is just wild, honestly.")
print(a.scalars["type_token_ratio"], a.n_tokens)
print(b.scalars["type_token_ratio"], b.n_tokens)
PY
```

---

## Q4. Function-word cosine by hand  **checkable**

**Prompt.** Restrict the vocabulary to `{the, a, i, of}`. Compute cosine
similarity of the two count vectors, then cosine distance.

```
P: I saw the cat of the neighbour.
Q: The theory of the aether was a curiosity and a myth.
```

**Answer.**

Counts on the restricted vocab:

|  | the | a | i | of |
| --- | --- | --- | --- | --- |
| P | 2 | 0 | 1 | 1 |
| Q | 2 | 2 | 0 | 1 |

\[
P\cdot Q = 2\cdot2 + 0\cdot2 + 1\cdot0 + 1\cdot1 = 5
\]
\[
\|P\| = \sqrt{4+0+1+1}=\sqrt{6}
\quad
\|Q\| = \sqrt{4+4+0+1}=\sqrt{9}=3
\]
\[
\cos = 5 / (3\sqrt{6}) \approx 0.680
\quad
d = 1-\cos \approx 0.320
\]

P is first-person and concrete; Q is nominal and definite-article
heavy. Even on four dimensions the habit shift is visible. Content
words (`cat`, `aether`) were ignored on purpose.

---

## Q5. Why accuracy is the wrong headline

**Prompt.** Gold `[0,0,1,0,0]`, system `[0,0,0,0,0]`. Compute accuracy,
precision, recall, F1 with the conventions of these notes. Which number
would you quote and why?

**Answer.** TP=0, FP=0, FN=1, TN=4.

- acc = 4/5 = 0.80
- P = 1 (no predicted positives; empty-precision convention)
- R = 0/1 = 0
- F1 = 0

Quote F1 (and mention the missed change). Quoting accuracy congratulates
a system that never fires. See `tests/test_evaluate.py`.

---

## Q6. Design a topic-leakage experiment

**Prompt.** You suspect your neural pair classifier is solving Easy by
topic. Design a three-step experiment that would convince a sceptic.

**Answer.**

1. **Ablation.** Retrain after masking or hashing content words (keep
   function words, punctuation, and morphology). If Easy F1 collapses
   and Hard barely moves, the model was using topic.
2. **Control set.** Evaluate on Hard (same topic, style-only) and on
   single-author documents that *do* change topic (a writer who
   digresses). Topic-driven models light up the digression; style
   models should not.
3. **Swap test.** Inside Easy documents, replace nouns in paragraph
   \(i+1\) with nouns from paragraph \(i\) while leaving function words
   and syntax. If predicted changes vanish, the decision was topical.

The repo already ships step 2 in miniature: compare
`stylechange.topic.topic_distance` against combined style distance on
`examples/data/easy/problem-001.txt` vs `examples/data/hard/problem-001.txt`.

---

## Q7. Threshold vs clustering for A–B–A

**Prompt.** Paragraph authors are A, B, A. What do a pairwise threshold
and a 2-means clustering each output? Which is “more correct”?

**Answer.** Gold changes = `[1, 1]`. A pairwise threshold that works
will emit `[1, 1]`. 2-means should recover clusters {1,3} and {2}, and
the induced change array is also `[1, 1]`. Both are correct for *this*
task. Clustering additionally claims that paragraph 3 is the same author
as paragraph 1 — extra information the official output does not require
and that you should not invent if the clusters are unstable.

---

## Q8. Pick features for Hard

**Prompt.** List four features you would keep and two you would drop for
the Hard split. One sentence each.

**Answer. Keep:** contraction rate (habit, low topic); first vs second
person (register); semicolon / hedge rates (academic vs instructional);
function-word cosine (classic stylometry). **Drop:** content TF–IDF
(topic by definition); raw TTR (length artefact on short Hard
paragraphs). Optional drop: unmodified transformer embeddings, unless
you have shown they survive the ablation in Q6.

---

## Q9. Off-by-one

**Prompt.** A system writes `changes: [0, 1, 0, 1]` for a document whose
`split_paragraphs` returns 4 strings. What happened, and what F1 will a
strict evaluator give?

**Answer.** Four paragraphs ⇒ three legal boundaries. The system labelled
paragraphs (or included a dummy). A strict scorer rejects the file
(`ValueError` in this repo) or scores it as zero. Fix the contract
before retuning \(t\).

---

## Q10. Ethics in six lines

**Prompt.** A department wants to run your detector on theses to “flag
ghost-written chapters”. Write the advice.

**Answer.** A style jump is not an identity. Thesis chapters *should*
change register (literature review ≠ methods). Any system trained on
social-media Easy data will fire on that genre shift. False positives
here are disciplinary accusations. If they insist, report a highlighted
distance track for the student to inspect, never a binary “ghost”
label, and validate on in-genre single-author theses first. See
[07-limitations-and-ethics.md](07-limitations-and-ethics.md).

---

## Q11. Compute a combined distance sketch

**Prompt.** Suppose \(d_{\text{scalar}}=0.40\), \(d_{\text{fw}}=0.20\),
\(d_{\text{3g}}=0.50\), \(d_{\text{punct}}=0.10\), weights
(0.55, 0.25, 0.10, 0.10). Combined distance? Decision at \(t=0.33\)?

**Answer.**

\[
0.55\cdot0.40 + 0.25\cdot0.20 + 0.10\cdot0.50 + 0.10\cdot0.10
= 0.220 + 0.050 + 0.050 + 0.010 = 0.330
\]

That is exactly the default cut-off. A careful implementation uses `>`
not `>=`, so this boundary is **no change**. Off-by-epsilon questions
are fair game; state the inequality.

---

## Q12. Read a live document  **checkable**

**Prompt.** For `examples/data/easy/problem-001.txt`, write the gold
array and explain in two sentences why a topic-only model and a
style-only model both get the same `1` in the middle.

**Answer.** Gold `[0, 1, 0]`. Paragraphs 1–2 are leftover pasta in a
casual first-person voice; 3–4 are sidewalk design in a formal civic
voice. A topic model fires because pasta tokens do not overlap
sidewalk tokens (topic distance 1.000 at the middle boundary). A style
model fires because contractions, `I`/`you`, and short sentences give
way to nominalizations and long words (combined style distance 0.528
versus 0.251 / 0.223 on the same-author sides). They agree on Easy for
different reasons; they will not agree on Hard.

Run:

```bash
PYTHONPATH=src python -m stylechange.cli inspect examples/data/easy/problem-001.txt
```
