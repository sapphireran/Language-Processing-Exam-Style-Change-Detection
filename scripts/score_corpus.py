#!/usr/bin/env python3
"""Score the toy bank. Thin wrapper around the CLI report."""

from kerf.report import directory_report


def main() -> None:
    print(directory_report("examples/corpus"))


if __name__ == "__main__":
    main()
