import pytest

from cli.analytics import compute_stats, format_stats


def test_compute_stats_basic():
    stats = compute_stats([1, 2, 3, 4, 5])
    assert stats["count"] == 5
    assert stats["sum"] == 15
    assert stats["min"] == 1
    assert stats["max"] == 5
    assert stats["mean"] == 3
    assert stats["median"] == 3
    assert round(stats["stdev"], 4) == round(1.5811388300841898, 4)


def test_compute_stats_single_value():
    stats = compute_stats([42])
    assert stats["count"] == 1
    assert stats["mean"] == 42
    assert stats["median"] == 42
    # Standard deviation is undefined for a single sample; we default to 0.0
    assert stats["stdev"] == 0.0


def test_compute_stats_accepts_ints_and_floats():
    stats = compute_stats([1, 2.5, 3])
    assert stats["count"] == 3
    assert stats["sum"] == pytest.approx(6.5)


def test_compute_stats_empty_raises_value_error():
    with pytest.raises(ValueError):
        compute_stats([])


def test_format_stats_contains_all_metrics():
    stats = compute_stats([10, 20, 30])
    output = format_stats(stats)
    for metric in ("count", "sum", "min", "max", "mean", "median", "stdev"):
        assert metric in output
