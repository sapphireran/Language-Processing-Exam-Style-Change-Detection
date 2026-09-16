# Topic is not style

This is the sentence the exam is fishing for. Write it at the top of the paper.

> A change of subject is not a change of writer. A change of writer may leave the subject still.

## Three controls in this repo

| File | Voice | Topics | Default detector |
| --- | --- | --- | --- |
| problem-19 | River | greenhouse, quince, night bus | quiet (correct) |
| problem-20 | Quill | stove, lock-gate, miso, bus, parking | quiet (correct) |
| problem-21 | Spark | film, tram, honey | false alarms |

19 and 20 are the clean lesson. 21 is the honest one: chat punctuation and lowercase starts wiggle enough that a register detector can think the writer changed when only the subject did. Do not delete 21 to make the table prettier.

## Medium files: the converse

Problem-08 keeps quince paste on both sides of the hinge. Marble writes a batch sheet; Hearth wraps a parcel. The nouns stay (`quince`, `square`, `paper`). Person, vocative, digits, and semicolons move. The default cut finds that hinge exactly (`00100`).

If you had used a topic vector, 08 would look like one writer and 19 would look like three.

## Hard files: topic held, register held

Problem-13 is two mycologists on one transect. The nouns are shared on purpose (`transect`, `spruce`, `plots`, `ridge`). The leftover signal is *however/which/towards/whilst* versus *but/that/toward/while*. The default blender misses the seam. That is the intended oral takeaway: when you hold topic *and* register, a hand feature set can go blind.

## A one-line test you can run

```bash
PYTHONPATH=src python3 examples/labs/07_topic_confound.py
```

The script scores 19 (must stay quiet) against 08 (must snap). If those two inequalities ever flip, a topic leak has crept back into the blender.
