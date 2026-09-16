# HTML reports

Generate from the teaching corpus:

```
PYTHONPATH=src python3 -m seamtrace report examples/corpus --out examples/reports
```

`index.html` is the table of contents. Generated HTML is gitignored so
the committed lab stays the notes plus the code that can rebuild them.
