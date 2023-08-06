Fork Syncer -- Fsyncer
======================

|Travis Build|

.. |Travis Build| image:: https://travis-ci.org/Skarlso/fsyncer.svg?branch=master
   :target: https://travis-ci.org/Skarlso/fsyncer

This is a small python application to keep all your remote forks up-to-date.

Usage
=====

Installing
----------

::

    pip install fsyncer


Running
-------

From a cron job for example which runs every day / week / month...

::

    export FSYNC_GITHUB_TOKEN=<github_token_with_repo_access_scope>
    fsyncer


Filter Repositories
-------------------

It's possible to provide a list of repositories that Fsyncer should deal with.
In that case, the list of forks will be filtered down to the provided list.
That files location is `~/.config/fsyncer/.repo_list`.

Example::

    my_awesome_repo
    my_other_awesome_repo
    and_sync_this_one

In this case if there are other repositories for that user, they will all be
ignored and only these three will be synced.

Requirements
============

Fsynver runs `git` in the background on the given environment. If the installed
`git` can push to a repository then so can Fsyncer. Hence the requirement is
only to have a valid git client with properly set up credentials.

fsyncer also requires a token to be present on the current machine to gather
data, like remote forks and username.

This environment property is `FSYNC_GITHUB_TOKEN`.

Restrictions
============

Only forks can be updated which can be fast forwarded for now. Fsyncer will
not try to do git magic or trying to resolve merge conflicts. If the push
doesn't work, it will skip that repository and move on to the next one.

Future
========

Future plans include:

1. Creating a cron job with an optional parameter for the current user
2. Documentation
3. Support other VCSs

Contributions
=============

Are always welcomed.
