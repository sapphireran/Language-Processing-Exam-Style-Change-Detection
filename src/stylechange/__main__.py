"""Allow ``python -m stylechange`` after an editable install or with PYTHONPATH=src."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
