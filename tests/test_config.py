"""Test configuration settings."""
from pathlib import Path

from src.config import DATA_DIR, OUTPUT_DIR, ROOT_DIR


def test_config_paths():
    assert isinstance(ROOT_DIR, Path)
    assert isinstance(DATA_DIR, Path)
    assert isinstance(OUTPUT_DIR, Path)
    assert DATA_DIR == ROOT_DIR / "data"
    assert OUTPUT_DIR == ROOT_DIR / "output"
