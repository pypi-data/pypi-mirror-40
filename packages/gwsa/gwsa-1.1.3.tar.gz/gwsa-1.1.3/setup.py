from setuptools import setup, find_packages
import os
import re

pkgname = "gwsa"


setup(
    name=pkgname,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="git workspace automation",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Version Control",
    ],
    url="https://gitlab.com/aanatoly/gwsa",
    author="Anatoly Asviyan",
    author_email="aanatoly@gmail.com",
    license="GPLv2",
    packages=find_packages(),
    install_requires=["gitpython", "blessed"],
    extras_require={"dev": ["tox", "cmarkgfm", "twine"]},
    entry_points={
        "console_scripts": [
            "%(pkgname)s = %(pkgname)s.__main__:main" % {"pkgname": pkgname}
        ]
    },
    zip_safe=False,
)
