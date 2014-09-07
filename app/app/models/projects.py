"""Datastore models for beardo
"""
# future imports
from __future__ import absolute_import

# third-party imports
import webapp2
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

# local imports
from app.models import base
from app.utils import gitlab
from app.utils import name_gen


class Project(base.BaseModel):

    name = ndb.StringProperty()
    namespace = ndb.IntegerProperty(default=4)

    project_info = ndb.JsonProperty(default=None)

    @property
    def git_url(self):
        return self.project_info.get('ssh_url_to_repo', None)

    def _pre_put_hook(self):
        if self.project_info is None:
            gitlab_client = gitlab.Gitlab()
            self.project_info = gitlab_client.create_project(self.name)

    @classmethod
    def _post_delete_hook(cls, key, future):
        sync_projects_async()

    def _post_put_hook(self, future):
        sync_projects_async()


# Repeatable queries are defined below in module level functions, this is just
# a personal preference, I think it makes the models a bit cleaner. Only
# behaviour that modifies the model gets implemented on the model directly.


def get(project_id):
    """Returns a single project instance, or None if not found.
    """
    return base.get(Project, project_id, _coerce=str)


def create():
    """Create a new project in the datastore with a random name
    """
    project_name = name_gen.generate()
    project = Project(id=project_name, name=project_name)
    return project.put().get()


def get_page(cursor=None, sort_order='name'):
    """Retrieves a page of projects from the datastore
    """
    valid_sort_orders = ['created', 'name']
    return base.get_page(Project, cursor=cursor, sort_order=sort_order, valid_sort_orders=valid_sort_orders)


def get_all():
    """Fetch all projects from the datastore. Primarily used during sync.
    """
    projects = []
    next_cursor = None
    while True:
        results, next_cursor, _, _ = get_page(cursor=next_cursor)
        projects += list(results)
        if not next_cursor or not results:
            break
    return projects


# Utility functions

def sync_projects():
    """Sync projects between the datastore and gitlab.

    Any projects present in the datastore which don't exist in gitlab will be
    created as required. Projects present in gitlab but not in the datastore
    will be deleted from gitlab.
    """

    # get an API client we can use to interact with our Gitlab instance
    gitlab_client = gitlab.Gitlab()

    # fetch lists of users from both the datastore and gitlab
    remote_projects = gitlab_client.get_projects()
    local_projects = get_all()

    # add missing projects (those that exist locally) to gitlab
    for _lp in local_projects:
        if not _lp.key.id() in (x['name'] for x in remote_projects):
            gitlab_client.create_project(_lp.key.id())

    # remove orphaned projects (those that don't exist locally) from gitlab
    for _rp in remote_projects:
        if not _rp['name'] in (x.key.id() for x in local_projects):
            gitlab_client.delete_project(_rp['id'])


def sync_projects_async():
    """Enqueues a task that syncs projects with gitlab in the background.
    """
    taskqueue.add(
        url=webapp2.uri_for('tasks-gitlab-sync-projects'),
        queue_name='gitlab-sync',
    )
