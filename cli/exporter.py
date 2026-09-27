"""Export utilities for the CLI skeleton project.

Supports exporting a flat dictionary of results (e.g. the output of
:func:`cli.analytics.compute_stats`) to JSON, CSV or plain text files. Used
by the ``--export``/``--export-format`` command line options.
"""

import csv
import json
import os
from typing import Dict, Union

Number = Union[int, float]

#: File formats supported by :func:`export_data`.
SUPPORTED_FORMATS = ("json", "csv", "txt")


def export_data(data: Dict[str, Number], filepath: str, fmt: str = "json") -> str:
    """Export a dict of results to ``filepath`` in the given format.

    :param data: Mapping of metric name to value.
    :param filepath: Destination file path. Parent directories are created
        automatically if they do not already exist.
    :param fmt: One of ``"json"``, ``"csv"`` or ``"txt"``.
    :return: The ``filepath`` that was written, for convenience.
    :raises ValueError: If ``fmt`` is not a supported format.
    """
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(
            "Unsupported export format '{0}'. Supported formats: {1}".format(
                fmt, ", ".join(SUPPORTED_FORMATS)
            )
        )

    directory = os.path.dirname(os.path.abspath(filepath))
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    if fmt == "json":
        _export_json(data, filepath)
    elif fmt == "csv":
        _export_csv(data, filepath)
    else:
        _export_txt(data, filepath)

    return filepath


def _export_json(data: Dict[str, Number], filepath: str) -> None:
    with open(filepath, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)


def _export_csv(data: Dict[str, Number], filepath: str) -> None:
    with open(filepath, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["key", "value"])
        for key, value in data.items():
            writer.writerow([key, value])


def _export_txt(data: Dict[str, Number], filepath: str) -> None:
    with open(filepath, "w") as fh:
        for key, value in data.items():
            fh.write("{0}: {1}\n".format(key, value))
