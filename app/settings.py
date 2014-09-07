"""Local settings for the beardo control server
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import os

# third-party imports
import webapp2
from google.appengine.api import users

# local imports
from app.utils.misc import replace_query_param
from app.filters import date_helper
from app.filters import gravatar
from app.filters import tojson


# This directory
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Python dotted path to the routes for the app
ROUTES_MODULE = 'app.routes.ROUTES'

# Jinja variables/functions/filters to inject into all jinja templates
JINJA_SETTINGS = {
    'globals': {
        'enumerate': enumerate,
        'int': int,
        'is_current_user_admin': users.is_current_user_admin,
        'uri_for': webapp2.uri_for,
        'logout_url': users.create_logout_url,
        'replace_query_param': replace_query_param,
    },
    'filters': {
        'gravatar': gravatar.gravatar,
        'relative_date': date_helper.relative_date,
        'tojson': tojson.tojson_filter,
    }
}

# Enable/Disable public access
INVITE_ONLY = True

# Import sensitive data from the `secrets.py` module.
from secrets import *
