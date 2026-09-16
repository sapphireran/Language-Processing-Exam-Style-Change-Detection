# Error taxonomy

I want a list of misses I am willing to own. A detector that only
fails on other people's documents is a story, not a method.

## False negatives I expect

- **Hard workshop pairs.** Two pewtersmiths, two thatchers, two
  cave-agers. Same nouns, both first person, both competent. If
  function-word profiles overlap, Quoin will shrug. That is the hard
  band doing its job.
- **Short second houses.** Menu fragments and safety bulletins are
  short on purpose. NCD becomes wrapper noise. If the 3-gram channel
  also starves, the hinge stays dark.
- **Polite complaint versus log.** A complaint that cleans itself up
  (full sentences, few slang tokens) will drift toward the log voice.

## False positives I expect

- **Trap files, if I get greedy.** A compositor writing about a
  bicycle still changes nouns. Character 3-grams will move. If I
  raise the n-gram weight, I will start marking topic as authorship.
- **Author return.** A versus A with a clerk in the middle: the two
  A paragraphs are not adjacent, so the return itself is fine. The
  risk is marking *inside* A because the second A paragraph has
  started talking about the notice.
- **Collage of short houses.** Four voices in four short paragraphs
  can look like one messy voice to zlib.

## Errors I treat as bugs, not as genre

- wrong-length `changes` array
- a control document that lights up every hinge
- a press-then-notice file that stays entirely dark
- F1 of 0 on a document whose gold is all zeros and whose pred is
  all zeros (the `safe_f1` clause was forgotten)

The last one is a scoring bug. I have written it down so I do not
"debug the detector" when the metric is the thing that broke.

## What I will say if they ask for an error analysis

I will pick one hard miss and one trap false-positive (if I have one
on the live run), show the channel table from `quoin explain`, and
say which channel was loudest. That is the whole analysis. I will not
invent a neural attention map.
