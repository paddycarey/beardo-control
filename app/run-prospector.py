#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Prospector runner for beardo-control
"""
# stdlib imports
import sys

# third-party imports
from prospector import run

# this looks like an unused import, but we're only using it to do some path
# manipulation on import so you can safely ignore it (even though your linter
# may complain)
import appengine_config

# setup our appengine environment so we can import the libs we need for our tests,
# we need to do this first so we can import the stubs from testbed
from nacelle.test.environ import setup_environ
setup_environ()


if __name__ == '__main__':

    sys.argv = [sys.argv[0]]
    sys.argv += ['--no-autodetect', '--ignore-paths', 'vendor']
    run.main()
