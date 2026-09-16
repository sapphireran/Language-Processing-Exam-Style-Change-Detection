# Exam handbook

Personal study notes for a Language Processing oral and written exam
on **intrinsic style-change detection**. They follow the public PAN
2023 multi-author writing-style analysis contract (paragraph pairs,
binary `changes`, F1) but they do not ship PAN data.

Read in this order if you have one sitting:

1. [What the task actually asks](01-task-and-pan-format.md)
2. [Intrinsic vs extrinsic authorship](02-intrinsic-authorship.md)
3. [Feature families you can defend](03-feature-families.md)
4. [Delta and character n-grams](04-delta-and-ngrams.md)
5. [CUSUM as a visual, not a verdict](05-cusum.md)
6. [Why topic is a confound](06-topic-confound.md)
7. [Metrics and dummy baselines](07-metrics-and-baselines.md)
8. [Threshold calibration](08-calibration.md)
9. [What to say about transformers](09-transformers-vs-stylometry.md)
10. [Worked walkthrough](10-worked-walkthrough.md)
11. [Oral cards](11-oral-cards.md)
12. [Written model answers](12-written-answers.md)
13. [Failure modes](13-failure-modes.md)
14. [Formula sheet](14-formula-sheet.md)

The runnable companion is the `splicefind` package and the original
documents under `examples/corpus/`.
