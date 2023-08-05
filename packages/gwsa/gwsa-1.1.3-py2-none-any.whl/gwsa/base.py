import argparse
import git
from blessed import Terminal
import json
import re
import logging

log = logging.getLogger("gwsa")

############################################################
# {{{ Run shell commands
import os
import subprocess as sp

run_fmt = {"pwd": os.getcwd()}


def run(cmd, hide_stdout=False, hide_stderr=False):
    cmd = cmd % run_fmt
    log.debug("Command '%s'", cmd)
    kwargs = {"shell": True, "executable": "/bin/bash"}
    if hide_stderr:
        kwargs["stderr"] = open("/dev/null", "w")
    if hide_stdout:
        kwargs["stdout"] = open("/dev/null", "w")
    sp.check_call(cmd, **kwargs)


def run_output(cmd, hide_stderr=True, strip=True, ignore_error=False):
    cmd = cmd % run_fmt
    log.debug("cmd '%s'", cmd)
    kwargs = {"shell": True, "executable": "/bin/bash"}
    if hide_stderr:
        kwargs["stderr"] = open("/dev/null", "r")
    try:
        rc = sp.check_output(cmd, **kwargs)
    except Exception as e:
        if ignore_error:
            return ""
        raise e
    if strip:
        rc = rc.strip()
    return rc


# }}}


def prettify(obj):
    class AllEncoder(json.JSONEncoder):
        def default(self, obj):
            try:
                return json.JSONEncoder.default(self, obj)
            except Exception as e:
                return str(obj)

    return json.dumps(obj, indent=4, sort_keys=True, cls=AllEncoder)


t = Terminal()
colors = {
    "repo": t.bold_green,
    "branch": t.blue,
    "ok": t.bright_green,
    "note": t.cyan,
    "warn": t.yellow,
    "error": t.bright_yellow,
}


def get_remote_has_updates(rem, progress=None):
    assert rem.exists()
    for fi in rem.fetch("--dry-run", progress=progress):
        if fi.flags != fi.HEAD_UPTODATE:
            return True
    return False


class AuxAction(object):
    def __init__(self, name, help, epilog, prog, subparsers):
        self.subp = subparsers.add_parser(
            name,
            help=help,
            description=help,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog=prog + " " + name,
            epilog=epilog,
        )
        self.subp.set_defaults(func=self.action)

    def action(self, Args, UnknownArgs):
        if UnknownArgs:
            raise Exception("unknown command line args")

        self.Args = Args
        self.UnknownArgs = UnknownArgs
        rdirs = run_output("find . -maxdepth 3 -type d -name .git | sort").splitlines()
        rdirs = [r[:-5] for r in rdirs]  # rm '/.git' ending
        rdirs = [r[2:] for r in rdirs]  # rm './' beggining
        if "" in rdirs:
            rdirs[rdirs.index("")] = "."
        if not rdirs:
            return
        self.repos = []
        for rdir in rdirs:
            r = git.Repo(rdir)
            setattr(r, "cwd", rdir)
            self.repos.append(r)

        repol = branchl = 5
        for repo in self.repos:
            repol = max(repol, len(repo.cwd))
            try:
                branchl = max(branchl, len(repo.active_branch.name))
            except:
                pass
        self.sizes = {"REPO": repol, "BRANCH": branchl}
        self.fmt = "%s %s"

        for r in self.repos:
            self.action_one(r)
