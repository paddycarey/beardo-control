"""This module provides a `tojson` template filter.

Totally stolen from Flask (https://github.com/mitsuhiko/flask/blob/01e831f08279d69f29984abf74c0eeaa12579915/flask/json.py).
"""
# stdlib imports
import json

# third-party imports
from jinja2 import Markup
from nacelle.core.utils.encoder import ModelEncoder


# Figure out if simplejson escapes slashes. This behavior was changed
# from one version to another without reason.
_slash_escape = '\\/' not in json.dumps('/')


def htmlsafe_dumps(obj, **kwargs):
    """Works exactly like :func:`dumps` but is safe for use in ``<script>``
tags. It accepts the same arguments and returns a JSON string. Note that
this is available in templates through the ``|tojson`` filter which will
also mark the result as safe. Due to how this function escapes certain
characters this is safe even if used outside of ``<script>`` tags.

The following characters are escaped in strings:

- ``<``
- ``>``
- ``&``
- ``'``

This makes it safe to embed such strings in any place in HTML with the
notable exception of double quoted attributes. In that case single
quote your attributes or HTML escape it in addition.

This function's return value is now always safe for HTML usage, even
if outside of script tags or if used in XHTML. This rule does not
hold true when using this function in HTML attributes that are double
quoted. Always single quote attributes if you use the ``|tojson``
filter. Alternatively use ``|tojson|forceescape``.
"""
    rv = json.dumps(obj, cls=ModelEncoder) \
        .replace(u'<', u'\\u003c') \
        .replace(u'>', u'\\u003e') \
        .replace(u'&', u'\\u0026') \
        .replace(u"'", u'\\u0027')
    if not _slash_escape:
        rv = rv.replace('\\/', '/')
    return rv


def htmlsafe_dump(obj, fp, **kwargs):
    """Like :func:`htmlsafe_dumps` but writes into a file object."""
    fp.write(unicode(htmlsafe_dumps(obj, **kwargs)))


def tojson_filter(obj, **kwargs):
    return Markup(htmlsafe_dumps(obj, **kwargs))
