# Intrinsic vs extrinsic

Keep the two families separate. Examiners like a clean contrast.

## Extrinsic

You have a questioned document *and* a set of candidate writers, each with known text. Verification ("is this A or not-A?") and attribution ("which of these n?") live here. Features can be trained against the candidate set. Closed-class Delta was built for this world: z-score a questioned text against a reference corpus.

## Intrinsic

You have only the questioned document. Style-change detection, author diarization inside one file, and "is this multi-authored at all?" live here. There is no reference corpus of the *same* writers. Any z-score you compute is against the document's own units, which is noisy when the document is short.

HingeMark is intrinsic. Intra-document Delta z-scores function words across the eight sentences of problem-13. That is a diagnostic, not a biography of Quist.

## Why people mix them up

A pairwise hinge score *looks* like verification: "are these two sentences the same writer?" It is verification without a known writer. The negative class is "someone else, unknown." You cannot say *who*.

Diarization (cluster units into writer spans) is the natural next step. The official `changes` array is a poorer cousin: it only marks the cuts. Problem-22 is the counter-example that keeps you honest.

## Exam sentence

> Extrinsic tasks compare a questioned text to named candidates. Intrinsic tasks, including style-change detection, see only the questioned text. A hinge classifier is intrinsic verification: same-or-different, no names.
