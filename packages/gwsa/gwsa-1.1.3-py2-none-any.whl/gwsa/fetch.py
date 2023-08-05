import git
import gwsa
import gwsa.base
from gwsa.base import colors
import os
import sys


class ProgressCount(git.RemoteProgress):
    def __init__(self):
        git.RemoteProgress.__init__(self)
        self.count = 0

    def update(self, op_code, cur_count, max_count=None, message=""):
        self.count += 1


class FetchAction(gwsa.base.AuxAction):
    def __init__(self, prog, subparsers):
        gwsa.base.AuxAction.__init__(
            self, "fetch", "fetch from all remotes", "", prog, subparsers
        )
        self.subp.add_argument(
            "-n",
            "--dry-run",
            help="check for updates, do not fetch them",
            action="store_true",
        )
        self.subp.add_argument(
            "-r", help="show remote url", action="store_true", dest="remote"
        )

    def action_one_remote(self, repo):
        print colors["repo"](repo.cwd)
        fmt = "  %-10s  :"
        for rem in repo.remotes:
            print fmt % rem.name,
            urls = " ".join(rem.urls)
            print urls,
            rc = self.get_fetch_status(rem, self.Args.dry_run)
            print rc

    def action_one(self, repo):
        if self.Args.remote:
            return self.action_one_remote(repo)
        fmt = "%-" + str(self.sizes["REPO"]) + "s"
        print fmt % repo.cwd, " : ",
        first = True
        for rem in repo.remotes:
            txt = ""
            if first:
                first = False
            else:
                txt = ", "
            txt += rem.name + " "
            sys.stdout.write(txt)
            sys.stdout.flush()
            txt = self.get_fetch_status(rem, self.Args.dry_run)
            sys.stdout.write(txt)
            sys.stdout.flush()
        print

    def get_fetch_status(self, rem, dry_run):
        pb = ProgressCount()
        txt = ""
        if dry_run:
            rc = gwsa.base.get_remote_has_updates(rem, progress=pb)
            if rc:
                if pb.count:
                    txt = colors["warn"]("fetch") + " "
                txt = colors["error"]("diff")
            else:
                txt = colors["note"]("ok")
        else:
            try:
                rem.fetch(prune=True, progress=pb)
                if pb.count:
                    txt = colors["warn"]("fetch")
                else:
                    txt = colors["note"]("ok")
            except:
                txt = colors["error"]("err")

        return txt
