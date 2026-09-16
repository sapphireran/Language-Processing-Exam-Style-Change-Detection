# Why compression is a style probe

The sentence I want in the oral is:

> Two paragraphs by the same person share regularities a compressor can
> reuse. Two paragraphs by different people share fewer. Normalized
> Compression Distance is a way of asking that question without writing
> down the regularities in advance.

That is the whole thesis of **quoin**. The rest of the lab is me being
honest about when the sentence is too optimistic.

## Kolmogorov, then we put it back on the shelf

The Kolmogorov complexity `K(x)` is the length of the shortest program
that emits `x`. It is a beautiful definition of "how much structure is
in this string." It is also uncomputable. I will say the word, I will
not pretend I computed it.

A real compressor `C(x)` — zlib in this repo, gzip / LZMA / a PPM
model in a more serious paper — is an **upper bound** on `K(x)`. If
`x` is boring to the compressor, `C(x)` is small relative to `|x|`. If
`x` is surprising, `C(x)` stays large.

Authorship is a source of boredom. People reuse function words in
stable ratios. They punctuate on a habit. They have a favourite
sentence length. A compressor that has just seen paragraph A will find
paragraph B cheaper if B was written by the same habit.

## Why I like this for an exam

I can defend it without a GPU and without a training set of authors.
That matches the *intrinsic* constraint. I can also compute a tiny
version by hand (see the next page) so the method is not a library I
cannot open.

It is also a useful contrast to transformers. A fine-tuned encoder is
usually stronger on the real PAN data. It is also a black box I cannot
derive on a whiteboard, and it will happily use topic unless I stop it.
Compression is the method I use to *talk about* the problem. It is not
the method I would ship to TIRA in 2026 without a lot more work.

## The three objections I expect

**Short text.** zlib has a header and a cold dictionary. A twenty-word
chat line does not fill the window. NCD on short paragraphs is mostly
the wrapper. That is why the Quoin score also uses character 3-grams
and function words, which degrade more gracefully.

**Topic.** The string `quoin` compresses whether or not the two
paragraphs share an author. Content words are regularities too. Closed-
class features are the counterweight: they do not name bees, roofs, or
letterpress.

**The compressor is the model.** Different compressors induce different
distances. zlib is a convenient, reproducible stand-in, not a claim
about the best approximation to `K`. If someone asks "why not PPM?"
the answer is "I would, in a paper; I will not hide a C extension in an
exam lab."

## The lineage I will cite if they want names

Benedetto, Caglioti and Loreto (2002) used gzip as a language
distance. Cilibrasi and Vitányi developed NCD as a general clustering
distance. The authorship literature picked the idea up because it is
language-agnostic and feature-free. I am not the first person to put a
compressor next to a paragraph hinge. I am using it as a teaching
wedge — a quoin — for the exam.
