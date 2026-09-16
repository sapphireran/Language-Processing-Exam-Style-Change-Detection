# Tests

```bash
python3 -m pip install -e .
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The suite checks feature tells for the house authors, macro-F1 arithmetic,
detector I/O length, and alignment of every synthetic gold file with its
`author_ids`. It does not download data and it does not call any network
API.
