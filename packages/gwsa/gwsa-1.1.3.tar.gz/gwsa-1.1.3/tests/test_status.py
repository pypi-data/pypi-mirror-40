import unittest
import gwsa
import gwsa.status
import gwsa.base
import tempfile
import shutil
import git
import os
import sys
from misc import *


class StatusTest(unittest.TestCase):
    def setUp(self):
        self.count = 0
        self.basedir = tempfile.mkdtemp()
        self.repo = create_repo(self.basedir, "repo1")
        fill_repo(self.repo)
        self.crepo = self.repo.clone(os.path.join(self.basedir, "repo2"))

    def tearDown(self):
        shutil.rmtree(self.basedir)
        # pass

    def test_status_clean_local_branch(self):
        rcs = gwsa.status.get_branches_status(self.repo)
        # print gwsa.base.prettify(rcs)
        expected = [
            {"active": True, "dirty": False, "name": "feature1"},
            {"active": False, "name": "feature2"},
            {"active": False, "name": "master"},
        ]
        self.assertEqual(rcs, expected)

        self.repo.heads["master"].checkout()
        rcs = gwsa.status.get_branches_status(self.repo)
        # print gwsa.base.prettify(rcs)
        expected[0]["active"] = False
        del expected[0]["dirty"]
        expected[2]["active"] = True
        expected[2]["dirty"] = False
        self.assertEqual(rcs, expected)

    def test_status_dirty_local_branch(self):
        self.repo.heads["master"].checkout()
        add_line(self.repo, "readme.md")
        rcs = gwsa.status.get_branches_status(self.repo)
        # print gwsa.base.prettify(rcs)
        expected = [
            {"active": False, "name": "feature1"},
            {"active": False, "name": "feature2"},
            {"active": True, "dirty": True, "name": "master"},
        ]
        self.assertEqual(rcs, expected)

    def test_status_remote_ahead_behind_branch(self):
        rcs = gwsa.status.get_branches_status(self.crepo)
        # print gwsa.base.prettify(rcs)
        expected = [
            {
                "active": True,
                "dirty": False,
                "name": "feature1",
                "remote": {"name": "origin/feature1", "valid": True},
            }
        ]
        self.assertEqual(rcs, expected)

        add_commit(self.crepo, "tt.txt")
        add_commit(self.crepo, "tt1.txt")
        rcs = gwsa.status.get_branches_status(self.crepo)
        # print gwsa.base.prettify(rcs)
        expected[0]["remote"]["ahead"] = "2"
        self.assertEqual(rcs, expected)

        add_commit(self.repo, "tt.txt")
        add_commit(self.repo, "tt1.txt")
        add_commit(self.repo, "tt1.txt")
        self.crepo.remotes["origin"].fetch(prune=True)
        rcs = gwsa.status.get_branches_status(self.crepo)
        # print gwsa.base.prettify(rcs)
        expected[0]["remote"]["behind"] = "3"
        self.assertEqual(rcs, expected)

    def test_status_remote_gone_branch(self):
        rcs = gwsa.status.get_branches_status(self.crepo)
        # print gwsa.base.prettify(rcs)
        tb = self.crepo.remotes.origin.refs.feature2
        h = self.crepo.create_head("feature2", tb)
        h.set_tracking_branch(tb)
        rcs = gwsa.status.get_branches_status(self.crepo)
        # print gwsa.base.prettify(rcs)
        self.repo.delete_head(self.repo.heads["feature2"], "-D")
        self.crepo.remotes["origin"].fetch(prune=True)
        rcs = gwsa.status.get_branches_status(self.crepo)
        # print gwsa.base.prettify(rcs)
        expected = [
            {
                "active": True,
                "dirty": False,
                "name": "feature1",
                "remote": {"name": "origin/feature1", "valid": True},
            },
            {
                "active": False,
                "name": "feature2",
                "remote": {"name": "origin/feature2", "valid": False},
            },
        ]
        self.assertEqual(rcs, expected)

    def test_status_in_rebase(self):
        self.repo.heads["feature1"].checkout()
        try:
            self.repo.git.rebase("feature2")
        except:
            pass
        rcs = gwsa.status.get_branches_status(self.repo)
        # print gwsa.base.prettify(rcs)
        expected = [
            {
                "active": True,
                "dirty": True,
                "name": "feature1",
                "op_in_progress": "rebase",
            },
            {"active": False, "name": "feature2"},
            {"active": False, "name": "master"},
        ]
        self.assertEqual(rcs, expected)

    def test_status_in_cherry_pick(self):
        self.repo.heads["feature1"].checkout()
        try:
            self.repo.git.cherry_pick("feature2")
        except:
            pass
        rcs = gwsa.status.get_branches_status(self.repo)
        # print gwsa.base.prettify(rcs)
        expected = [
            {
                "active": True,
                "dirty": True,
                "name": "feature1",
                "op_in_progress": "cherry-pick",
            },
            {"active": False, "name": "feature2"},
            {"active": False, "name": "master"},
        ]
        self.assertEqual(rcs, expected)

    def test_status_in_merge(self):
        self.repo.heads["feature1"].checkout()
        try:
            self.repo.git.merge("feature2")
        except:
            pass
        rcs = gwsa.status.get_branches_status(self.repo)
        # print gwsa.base.prettify(rcs)
        expected = [
            {
                "active": True,
                "dirty": True,
                "name": "feature1",
                "op_in_progress": "merge",
            },
            {"active": False, "name": "feature2"},
            {"active": False, "name": "master"},
        ]
        self.assertEqual(rcs, expected)

    def test_status_forced_update(self):
        self.repo.heads["feature1"].checkout()
        self.repo.head.reset("HEAD~1", index=True, working_tree=True)
        add_commit(self.repo, "tt.txt")
        self.crepo.remotes["origin"].fetch(prune=True)
        rcs = gwsa.status.get_branches_status(self.crepo)
        # print gwsa.base.prettify(rcs)
        expected = [
            {
                "active": True,
                "dirty": False,
                "name": "feature1",
                "remote": {
                    "ahead": "1",
                    "behind": "1",
                    "forced-update": True,
                    "name": "origin/feature1",
                    "valid": True,
                },
            }
        ]
        self.assertEqual(rcs, expected)
