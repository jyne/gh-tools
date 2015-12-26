========
gh-tools
========
.. image:: https://travis-ci.org/robvanderleek/gh-tools.svg?branch=master
:target: https://travis-ci.org/robvanderleek/gh-tools

Collection of command line tools written in Python for GitHub exploration and mining.

------------
Installation
------------
There are a couple of ways to install this package. Pick one of the following:

1. Test-drive this package with `virtualenv`::

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/pypi gh-tools

2. Install this package under a user account::

    $ pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/pypi gh-tools --user

3. Install this package system-wide with `pip`::

    $ pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/pypi gh-tools

-----
Setup
-----

These tools query parts of the GitHub REST API that require authentication.
Therefore you need to create a file called .github-secret in your home 
directory. The content of this file should be an access token generated via
https://github.com/settings/tokens

Make sure this file is only accessible by its owner, for example ::

    -rw-------  1 rob  staff  41 Jul  5 20:28 /Users/rob/.github-secret

-----
Usage
-----

After installation these tools are available:

gt-query
    Query the GitHub search API

gt-clone
    Clone GitHub repositories

gt-xargs
    Analyze GitHub repositories

-----------
Development
-----------

For development and testing, install this package locally with ::

    $ ./setup.py install --user

(For the maintainer) Uploading the package to the PyPi test server ::

    $ ./setup.py sdist upload -r https://testpypi.python.org/pypi

Installing the package from the PyPi test server under a user account ::

    $ pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/pypi gh-tools --user

Upgrading the package from the PyPi test server under a user account ::

    $ pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/pypi gh-tools --user --upgrade
