#!/usr/bin/python2
"""git workspace automation. Runs specified command on all git repositories.
"""


############################################################
# {{{ configure logging
import logging
import sys
import json

try:
    import customlogging
except:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

log = logging.getLogger("gwsa")
if "--debug" in sys.argv:
    log.setLevel(logging.DEBUG)


def prettify(obj):
    class AllEncoder(json.JSONEncoder):
        def default(self, obj):
            try:
                return json.JSONEncoder.default(self, obj)
            except Exception as e:
                return str(obj)

    return json.dumps(obj, indent=4, sort_keys=True, cls=AllEncoder)


# }}}


############################################################
# {{{ main: argparse and dispatch

import json
import argparse
import os
import gwsa
import gwsa.status
import gwsa.fetch
import gwsa.rebase
import git


class MyProgressPrinter(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(
            op_code,
            cur_count,
            max_count,
            cur_count / (max_count or 100.0),
            message or "NO MESSAGE",
        )


def AppArgParser():
    p = argparse.ArgumentParser(
        prog=gwsa.__package__,
        usage="usage: %(prog)s [options] <command> [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    p.add_argument("--debug", help="debug mode", dest="debug", action="store_true")
    p.add_argument("--version", action="version", version=gwsa.__version__)
    return p


def main():
    p = AppArgParser()
    desc = "run '%(prog)s <command> -h' to get help"
    subparsers = p.add_subparsers(description=desc, metavar=" ", dest="subcommand")
    gwsa.status.StatusAction(gwsa.__package__, subparsers)
    gwsa.fetch.FetchAction(gwsa.__package__, subparsers)
    gwsa.rebase.RebaseAction(gwsa.__package__, subparsers)

    Args, UnknownArgs = p.parse_known_args()
    log.debug("Args: %s", prettify(vars(Args)))
    log.debug("UnknownArgs: %s", UnknownArgs)

    if hasattr(Args, "func"):
        Args.func(Args, UnknownArgs)


# }}}

if __name__ == "__main__":
    main()
