import os
import logging
import sys
from github import Github, Repository
from pathlib import Path
from subprocess import run, CalledProcessError
from typing import List


logging.basicConfig(filename='fsync.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger('fsync_logger')


def sync_list(repos: List[Repository.Repository]):
    """
    Syncs all forks for a given user.
    1: Clone the repository
    2: Setup upstream as the parent ssh url
    3: Do a fetch from the upstream
    4: Rebase
    5: Push

    This only works in case the remote fork isn't dirty / does not have changes
    that make it impossible to do a Fast forward.

    :param repos: Repository.Repository
        A List of repositories to sync.
    :return: None
    """
    logger.info("syncing %d forked repositories" % len(repos))
    for repo in repos:  # type: Repository.Repository
        try:
            logger.info("cloning into: %s" % repo.name)
            run(["git", "clone", repo.ssh_url, repo.name])
            # setup upstream for updating
            logger.info("setup upstream to %s" % repo.parent.ssh_url)
            upstream = "cd %s && git remote add upstream %s" % (repo.name, repo.parent.ssh_url)
            run(['/bin/bash', '-l', '-c', upstream])
            # do the update
            logger.info("doing the update with push")
            push = "cd %s && git fetch upstream && git rebase upstream/master && git push origin" % (repo.name)
            run(['/bin/bash', '-l', '-c', push])
            logger.info("successfully updated %s" % repo.name)
        except CalledProcessError:
            logger.info("failed updating {repo.name}")
        finally:
            run(["rm", "-fr", repo.name])


def get_repo_list() -> List[Repository.Repository]:
    """
    Gather a list of remote forks for a given user.
    Only repositories are selected for which the given user is an owner.
    This prevents the inclusion of Company based forks.

    :return: List[Repository.Repository]
        A list of remote forks for the current user.
    """
    g = Github(os.environ['FSYNC_GITHUB_TOKEN'])
    repos = []
    user = g.get_user()
    for repo in user.get_repos():
        if repo.fork and repo.owner.name == user.name:
            repos.append(repo)
    return repos


def main():
    """
    The main of fsyncer. Gathers the list of repositories to sync
    and filters them based on a `.repos_list` file that can be located
    under `~/.config/fsyncer/.repo_list`. This file contains a list
    of repository names which the user wishes to syncronize. Anything else
    will be ignored.
    :return: None
    """
    print(r'''
    (`-').->          <-. (`-')_           (`-')  _   (`-')
    ( OO)_      .->      \( OO) )_         ( OO).-/<-.(OO )
    (_)--\_) ,--.'  ,-.,--./ ,--/ \-,-----.(,------.,------,)
    /    _ /(`-')'.'  /|   \ |  |  |  .--./ |  .---'|   /`. '
    \_..`--.(OO \    / |  . '|  |)/_) (`-')(|  '--. |  |_.' |
    .-._)   \|  /   /) |  |\    | ||  |OO ) |  .--' |  .   .'
    \       /`-/   /`  |  | \   |(_'  '--'\ |  `---.|  |\  \
    `-----'   `--'    `--'  `--'   `-----' `------'`--' '--'

    Beginning syncing...
    ''')

    if "FSYNC_GITHUB_TOKEN" not in os.environ:
        print("Please set up a token by FSYNC_GITHUB_TOKEN=<token>.")
        sys.exit(1)

    repo_list = Path(os.path.join(Path.home(), '.config', 'fsyncer', '.repo_list'))
    only = []
    if repo_list.is_file():
        logger.info('found configuration file... syncing repos from file')
        with open(repo_list) as conf:
            for line in conf:
                only.append(line.strip())

    logger.info('retrieving forks for user')
    repos = get_repo_list()
    if len(only) > 0:
        repos = list(filter(lambda r: r.name in only, repos))

    sync_list(repos)
