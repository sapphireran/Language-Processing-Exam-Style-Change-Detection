# References and further reading

Personal reading list for the exam topic. None of these texts are
redistributed in this repository.

## Shared-task overviews (format and problem history)

- PAN / CLEF multi-author writing-style analysis task pages (2018–2025).
  Useful for the I/O contract, the move from document-level “single vs
  multi” to paragraph-level changes to sentence-level changes, and the
  later emphasis on topic control.
- Zangerle et al., overview papers for recent PAN style-analysis editions.
  Read for dataset construction (topical homogeneity as difficulty) and
  for the official macro-F1 protocol.

## Stylometry textbooks and handbook chapters

- Holmes, “The evolution of stylometry in humanities scholarship”
  — short history; good for a “what is style?” paragraph.
- Juola, *Authorship Attribution* — the standard compact survey of
  extrinsic tasks; use it to contrast with the intrinsic setting.
- Stamatatos, “A survey of modern authorship attribution methods”
  — feature families (function words, char n-grams, punctuation).
- Koppel, Schler, Argamon — unmasking and the idea that *difference*
  can be more stable than a writer’s absolute profile.

## Change-point and intrinsic analysis

- Papers on intrinsic plagiarism detection (usually paragraph or
  sliding-window style divergence, often cosine on char n-grams).
  The unsupervised detector in this repo is a stripped classroom version
  of that idea.
- Sequence-labelling treatments (CRF / BiLSTM over sentence pairs) from
  later shared-task notes. Mention these if asked how to drop the
  independence assumption of pairwise logistic regression.

## Evaluation

- Any standard IR/ML note on macro vs micro F1. You need the two-class
  special case, not the 20-class named-entity case.
- The PAN evaluator repositories (macro-F1 on concatenated pair labels).
  Compatible in spirit with `stylechange.evaluate`.

## Ethics

- Writing-assistance and ghost-authorship discussions in research-integrity
  codes. The tool can flag a seam; it cannot name a guilty person.
- Short-text reliability: do not treat a 4-sentence “detection” as
  evidence in an accusation.

## What this repo is not citing

No employer internal docs. No proprietary datasets. No scraped dumps
shipped as “examples”. If you add a dataset later, put the licence next
to it and keep it out of `data/synthetic/` so the original study set
stays small and clean.
