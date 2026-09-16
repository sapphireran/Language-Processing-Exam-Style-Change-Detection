# Why pairwise hinges lie

A pairwise detector scores paragraph *i* against paragraph *i+1*.
Three ordinary documents make that score a liar.

## Short neighbours

A twelve-word paragraph has unstable rates. *You* appearing twice is
a 0.16 swing. Pairwise cosine / Euclidean treats that swing as a
house. A split score averages the short paragraph into a side, so
one stub cannot move the cut unless the rest of the side agrees.

## ABA returns

Document 25 is Pocket / Statute / Pocket. Both local steps are loud
(adjacent ≈ 0.62). The *global* split is modest (≈ 0.27) because
each side of a single cut is mixed. A pairwise model that only looks
at neighbours may fire both hinges, which happens to be correct here.
A pairwise model that z-scores within the document will fire
*neither*: both steps are equally loud, so neither is an outlier.

That is why kerf keeps an **absolute adjacent floor** as a second
blade. Z-peaks are for documents with one loud step. ABA has two.

## The topic costume

Document 20 is Caliper on a stilling well and then Caliper on a
cinema booth. A bag-of-words pair will scream. The saw should stay
shut. Pairwise content models fail this on purpose; that failure is
the 2023–2025 PAN difficulty story (topical homogeneity). I baked
the same story into four trap files so I can point at them.

## What I still use neighbours for

Adjacent distance is a good *secondary* cue. I do not lead with it.
I lead with the left/right split, then I let a loud absolute step
mark a hinge the first saw diluted. See
[binary segmentation](05-binary-segmentation.md).
