# Hinges and PAN-shaped I/O

The bundled files follow the shared-task *shape* without using shared-task *text*.

## Problem file

`examples/corpus/problem-13-two-mycologists.txt` is one sentence per line. That is a teaching convention so `len(changes) == n_units - 1` is obvious. A real dump may be wrapped prose; `hingemark split --mode sentences` exists for that.

## Truth file

```json
{
  "changes": [0, 0, 0, 1, 0, 0, 0],
  "authors": [1, 1, 1, 1, 2, 2, 2, 2],
  "split": "hard",
  "note": "Same chanterelle transect. ..."
}
```

A submitted **solution** only needs `changes`. `authors` is extra teaching metadata.

## The returning-author identity

```
n_authors_from_changes = 1 + sum(changes)
```

This equals the true writer count only if nobody returns. Problem-22 is River, Marble, River:

- `changes = [0, 1, 0, 1, 0]`
- `1 + sum(changes) = 3`
- `len(set(authors)) = 2`

Say this out loud in the oral if you are asked for a limitation of the official label. Binary hinges record *seams*, not *identities*.

## Length checks the tests lock

- `len(changes) == n_units - 1`
- `len(authors) == n_units` when authors are present
- every bit is 0 or 1
- `changes[i] == 0` iff `authors[i] == authors[i+1]`

If a detector emits the wrong length, the evaluator should refuse the file rather than pad it.

## CLI

```bash
PYTHONPATH=src python3 -m hingemark split examples/corpus/problem-01-canal-then-lot.txt
PYTHONPATH=src python3 -m hingemark detect examples/corpus/problem-01-canal-then-lot.txt
PYTHONPATH=src python3 -m hingemark explain examples/corpus/problem-22-canal-return.txt
```
