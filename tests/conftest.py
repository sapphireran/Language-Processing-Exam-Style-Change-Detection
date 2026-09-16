from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = ROOT / "examples" / "documents"
TRUTH_DIR = DOC_DIR / "truth"
AUTHOR_DIR = ROOT / "examples" / "authors"


@pytest.fixture
def doc_dir() -> Path:
    return DOC_DIR


@pytest.fixture
def truth_dir() -> Path:
    return TRUTH_DIR


@pytest.fixture
def author_dir() -> Path:
    return AUTHOR_DIR
