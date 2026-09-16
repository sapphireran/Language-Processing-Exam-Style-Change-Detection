# Question bank

Answer these on paper first. Model answers are in
[09-model-answers.md](09-model-answers.md).

## Definitions

1. Give the input and output of paragraph-level style-change detection.
2. Why is the task called intrinsic?
3. State the two modelling assumptions about paragraphs.
4. Distinguish style-change detection from authorship attribution.
5. Distinguish it from extrinsic plagiarism detection.

## History and data

6. Name three ways the PAN task changed between 2018 and 2023.
7. What is the point of the easy / medium / hard splits in 2023?
8. Where did the 2023 paragraphs come from, and why does that matter?
9. Why can an author return later, and why do the official labels
   not name them?

## Features

10. Why are function words used as style features?
11. Why are character n-grams robust to tokenisation arguments?
12. Give two features that measure register rather than topic.
13. Why is raw type–token ratio misleading on a 20-word paragraph?
14. Write the formula for cosine distance between two count vectors.
15. Write Burrows's Delta and say what the reference sample is in
    this kit.

## Methods

16. Sketch an unsupervised pairwise detector in four steps.
17. Why can a z-score of adjacent distances invent changes in a
    single-author document?
18. How would you recover a returning author if PAN asked?
19. What did the 2023 winning systems do that this kit does not?
20. CUSUM: write the recurrence and interpret a slope change.

## Evaluation and critique

21. Why is accuracy a poor headline metric here?
22. Macro-F1 vs micro-F1 on a collection of documents.
23. Gold `[1,0,1]`, pred `[1,1,0]`. Compute P, R, F1.
24. Gold `[0,0,0]`, pred `[0,0,0]`. What F1 should you report, and
    why is that a convention?
25. A system scores 0.91 easy and 0.54 hard. Diagnose it.
26. Why might a transformer still be a topic model?
27. Give two real-world applications that do not look like Reddit.
28. List three failure modes of the ensemble in this repo.
29. The landlord letter is first person and formal. Why should the
    detector *not* flag it?
30. If you could add one feature, what would it be and what would it
    still miss?
