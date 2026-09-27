[![Build Status](https://travis-ci.org/danielecook/python-cli-skeleton.svg?branch=master)](https://travis-ci.org/danielecook/python-cli-skeleton) [![Coverage Status](https://coveralls.io/repos/github/danielecook/python-cli-skeleton/badge.svg?branch=master)](https://coveralls.io/github/danielecook/python-cli-skeleton?branch=master)

# python-cli-skeleton

**v2.0** — A simple python command line interface skeleton project. Features support for:

* travis-ci
* coveralls
* argparse
* py.test (testing)
* built-in **analytics** (basic statistics on numeric input)
* built-in **export** (save results to JSON, CSV, or plain text)

The `cli/analytics.py` module computes and formats descriptive statistics
for numeric input. The `cli/exporter.py` module writes those results to JSON,
CSV, or plain-text files.

__Installation__

```
python setup.py install 
```

For development, use:

```
python setup.py develop
```

...and the program will be installed in-place, allowing you to edit the script files and test them from the command line.

__Usage__

The setup script will install the program as `cli`. You can invoke it using:

```
cli
```

To change the way the program is invoked, edit the `cli/__init__.py` file where you can set the `__version__` and `_program` variables. The `_program` variable sets the commandline command (`cli`), and the program name. You may want to change the names of modules (folders) as well to reflect your program. You should change the entry_point part of the setup script to reflect any changes you make to folders/files:

```
entry_points="""
[console_scripts]
{program} = cli.cli:main
""".format(program = _program),
```

__New in v2.0: Analytics (`cli/analytics.py`)__

The `--data` option accepts one or more numeric values. Combined with `--stats`, it computes and prints basic descriptive statistics (`count`, `sum`, `min`, `max`, `mean`, `median`, `stdev`) as a formatted table:

```
cli --data 4 8 15 16 23 42 --stats
```

```
Metric       Value
--------  --------
count       6
sum       108
min         4
max        42
mean       18
median     15.5
stdev      13.4907
```

The underlying logic lives in `cli/analytics.py` and can be reused directly:

```python
from cli.analytics import compute_stats, format_stats

stats = compute_stats([4, 8, 15, 16, 23, 42])
print(format_stats(stats))
```

__New in v2.0: Export (`cli/exporter.py`)__

Use `--export <filepath>` to save the computed statistics to a file. Choose the output format with `--export-format` (`json` [default], `csv`, or `txt`):

```
cli --data 1 2 3 4 5 --export results.json
cli --data 1 2 3 4 5 --export results.csv --export-format csv
```

Missing parent directories in the destination path are created automatically. The underlying logic lives in `cli/exporter.py`:

```python
from cli.exporter import export_data

export_data({"mean": 3.0, "count": 5}, "results.json", fmt="json")
```

Both `--stats` and `--export` require `--data` to be supplied, and they can be combined in a single invocation to both print and save the results.

__requirements.txt__

Add any modules you want installed to the `requirements.txt` file. The setup file parses this file before installation. Current requirements:

* `[clint](https://github.com/kennethreitz/clint)` — adding color, indenting, progress bars, and other useful things to command-line based programs.
* `[tabulate](https://github.com/astanin/python-tabulate)` — used by `cli/analytics.py` to render the statistics table.

__travis-ci__

A `.travis.yml` file is included and setup for Python. Testing is performed using Python 2.7 and 3.6. You will need to setup `[travis-ci.org](travis-ci.org)` to perform testing.

__coveralls__

Support for coveralls is build in using `pytest-cov`. Please see [coveralls.io](https://coveralls.io/) for more information. You may want to edit the `.coveragerc` file to fine tune how coverage is calculated.