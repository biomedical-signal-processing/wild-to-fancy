"""
Entry script redirecting all command line arguments to a specified script
from the wtfancy.bin folder.

Usage:
ut [--help] script [script args]... [--seed]
"""

import argparse
import os
import sys

sys.path.insert(0, '/app')
print(sys.path)
import wtfancy


def get_parser():
    from wtfancy import bin
    import pkgutil
    mods = pkgutil.iter_modules(bin.__path__)

    ids = "wild-to-fancy"
    sep = "-" * len(ids)
    usage = ("wtfancy [--help] script [script args]... [--seed]\n\n"
             "%s\n%s\n"
             "Available scripts:\n") % (ids, sep)

    choices = []
    file_name = os.path.split(os.path.abspath(__file__))[-1]
    for m in mods:
        if isinstance(m, tuple):
            name, ispkg = m[1], m[2]
        else:
            name, ispkg = m.name, m.ispkg
        if name == file_name[:-3] or ispkg:
            continue
        usage += "- " + name + "\n"
        choices.append(name)

    # Top level parser
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("script", help="Name of the mp script to run.",
                        choices=choices)
    parser.add_argument("--seed", default=None, type=int,
                        help="Run this script with numpy and random RNGs seeded "
                             "from integer --seed.")
    return parser


def split_help_from_args(args):
    other_args, help_args = [], []
    for arg in args:
        if arg == "-h" or arg == "--help":
            help_args.append("--help")
        else:
            other_args.append(arg)
    return other_args, help_args


def entry_func():
    # Get the script to execute, parse only first input
    args, help_args = split_help_from_args(sys.argv[1:])
    parsed, script_args = get_parser().parse_known_args(args or help_args)
    script = parsed.script
    if parsed.seed is not None:
        wtfancy.Defaults.set_global_seed(parsed.seed)

    # Import the script
    import importlib
    mod = importlib.import_module("wtfancy.bin." + script)

    # Call entry function with remaining arguments
    mod.entry_func(script_args + help_args)


if __name__ == "__main__":
    entry_func()
