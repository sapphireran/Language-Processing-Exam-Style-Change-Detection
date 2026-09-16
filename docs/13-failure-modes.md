# Failure modes

Memorise one row per family. The oral loves "when does this break?"

| Situation | What the features see | Typical error | Corpus exhibit |
|-----------|-----------------------|---------------|----------------|
| Single author, one topic | Small jitter | False alarm if threshold is greedy | `problem-01-allotment` |
| Same author, new topic | Nouns and some 3-grams jump | False alarm for content models | `problem-16-tomato-then-train` |
| Two authors, one topic | Weak open-class gap | Miss | `problem-04-tidally-locked` |
| Notes then prose, one person | Sentence length and punctuation explode | False alarm | `problem-08-minutes-then-chat` is two people; `problem-09-dino-book` is the cleaner two-register case |
| Quoted table or list | Digits, fragments | False alarm | `problem-13-patch-notes` (two people by design; same geometry) |
| Gift abstract | Hedges, `we`, nominalisations | Should hit; may miss if both writers are academic | `problem-05-gift-abstract` |
| Very short paragraph | Every rate is a coin flip | Either way | `problem-15-collage` fragments |
| Shared boilerplate | 3-grams glue authors together | Miss | legal `hereby` / `regarding` in `problem-14` if both sides used it |
| Editor homogenised the text | Features flattened | Miss | not in corpus; say it anyway |
| Code-switch or second language | Length and 3-grams jump | Change, but maybe not *author* | out of scope; flag it |

## Things this toolkit will never do

- Name the authors.
- Recover a plagiarism source.
- Tell a court that a kinked CUSUM is proof.
- Download the PAN Reddit collection.
- Replace a properly trained pair classifier on a large labelled set.

If you cannot say those five sentences, the rest of the handbook is
decoration.
