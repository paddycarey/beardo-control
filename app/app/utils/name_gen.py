"""Utilities used for generating random project names.
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import os
import random

# third-party imports
from nacelle.conf import settings

# local imports
from app.utils.slug import slugify


def _random_line(filename):
    """Returns a random line from a text file.
    """
    path = os.path.join(settings.ROOT_DIR, 'data', filename)
    with open(path, 'r') as f:
        line = next(f)
        for num, aline in enumerate(f):
            if random.randrange(num + 2):
                continue
            line = aline
    return line


def _get_adj():
    """Returns a random adjective from file.
    """
    return _random_line('adjectives.txt')


def _get_noun():
    """Returns a random noun from file.
    """
    return _random_line('nouns.txt')


def generate():
    # originally from: https://gist.github.com/1266756
    # with some changes. example output: "falling-violet-d27b3a"
    _hex = "0123456789abcdef"
    return (
        slugify(_get_adj()) + "-" +
        slugify(_get_noun()) + "-" +
        random.choice(_hex) + random.choice(_hex) + random.choice(_hex) +
        random.choice(_hex) + random.choice(_hex) + random.choice(_hex)
    )
