# Ninety-second oral

Memorise a version of this, then throw it away and say it in your
own words.

> Style-change detection asks, for each pair of neighbouring
> paragraphs, whether the author changed. It is intrinsic: there is
> no gallery of suspects. PAN 2023 emits a binary vector and scores
> macro-F1, with three topic-controlled difficulties so that a
> topic model cannot hide on the easy set.
>
> A classical system builds a fingerprint per paragraph — function
> words, character 3-grams, sentence length, register — and looks
> for a jump. I use Burrows's Delta on function words and cosine on
> 3-grams, plus a formality score so that Slack versus minutes is
> obvious. I vote: two weak channels or one strong channel.
>
> Transformers win the shared task. I still start from stylometry
> because I can compute it on paper and I can show, on a circadian
> text with two academic voices, that topic Jaccard stays high while
> Delta moves. That is the distinction the hard split is for.
>
> Limitations: short paragraphs, similar academics, and thresholds I
> set on my own examples. I would not claim a PAN number.

## If they interrupt

- **Why not BERT from the start?** "I can, and I would for a
  submission. I wanted a method I can derive."
- **Is formality style?** "It is register, which is part of the
  habitual fingerprint. It is not literary style."
- **A-B-A?** "The official bits cannot name the returning author.
  I would cluster."
- **Function-word list?** "Closed-class inventory; I can add or
  drop items. The idea matters more than my 80 words."
- **Single-author F1?** "I treat all-zero / all-zero as 1. I will
  say so in the write-up."
