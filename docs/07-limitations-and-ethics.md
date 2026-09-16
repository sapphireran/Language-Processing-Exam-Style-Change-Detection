# Limitations and ethics

## What a distance cannot prove

A high style distance is evidence of a **distributional shift** in
habits. It is not a name, a motive, or a legal identity. Two paragraphs
can diverge because:

- the writer switched genre (mail → method section)
- the writer got tired, edited, or used a template
- a copy-editor rewrote one span
- the topic changed and your “style” features leaked content
- the spans are too short for the rates to exist

An exam answer that says “therefore paragraph 4 was written by a second
person” has overclaimed. The correct modal is: the boundary is
consistent with a change of author *or* a change of register.

## Short text is the central statistical limit

Paragraph-level PAN problems are already short. Sentence-level versions
are worse. Relative frequencies of 70 function words on 25 tokens are
mostly zeros. That sparsity is why character n-grams and neural
encoders get used, and why they re-import topic.

## Topic leakage is an ethical issue as well as a metric one

If a detector flags “the science-y paragraphs” as a different author,
it will systematically accuse the collaborator who wrote the method
section. Gift-authorship detection, one of the advertised use cases,
then becomes genre detection. Always show Hard (same topic) before you
talk about academic integrity.

## Forensic and classroom misuse

Possible uses people actually cite:

- intrinsic plagiarism screening
- gift-authorship or ghost-authorship hypotheses
- writing-support tools (“your tone jumped here”)
- multi-author document navigation

Misuses:

- treating a score as proof in a disciplinary hearing
- running the tool on exam scripts to “catch collusion” without a
  validation set in that genre
- deanonymising anonymous speech by stitching style with other signals

If you would not defend the false-positive rate in front of the accused
person, do not ship the number.

## Dual use and this repository

This repo is exam notes plus a transparent baseline. It does not include
a trained author-identification model, a scraping pipeline, or anyone
else’s writing. The synthetic documents exist so you never have to paste
a classmate’s essay into a detector to learn the math.

## Dual authorship is normal

Academic papers, software docs, and group projects are supposed to be
multi-author. A style change can be a *healthy* seam: methods written
by the experimenter, discussion written by the theorist. Detection
without a social context is not a moral finding.

## What to write in a 6-line ethics paragraph

1. Intrinsic ≠ identification.
2. Features leak topic unless you ablate them.
3. Short spans make scores unstable.
4. False positives harm more than false negatives in disciplinary use.
5. Validate in-genre; do not transfer a Reddit-trained cut-off to theses.
6. Prefer assistive display (“this boundary is unusual”) over binary
   accusations.
