# Binary segmentation

Given feature vectors *x₁ … xₙ*, I score every cut *k ∈ {1,…,n-1}*:

```
score(k) = || μ(x₁…xₖ) − μ(xₖ₊₁…xₙ) ||  ·  √( k(n−k)/n )
```

The first factor is how far the two side-means sit in the saw space.
The second is the usual two-sample / CUSUM weight. A cut that
isolates one paragraph must be very loud. A cut that balances two
houses is preferred.

I take the best *k*. If `score(k)` clears the **first-cut penalty**,
I mark that hinge and recurse on each side. Recursion uses a
**stricter** penalty. A two-paragraph piece always looks sharper
than a four-paragraph piece; if I reused the first-cut number I
would start sawing same-house pairs.

## Why not PELT

PELT and related pruned methods are the grown-up version of this
idea. I do not implement them. On four-to-five paragraph toy files
the extra machinery is an oral distraction. I can say "this is the
first split of binary segmentation; PELT is how you would stop
recomputing on a long series" and sit down.

## Why not only adjacent

Adjacent Euclidean on the saw axis is printed in every report. It
is not the decision. On document 16 (Caliper then Seminar, same
well) both numbers agree. On document 24 (Caliper / Placard /
Caliper) the global split is shy and the adjacent steps are the
ones that clear the floor. I want both numbers on the page so I
can talk about the disagreement instead of hiding it.

## Author count

`1 + sum(changes)` is a lower bound only if authors never return.
On an ABA file it over-counts. The truth files store a real
`authors` field. If the examiner asks how many authors, I say:
the change vector does not answer that; clustering the paragraph
vectors after the cuts does, and I did not implement that because
the exam task as I am revising it is the change vector.
