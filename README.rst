========
gh-tools
========

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
