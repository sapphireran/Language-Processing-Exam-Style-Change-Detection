# Stylometry used in this toolkit

Style markers are habits that stay when the subject changes: how long
the sentences run, whether the writer says `don't` or `do not`, how often
`I` appears, how many commas decorate a clause. None of them is
authorship by itself. Together they are a fingerprint of register plus
idiosyncrasy, which is the signal intrinsic detection actually has.

This file is the feature list I want to be able to write from memory,
plus why each family is in the code.

## 1. Lexical richness

| Feature | Intuition |
| --- | --- |
| Type-token ratio | Vocabulary variety. Inflates on short texts. |
| Hapax ratio | Share of types that occur once. |
| Yule's K | Vocabulary concentration; less enslaved to length than TTR. |
| Honoré's R | Rewards hapax-heavy vocabularies. |

These move when a chatty paragraph sits next to a memo full of repeated
technical nouns. They also twitch on paragraph length, so the detectors
z-score columns *inside the document* before taking cosine distance.

## 2. Length and rhythm

- Average and standard deviation of word length
- Average and standard deviation of sentence length
- Long-word rate (≥ 7 characters)
- Short-word rate (≤ 3 characters)
- Vowel-group proxy for syllable-ish complexity

Author A in `easy/problem-001` leans on short words and uneven
sentences. Author B leans on longer Latinate tokens and steadier
sentence length. You can see that in the feature table without reading
the prose.

## 3. Punctuation

Comma, period, question, exclamation, semicolon, colon, dash, and quote
rates are all counted per character so paragraph length does not
dominate. Commas per sentence is kept as a separate complexity proxy.

Punctuation is cheap and surprisingly author-specific. It is also genre
specific, which is why it helps on easy documents and can overfit
register on hard ones.

## 4. Closed-class words

Function words (`the`, `of`, `however`, pronouns, auxiliaries) are the
classic stylometric bet: they are frequent, they are weakly bound to
topic, and people do not monitor them. The toolkit tracks:

- overall function-word rate
- personal pronouns and first person
- articles and prepositions
- hedges (`maybe`, `perhaps`, `seems`)
- intensifiers (`very`, `really`, `extremely`)
- connectives (`therefore`, `moreover`, `however`)

`src/style_change/lexicons.py` is intentionally short. An exam answer
should name the category and a few examples, not recite 400 stopwords.

The `function_word` detector goes further than rates: it builds a
distribution over the whole list and compares adjacent paragraphs with
Jensen–Shannon divergence. That is closer to the “who prefers *which*
and *of*” view of authorship than a single pronoun percentage.

## 5. Surface habits

- Contraction rate (`don't`, `I'm`)
- Uppercase word rate (a rough named-entity / shouting proxy)
- Digit rate

Contractions alone almost separate author A from author B in the first
easy document. Digits help when one writer cites quantities and the
other does not. They are not magic on the hard split.

## 6. Character 3-grams

Word lists miss morphology, spelling, and punctuation sequences.
Character 3-grams do not. The `char3` detector builds a normalized
profile over those grams and takes cosine distance. This is the feature
I mention second in an oral exam, after function words, because it is
simple to describe and annoying to argue against.

## How distances are turned into labels

Adjacent paragraphs become three scores:

1. cosine distance of z-scored stylometric vectors
2. cosine distance of character 3-gram profiles
3. Jensen–Shannon divergence of function-word distributions

The ensemble is a weighted sum (0.45 / 0.35 / 0.20 by default). A
threshold then binarizes the list. If no fixed threshold is given, the
cut is adaptive: inside a document, only distances that sit a given
fraction of the way from that document's min to its max count as
changes. If the range is tiny, the detector predicts all zeros. That
last clause is what keeps single-author controls from being shredded.

## What this does not include

No POS tagger, no parser, no transformer. Those are fair extensions.
They are not required to make the sample documents solvable, and they
would hide the arithmetic the notes are trying to show.

If I were adding one more family after the exam, it would be POS
n-grams or a small frozen encoder used only as a paragraph embedder,
still followed by the same adjacent-distance plus threshold recipe.
