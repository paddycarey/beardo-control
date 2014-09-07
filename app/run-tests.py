#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test runner for beardo-control
"""
# stdlib imports
import os
import sys

# third-party imports
import nose

# this looks like an unused import, but we're only using it to do some path
# manipulation on import so you can safely ignore it (even though your linter
# may complain)
import appengine_config

# setup our appengine environment so we can import the libs we need for our tests,
# we need to do this first so we can import the stubs from testbed
from nacelle.test.environ import setup_environ
setup_environ()


if __name__ == '__main__':

    res = nose.run(argv=[
        'run-tests.py',
        '-v',
        '--with-coverage',
        '--cover-erase',
        '--cover-package=app',
        '--cover-xml',
        '--cover-xml-file=/output/coverage.xml',
        '--with-xunit',
        '--xunit-file=/output/nosetests.xml',
        '--with-yanc',
        '--logging-level=INFO'
    ])
    os.remove('/app/.coverage')
    sys.exit(int(not res))
