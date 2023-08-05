import unittest
import gwsa
import gwsa.base
import tempfile
import shutil
import git
import os
import sys
from misc import *


class MyProgressPrinter(git.RemoteProgress):
    def __init__(self):
        git.RemoteProgress.__init__(self)
        self.count = 0

    def update(self, op_code, cur_count, max_count=None, message=""):
        self.count += 1


class FetchTest(unittest.TestCase):
    def setUp(self):
        self.count = 0
        self.basedir = tempfile.mkdtemp()
        self.repo = create_repo(self.basedir, "repo1")
        fill_repo(self.repo)
        self.crepo = self.repo.clone(os.path.join(self.basedir, "repo2"))

    def tearDown(self):
        shutil.rmtree(self.basedir)

    def test_remote_has_updates(self):
        rem = self.crepo.remote()
        rem.fetch()
        rcs = gwsa.base.get_remote_has_updates(rem)
        # print gwsa.base.prettify(rcs)
        self.assertEqual(rcs, False)

        add_commit(self.repo, "tt.txt")
        add_commit(self.repo, "tt1.txt")
        rcs = gwsa.base.get_remote_has_updates(rem)
        # print gwsa.base.prettify(rcs)
        self.assertEqual(rcs, True)

        rem.fetch()
        rcs = gwsa.base.get_remote_has_updates(rem)
        # print gwsa.base.prettify(rcs)
        self.assertEqual(rcs, False)

    def test_remote_has_updates_with_progress(self):
        rem = self.crepo.remote()
        rem.fetch()
        pr = MyProgressPrinter()
        rcs = gwsa.base.get_remote_has_updates(rem, progress=pr)
        self.assertEqual(rcs, False)
        self.assertEqual(pr.count, 0)

        add_commit(self.repo, "tt.txt")
        add_commit(self.repo, "tt1.txt")
        pr = MyProgressPrinter()
        rcs = gwsa.base.get_remote_has_updates(rem, progress=pr)
        self.assertEqual(rcs, True)
        self.assertNotEqual(pr.count, 0)

        rem.fetch()
        pr = MyProgressPrinter()
        rcs = gwsa.base.get_remote_has_updates(rem, progress=pr)
        self.assertEqual(rcs, False)
        self.assertEqual(pr.count, 0)

    def test_fetch_with_progress(self):
        rem = self.crepo.remote()

        pr = MyProgressPrinter()
        rem.fetch(progress=pr)
        self.assertEqual(pr.count, 0)

        add_commit(self.repo, "tt.txt")
        add_commit(self.repo, "tt1.txt")
        pr = MyProgressPrinter()
        rem.fetch(progress=pr)
        self.assertNotEqual(pr.count, 0)

        pr = MyProgressPrinter()
        rem.fetch(progress=pr)
        self.assertEqual(pr.count, 0)
