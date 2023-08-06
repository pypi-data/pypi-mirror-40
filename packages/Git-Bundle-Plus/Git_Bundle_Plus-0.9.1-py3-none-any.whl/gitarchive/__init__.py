#!/usr/bin/env python

import sys
import os
from .git_cmd import Git
from .constants import Constants
import argparse

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

if __name__ == "__main__":
    default_dir = os.getcwd()
    parser = argparse.ArgumentParser(description="Bundle a local Git project with all uncommitted changes and stashes.")
    parser.add_argument("path", help="Git directory to archive", type=dir_path, default=default_dir)
    args = parser.parse_args()
    cwd = os.path.realpath(args.path)

    if Git.status(cwd) != 0:
        print("An error occured when performing `git status ...`")
        sys.exit()
    if Git.stash_list(cwd) != 0:
        print("An error occured when performing `git stash list`")
        sys.exit()
    Git.tag_refs(cwd) != 0
    stashcode = Git.stash(cwd)
    if stashcode == 0:
        Git.tag_ref(Constants.stash_tag_pattern.format("ga-latest"), "stash@{{0}}", cwd)
    if Git.bundle(cwd) != 0:
        print("An error occured when performing `git bundle ...`")
        sys.exit()
    Git.del_tag_refs(cwd, stashcode)
