"""Datastore models for beardo
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import logging

# third-party imports
from google.appengine.ext import ndb

# local imports
from app.models import base


class Build(base.BaseModel):

    project = ndb.KeyProperty()
    build_data = ndb.JsonProperty(compressed=True)

    @property
    def git_ref(self):
        return self.build_data['payload']['ref']

    @property
    def git_sha(self):
        return self.build_data['payload']['after']

    @property
    def success(self):
        return self.build_data.get('success', False)


# Repeatable queries are defined below in module level functions, this is just
# a personal preference, I think it makes the models a bit cleaner. Only
# behaviour that modifies the model gets implemented on the model directly.


def get(build_id):
    """Returns a single build instance, or None if not found.
    """
    try:
        build_id = int(build_id)
    except ValueError:
        logging.debug('Invalid build ID (Not a number): {0}'.format(build_id))
        return None
    return Build.get_by_id(build_id)


def get_latest_for_project(project_key):
    q = Build.query()
    q = q.filter(Build.project == project_key)
    q = q.order(-Build.created)
    return q.fetch(100)


def record_build(build_data):
    """Record a build log in the datastore
    """
    build = Build(
        project=ndb.Key('Project', build_data['payload']['repository']['name']),
        build_data=build_data,
    )
    return build.put().get()
