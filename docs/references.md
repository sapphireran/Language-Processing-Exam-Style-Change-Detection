# References (short list)

Personal exam reading, not a paper dump. Prefer the surveys and the
task overviews; skim methods papers only for the feature list.

## Shared task (the exam’s public cousin)

- PAN / CLEF multi-author writing style analysis and style change
  detection overviews, 2018–2025 (Zangerle and co-authors). Paragraph
  vs sentence granularity, and the Easy / Medium / Hard topic control,
  are defined there.
- Task page (2023 edition, closest to this repo’s I/O):
  <https://pan.webis.de/clef23/pan23-web/style-change-detection.html>

## Classical stylometry

- Mosteller, F. and Wallace, D. L. *Inference and Disputed Authorship:
  The Federalist.* Function-word rates as authorship evidence.
- Burrows, J. “Delta”: a distance over function-word z-scores. Still
  the right one-line “classical baseline” in an exam.
- Stamatatos, E. survey papers on authorship attribution. Use these
  for the taxonomy (intrinsic / extrinsic, instance-based /
  profile-based).

## Style vs topic

- Argamon and others on register / systemic-functional cues
  (pronouns, hedges, nominalizations). The casualness axis in this
  repo is a toy version of that idea.
- Work on topic confound in authorship (including later PAN editions
  that explicitly built Hard sets). If you only remember one sentence:
  **do not quote an Easy F1 as a style result.**

## Evaluation

- Any IR / NLP textbook chapter on precision, recall, F1, and
  macro-averaging. The empty-positive convention used here is the
  same one scikit-learn calls `zero_division=1` if you set it that
  way — say it explicitly.

## Ethics

- Forensic linguistics primers on what stylometry can and cannot
  swear to in court. The six-line version is in
  [07-limitations-and-ethics.md](07-limitations-and-ethics.md).

This repository does not vendor PDFs or shared-task data.
