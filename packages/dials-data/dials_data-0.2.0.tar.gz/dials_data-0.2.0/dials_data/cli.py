from __future__ import absolute_import, division, print_function

import argparse
import sys

import dials_data
import dials_data.datasets


def cli_list(cmd_args):
    parser = argparse.ArgumentParser(
        description="Show dataset information", prog="dials.data list"
    )
    parser.add_argument(
        "--missing-fileinfo",
        action="store_true",
        help="only list datasets that do not have a bill of material",
    )
    parser.add_argument("--quiet", action="store_true", help="machine readable output")
    args = parser.parse_args(cmd_args)
    if args.missing_fileinfo:
        ds_list = dials_data.datasets.fileinfo_dirty
    else:
        ds_list = dials_data.datasets.definition
    dials_data.datasets.list_known_definitions(ds_list, quiet=args.quiet)


def main():
    parser = argparse.ArgumentParser(
        usage="dials.data <command> [<args>]",
        description="""DIALS regression data manager v{version}

The most commonly used commands are:
   list     List available datasets
   get      Download datasets
""".format(
            version=dials_data.__version__
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("subcommand", help=argparse.SUPPRESS)
    # parse_args defaults to [1:] for args, but need to
    # exclude the rest of the args too, or validation will fail
    parameters = sys.argv[1:2]
    if not parameters:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args(parameters)
    subcommand = globals().get("cli_" + args.subcommand)
    if subcommand:
        return subcommand(sys.argv[2:])
    parser.print_help()
    print()
    sys.exit("Unrecognized command: {}".format(args.subcommand))
