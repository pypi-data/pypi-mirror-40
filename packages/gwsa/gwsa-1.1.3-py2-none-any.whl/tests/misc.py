import git
import os
import sys

count = 0


def create_repo(basedir, name):
    repodir = os.path.join(basedir, name)
    repo = git.Repo.init(repodir)
    add_commit(repo, "readme.md")
    repo.config_writer().set_value("user", "name", "vova").release()
    repo.config_writer().set_value("user", "email", "vova@gov.ru").release()
    return repo


def add_line(repo, path):
    rpath = os.path.join(repo.working_dir, path)
    c = get_count()
    with open(rpath, "a+") as f:
        f.write("hello %d\n" % c)
        f.flush()


def add_commit(repo, path):
    add_line(repo, path)
    repo.index.add([path])
    repo.index.commit("act %d" % get_count())


def get_count():
    global count
    count += 1
    return count


def fill_repo(repo):
    b1 = repo.create_head("feature1")
    b1.checkout()
    for i in range(5):
        add_commit(repo, "tt.txt")

    b2 = repo.create_head("feature2")
    b2.checkout()
    for i in range(5):
        add_commit(repo, "tt.txt")

    b1.checkout()
    for i in range(5):
        add_commit(repo, "tt.txt")
