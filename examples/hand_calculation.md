# Hand calculation

These two micro-texts are also [Q3 and Q4](../docs/06-worked-exam-questions.md).
Run the snippet to confirm your arithmetic before the exam.

## Type–token ratio

```
A: The cat sat on the mat. The cat was sad.
B: I can't even. This is just wild, honestly.
```

Expected: A has 10 tokens, 7 types, TTR = 0.70. B has 8 tokens, 8
types, TTR = 1.00. Do not treat the gap as authorship.

## Function-word cosine

Restricted vocab `{the, a, i, of}`:

```
P: I saw the cat of the neighbour.
Q: The theory of the aether was a curiosity and a myth.
```

Counts P = (2, 0, 1, 1), Q = (2, 2, 0, 1). Cosine ≈ 0.680, distance ≈
0.320.

```bash
PYTHONPATH=src python3 scripts/check_hand_calculation.py
```
