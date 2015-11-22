========
gh-tools
========
[![Build Status](https://travis-ci.org/robvanderleek/gh-tools.svg?branch=master)](https://travis-ci.org/robvanderleek/gh-tools)

Collection of command line tools written in Python for GitHub exploration and 
data mining.

------------
Installation
------------

You can install gh-tools with `pip`::

    $ pip install gh-tools

-----
Usage
-----

These tools query parts of the GitHub REST API that require authentication.
Therefore you need to create a file called .github-secret in your home 
directory. The content of this file should be an access token generated via
https://github.com/blog/1509-personal-api-tokens

-----------
Development
-----------

For development and testing, install this package locally with ::

    $ ./setup.py install --user

Uploading the package to the PyPi test server ::

    $ python setup.py sdist upload -r https://testpypi.python.org/pypi

Installing the package from the PyPi test server under a user account ::

    $ pip install -i https://testpypi.python.org/pypi gh-tools --user
