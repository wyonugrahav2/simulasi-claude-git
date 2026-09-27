"""Analytics utilities for the CLI skeleton project.

This module provides simple, dependency-light statistical helpers that can
be applied to a list of numeric values. It backs the ``--data``/``--stats``
options exposed on the command line (see :mod:`cli.command`).
"""

import statistics
from typing import Dict, List, Union

from tabulate import tabulate

Number = Union[int, float]

#: The order in which computed metrics are displayed/exported.
STAT_KEYS = ("count", "sum", "min", "max", "mean", "median", "stdev")


def compute_stats(data: List[Number]) -> Dict[str, Number]:
    """Compute basic descriptive statistics for a list of numbers.

    :param data: A non-empty list of numeric values.
    :return: A dict containing ``count``, ``sum``, ``min``, ``max``,
        ``mean``, ``median`` and ``stdev``.
    :raises ValueError: If ``data`` is empty.
    """
    if not data:
        raise ValueError("data must contain at least one numeric value")

    numeric_data = [float(x) for x in data]

    stats: Dict[str, Number] = {
        "count": len(numeric_data),
        "sum": sum(numeric_data),
        "min": min(numeric_data),
        "max": max(numeric_data),
        "mean": statistics.mean(numeric_data),
        "median": statistics.median(numeric_data),
    }

    # Standard deviation is undefined for a single sample; default to 0.0
    # instead of raising, so single-value inputs remain usable.
    stats["stdev"] = statistics.stdev(numeric_data) if len(numeric_data) > 1 else 0.0

    return stats


def format_stats(stats: Dict[str, Number]) -> str:
    """Render a stats dict (from :func:`compute_stats`) as a readable table."""
    rows = []
    for key in STAT_KEYS:
        value = stats.get(key)
        if isinstance(value, float):
            value = round(value, 4)
        rows.append([key, value])

    return tabulate(rows, headers=["Metric", "Value"], tablefmt="simple")
