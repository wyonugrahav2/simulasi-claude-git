import sys
import argparse
from . import _program, __version__
from clint.textui import puts, indent, colored

from cli.analytics import compute_stats, format_stats
from cli.exporter import export_data, SUPPORTED_FORMATS


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog=_program)

    parser.add_argument("--version",
                        action="version",
                        version="{0} {1}".format(_program, __version__))

    parser.add_argument("--square",
                        help="Used for testing",
                        type=int,
                        default=None)

    parser.add_argument("--int_value",
                        help="display a square of a given number",
                        type=int)

    parser.add_argument("--float_value",
                        help="display a square of a given number",
                        type=int)

    parser.add_argument("-f",
                        "--flag",
                        help="Specify a flag",
                        action="store_true")
    parser.add_argument("--rating",
                        help="An option with a limited range of values",
                        choices=[1, 2, 3],
                        type=int)

    # Allow --day and --night options, but not together.
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--day",
                       help = "mutually exclusive option",
                       action = "store_true")
    group.add_argument("--night",
                       help = "mutually exclusive option",
                       action = "store_true")

    # --- New in v2.0: analytics feature (cli/analytics.py) ---
    analytics_group = parser.add_argument_group(
        "analytics", "Compute basic statistics on a list of numbers")
    analytics_group.add_argument("--data",
                        help="One or more numeric values to analyze, "
                             "e.g. --data 1 2 3 4",
                        type=float,
                        nargs="+",
                        default=None)
    analytics_group.add_argument("--stats",
                        help="Compute and print statistics for --data",
                        action="store_true")

    # --- New in v2.0: export feature (cli/exporter.py) ---
    export_group = parser.add_argument_group(
        "export", "Export computed statistics to a file")
    export_group.add_argument("--export",
                        help="Filepath to export the computed statistics to",
                        type=str,
                        default=None)
    export_group.add_argument("--export-format",
                        help="File format to export statistics in "
                             "(default: json)",
                        choices=SUPPORTED_FORMATS,
                        default="json")

    args = parser.parse_args(args)

    if args.square:
        print(args.square**2)
        return

    if args.stats or args.export:
        if not args.data:
            parser.error("--stats/--export requires --data to be provided")

        stats = compute_stats(args.data)

        if args.stats:
            print(format_stats(stats))

        if args.export:
            path = export_data(stats, args.export, args.export_format)
            with indent(4):
                puts(colored.green("Exported statistics to: ") + path)
        return

    with indent(4):
        puts(colored.blue("Arguments"))
        puts(colored.green("int value: ") + str(args.int_value))
        puts(colored.green("float value: ") + str(args.float_value))
        puts(colored.green("flag: ") + str(args.flag))
        puts(colored.green("rating: ") + str(args.rating))

if __name__ == '__main__':
    main()
