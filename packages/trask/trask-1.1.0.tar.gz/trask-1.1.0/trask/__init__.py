# TODO remove this
# pylint: disable=missing-docstring

import argparse

from trask import phase1, phase2, phase3


def load(path):
    root = phase1.load(path)
    return phase2.Phase2.load(phase2.SCHEMA, root)


def run(path, dry_run):
    root = load(path)
    ctx = phase3.Context(dry_run=dry_run)
    phase3.run(root, ctx)


def parse_args(args=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog='trask', description='run a trask file')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('path')
    return parser.parse_args(args)
