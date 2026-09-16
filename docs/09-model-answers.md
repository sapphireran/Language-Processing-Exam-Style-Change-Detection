# Model answers

Short answers. Expand any of them into a ten-line oral paragraph.

1. Input: one document. Output: a binary vector of length
   `n_paragraphs - 1` saying whether authorship changes between each
   neighbouring pair.

2. No external author corpus is supplied at test time. All evidence
   comes from variation inside the document.

3. Changes only at paragraph boundaries; each paragraph has one
   author.

4. Attribution names an author against a gallery. Style-change
   detection only finds the cuts.

5. Extrinsic plagiarism compares the text to a reference collection.
   Intrinsic style change looks for an internal inconsistency when
   no source is known.

6. 2018 was document-level single vs multi; 2020 added paragraph
   flags; 2021 asked for author labels; 2022 went to sentences; 2023
   returned to paragraph flags but controlled topic.

7. To stop systems from solving authorship with topic. Hard ≈ same
   topic, so style has to do the work.

8. Reddit posts from discussion-heavy subreddits, cleaned of
   markdown and links, then shuffled by semantic *and* stylistic
   similarity. Informal web English, not edited books.

9. Documents are concatenations of several users. Official output is
   only adjacent bits, so A-B-A and A-B-C are indistinguishable from
   the label alone.

10. Frequent, closed-class, topic-light, hard to fake consistently.

11. They operate on raw characters, so hyphenation, contractions, and
    morphology still leave a trace.

12. Contraction rate; `I` vs `one`; `however` / `therefore` rate.

13. Almost every token is unique, so TTR ≈ 1 for every author.
    Dampen by `sqrt(n)` or do not use TTR on short spans.

14. \(d = 1 - (x\cdot y)/(\|x\|\|y\|)\).

15. Mean absolute difference of z-scored function-word frequencies.
    Here the z-scores use the other paragraphs of the same document.

16. Split paragraphs; fingerprint each; score adjacent pairs; apply a
    threshold / vote rule; emit bits.

17. There is always a largest distance. Without a hard floor, that
    pair becomes a false alarm.

18. Cluster paragraphs (agglomerative, HMM, reassignment after the
    cuts) and allow non-contiguous spans to share a label.

19. Fine-tuned transformers (DeBERTa-v3, contrastive or NLI heads)
    trained on the official pairs.

20. \(S_t = S_{t-1} + (x_t - \bar x)\). A new slope means the local
    mean has moved: a candidate author change.

21. Most boundaries in a long single-author stretch are zeros.
    Always predicting 0 looks accurate and is useless.

22. Macro: unweighted mean of per-document F1. Micro: pool every
    boundary first. Macro gives short documents equal say.

23. TP=1, FP=1, FN=1 → P=0.5, R=0.5, F1=0.5.

24. Report 1.0 by the "no positives, no false alarms" convention used
    here and in several student notes. State the convention.

25. The system is using topic (or subreddit) leakage. It has not
    learned style.

26. Pretraining and fine-tuning both see lexical semantics. Named
    entities and thread-specific jargon become features.

27. Gift authorship on a paper; a ghost-written chapter in a thesis.

28. Short paragraphs; two academic voices; thresholds fit to the
    bundled set; CUSUM confused by A-B-A-B alternation.

29. Formality is high *and stable*. The ensemble looks at jumps, not
    at "is this formal?".

30. A cheap POS tagger or a small contrastive encoder. It would still
    miss two similar academics on one topic, and it would still leak
    topic on the easy split if you are not careful.
