.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   This text does not appear on pypi or github. It is a comment.

================
buildout.environ
================

Expose system envionment variables into `zc.buildout <https://pypi.org/project/zc.buildout/>`_ section.

It is an extension for buildout.
All variables seen by Pythons ``os.environ`` are available in buildout.


Installation
------------

Install ``buildout.environ`` by adding it to your buildout extensions::

    [buildout]
    extensions = buildout.environment

Usage
-----

Use ``${__environ__:VARIABLENAME}`` to address any environment variable.

Example::

    [buildout]
    extensions = buildout.environ
    parts = print

    [print]
    recipe = mr.scripty
    install =
        print("Found in environ: PATH=${__environ__:PATH}")


Source Code
-----------

The sources are in a GIT DVCS with its main branches at `github <http://github.com/collective/buildout.environ>`_.
There you can report issue too.

We'd be happy to see many forks and pull-requests to make this addon even better.

Maintainers are `Jens Klein <mailto:jk@kleinundpartner.at>`_ and the BlueDynamics Alliance developer team.
We appreciate any contribution and if a release is needed to be done on pypi, please just contact one of us.
We also offer commercial support if any training, coaching, integration or adaptions are needed.


Contributions
-------------

Initial implementation by Jens W. Klein.

Further Authors:

- no others so far


License
-------

The project is licensed under Zope Public License (ZPL) Version 2.1
