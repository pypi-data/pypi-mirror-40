import git
import gwsa
import gwsa.base
from gwsa.status import get_branches_status, get_op_in_progress
from gwsa.base import colors
import os
import sys
import re


class RebaseAction(gwsa.base.AuxAction):
    def __init__(self, prog, subparsers):
        gwsa.base.AuxAction.__init__(
            self, "rebase", "rebase tracking branches", "", prog, subparsers
        )
        self.subp.add_argument(
            "-a", help="rebase all tracking branches", action="store_true", dest="all"
        )

    def action_one(self, repo):
        print colors["repo"](os.path.relpath(repo.working_dir)),
        oip = get_op_in_progress(repo)
        if oip:
            print "   ", oip["op"], "in progress, skipping"
            return
        print
        dirty = repo.is_dirty()
        if dirty:
            repo.git.stash()
        ab = repo.active_branch
        fmt = "   %-" + str(self.sizes["BRANCH"]) + "s  : "
        rcs = get_branches_status(repo)
        if not self.Args.all:
            rcs = [rc for rc in rcs if rc["active"]]

        def print_skip(txt):
            print colors["note"]("skip") + ", " + txt

        def print_flushed(txt):
            sys.stdout.write(txt)
            sys.stdout.flush()

        for rc in rcs:
            print_flushed(fmt % rc["name"])
            if "remote" not in rc:
                print_skip("no remote")
                continue
            if not rc["remote"]["valid"]:
                print_skip("remote gone")
                continue
            if "forced-update" in rc["remote"]:
                print_skip("forced update")
                continue
            if "behind" not in rc["remote"]:
                print_skip("no behind")
                continue
            print_flushed("co ")
            repo.heads[rc["name"]].checkout()
            print_flushed("rebase ")
            try:
                repo.git.rebase(rc["remote"]["name"])
                print_flushed(colors["ok"]("ok"))
            except:
                repo.git.rebase("--abort")
                print_flushed(colors["error"]("conflicts"))
            print
        ab.checkout()
        if dirty:
            repo.git.stash("pop")
