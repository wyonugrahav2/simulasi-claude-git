import json

import pytest

from cli import command
from tests.test_utilities import Capturing


def test_cli_stats_prints_summary():
    with Capturing() as out:
        command.main(["--data", "1", "2", "3", "4", "5", "--stats"])
    output = "\n".join(out)
    assert "mean" in output
    assert "median" in output


def test_cli_export_writes_file(tmp_path):
    # Note: the "Exported statistics to: ..." confirmation is printed via
    # clint's puts(), which writes to the real stdout file descriptor and
    # therefore isn't captured by Capturing() (same limitation as the
    # pre-existing test_vars test in test_cli.py). We verify the concrete,
    # observable effect instead: the file itself.
    export_path = str(tmp_path / "stats.json")
    command.main(["--data", "10", "20", "30", "--export", export_path])

    with open(export_path) as fh:
        data = json.load(fh)
    assert data["count"] == 3
    assert data["mean"] == 20.0


def test_cli_stats_and_export_together(tmp_path):
    export_path = str(tmp_path / "stats.csv")
    with Capturing() as out:
        command.main([
            "--data", "5", "10", "15",
            "--stats",
            "--export", export_path,
            "--export-format", "csv",
        ])
    output = "\n".join(out)
    assert "mean" in output
    with open(export_path) as fh:
        content = fh.read()
    assert "count" in content


def test_cli_stats_without_data_errors():
    with pytest.raises(SystemExit):
        command.main(["--stats"])


def test_cli_existing_square_behavior_unchanged():
    with Capturing() as out:
        command.main(["--square", "20"])
    assert int(out[0]) == 400
