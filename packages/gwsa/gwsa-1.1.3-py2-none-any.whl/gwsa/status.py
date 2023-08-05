import git
import gwsa
import gwsa.base
from gwsa.base import colors
import os
import re


def get_op_in_progress(repo):
    status = repo.git.status()
    opipre = '(?m)use "git (?P<op>\S+) --abort"'
    m = re.search(opipre, status)
    if not m:
        return None
    md = m.groupdict()
    if md["op"] == "rebase":
        brre = "(?m)currently rebasing branch '(?P<branch>\S+)' on "
    else:
        brre = "(?m)^On branch (?P<branch>\S+)"
    m = re.search(brre, status)
    if m:
        md.update(m.groupdict())
    return md


class Branches(object):
    def __init__(self, repo):
        super(Branches, self).__init__()
        self.repo = repo

    def get_branch_status_remote(self, rc):
        if not rc["remote"]:
            return None
        remre = "^\[(?P<name>.*?)(: (?P<track>.*))?\]"
        m = re.match(remre, rc["remote"])
        if not m:
            return None
        m = m.groupdict()
        rcr = {"name": m["name"], "valid": True}
        if not m["track"]:
            return rcr
        for tok in m["track"].split(", "):
            if tok == "gone":
                rcr["valid"] = False
            elif tok.startswith("ahead "):
                rcr["ahead"] = tok.split()[1]
            elif tok.startswith("behind "):
                rcr["behind"] = tok.split()[1]
            else:
                try:
                    rcr["notes"].apeend(tok)
                except:
                    rcr["notes"] = [tok]
        if "behind" in rcr:
            txt = self.repo.git.reflog(rcr["name"])
            txt = txt.splitlines()
            if txt and txt[0].endswith("forced-update"):
                rcr["forced-update"] = True
        return rcr

    def get_branch_status(self, line):
        bvvre = "^(?P<active>\*)?\s+(?P<name>.*?)\s+(?P<hash>[a-f0-9]+)\s+"
        bvvre += "(?P<remote>\[[^]]*\])?(?P<msg>.+)"
        m = re.match(bvvre, line)
        if not m:
            return
        rc = m.groupdict()
        if rc["name"].startswith("(no branch, rebasing"):
            return
        frc = {"name": rc["name"]}
        if self.oip:
            frc["active"] = rc["name"] == self.oip["branch"]
            if frc["active"]:
                frc["op_in_progress"] = self.oip["op"]
        else:
            frc["active"] = bool(rc["active"])
        if frc["active"]:
            frc["dirty"] = self.repo.is_dirty()
        # rc['msg'] = rc['msg'].strip()
        rcr = self.get_branch_status_remote(rc)
        if rcr:
            frc["remote"] = rcr
        return frc

    def __iter__(self):
        self.lines = self.repo.git.branch("-vv").splitlines()
        self.oip = get_op_in_progress(self.repo)
        return self

    def __next__(self):
        while self.lines:
            rc = self.get_branch_status(self.lines[0])
            del self.lines[0]
            if not rc:
                continue
            return rc
        raise StopIteration

    def next(self):
        return self.__next__()


def get_branches_status(repo):
    return list(Branches(repo))


class StatusAction(gwsa.base.AuxAction):
    def __init__(self, prog, subparsers):
        gwsa.base.AuxAction.__init__(
            self,
            "status",
            "print status of repo and all branches",
            "",
            prog,
            subparsers,
        )
        self.subp.add_argument(
            "-s", help="short output format", action="store_true", dest="short"
        )
        self.subp.add_argument(
            "-r", help="show remote branch", action="store_true", dest="remote"
        )

    def action_one(self, repo):
        rcs = get_branches_status(repo)
        # print gwsa.base.prettify(rcs)
        if self.Args.short:
            self.action_one_short(repo, rcs)
        else:
            self.action_one_full(repo, rcs)

    def action_one_short(self, repo, rcs):
        fmt = "%-" + str(self.sizes["REPO"]) + "s"
        print fmt % repo.cwd, " : ",
        fmt = "%-" + str(self.sizes["BRANCH"]) + "s"
        rc = [rc for rc in rcs if rc["active"]]
        assert len(rc) == 1
        rc = rc[0]
        print fmt % rc["name"], " : ",
        print self.branch_status(repo, rc)

    def action_one_full(self, repo, rcs):
        print colors["repo"](os.path.relpath(repo.working_dir))
        fmt = "%-" + str(self.sizes["BRANCH"]) + "s"
        for rc in rcs:
            if rc["active"]:
                print colors["note"]("  *"),
            else:
                print "   ",
            print fmt % rc["name"], " : ",
            print self.branch_status(repo, rc)

    def branch_status(self, repo, rc):
        notes = []
        if "op_in_progress" in rc:
            notes.append(colors["error"](rc["op_in_progress"]))
        if "dirty" in rc and rc["dirty"]:
            notes.append(colors["warn"]("dirty"))
        if "remote" in rc:
            ts = rc["remote"]
            if not ts["valid"]:
                notes.append(colors["error"]("gone"))
            if "ahead" in ts:
                notes.append(colors["note"]("ahead " + ts["ahead"]))
            if "behind" in ts:
                notes.append(colors["warn"]("behind " + ts["behind"]))
                if "forced-update" in ts:
                    notes.append(colors["error"]("forced-update"))
            if self.Args.remote:
                notes.append(rc["remote"]["name"])
        return ", ".join(notes)
