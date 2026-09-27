import csv
import json
import os

import pytest

from cli.exporter import export_data, SUPPORTED_FORMATS

SAMPLE_DATA = {"count": 3, "sum": 60, "mean": 20.0}


def test_supported_formats_contains_expected_values():
    assert set(SUPPORTED_FORMATS) == {"json", "csv", "txt"}


def test_export_json(tmp_path):
    filepath = str(tmp_path / "stats.json")
    result = export_data(SAMPLE_DATA, filepath, "json")

    assert result == filepath
    with open(filepath) as fh:
        loaded = json.load(fh)
    assert loaded == SAMPLE_DATA


def test_export_csv(tmp_path):
    filepath = str(tmp_path / "stats.csv")
    export_data(SAMPLE_DATA, filepath, "csv")

    with open(filepath, newline="") as fh:
        rows = list(csv.reader(fh))
    assert rows[0] == ["key", "value"]
    assert ["count", "3"] in rows
    assert ["mean", "20.0"] in rows


def test_export_txt(tmp_path):
    filepath = str(tmp_path / "stats.txt")
    export_data(SAMPLE_DATA, filepath, "txt")

    with open(filepath) as fh:
        content = fh.read()
    assert "mean: 20.0" in content
    assert "count: 3" in content


def test_export_creates_missing_parent_directory(tmp_path):
    nested_filepath = str(tmp_path / "nested" / "dir" / "stats.json")
    export_data(SAMPLE_DATA, nested_filepath, "json")

    assert os.path.exists(nested_filepath)


def test_export_format_is_case_insensitive(tmp_path):
    filepath = str(tmp_path / "stats.json")
    export_data(SAMPLE_DATA, filepath, "JSON")

    assert os.path.exists(filepath)


def test_export_invalid_format_raises_value_error(tmp_path):
    filepath = str(tmp_path / "stats.bad")
    with pytest.raises(ValueError):
        export_data(SAMPLE_DATA, filepath, "xml")
