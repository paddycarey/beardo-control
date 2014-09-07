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
from app.models import ssh_keys
from app.utils import gitlab


class User(base.BaseModel):

    email = ndb.StringProperty(required=True)

    @classmethod
    def _post_delete_hook(cls, key, future):
        sync_users_async()

    def _post_put_hook(self, future):
        sync_users_async()


# Repeatable queries are defined below in module level functions, this is just
# a personal preference, I think it makes the models a bit cleaner. Only
# behaviour that modifies the model gets implemented on the model directly.


def get(user_id):
    """Returns a single user instance, or None if not found.
    """
    return base.get(User, user_id, _coerce=str)


def get_or_create(aeuser):
    """Given an appengine.api.user.User instance, retrieves a user object
    from the datastore. A user record will be created if one is not found.
    """
    if aeuser is None:
        return None
    user = get(aeuser.user_id())
    # create a user if necessary.
    if user is None:
        user = User(id=str(aeuser.user_id()), email=aeuser.email())
        user = user.put().get()
    return user


def get_page(cursor=None, sort_order='email'):
    """Retrieves a page of users from the datastore
    """
    valid_sort_orders = ['created', 'email']
    return base.get_page(User, cursor=None, sort_order=sort_order, valid_sort_orders=valid_sort_orders)


def get_all():
    """Fetch all users from the datastore. Primarily used during sync.
    """
    users = []
    next_cursor = None
    while True:
        results, next_cursor, _, _ = get_page(cursor=next_cursor)
        users += list(results)
        if not next_cursor or not results:
            break
    return users


# Utility functions

def sync_users():
    """Sync Users between the datastore and gitlab.

    Any users present in the datastore which don't exist in gitlab will be
    created as required. Users present in gitlab but not in the datastore
    will be deleted from gitlab. Users with administrator status in Gitlab
    will not be deleted.
    """

    # get an API client we can use to interact with our Gitlab instance
    gitlab_client = gitlab.Gitlab()

    # fetch lists of users from both the datastore and gitlab
    remote_users = gitlab_client.get_users()
    local_users = get_all()

    # add missing users (those that exist locally) to gitlab
    for _lu in local_users:
        if not _lu.key.id() in (x['username'] for x in remote_users):
            gitlab_client.create_user(_lu.key.id())
            ssh_keys.sync_ssh_keys_async(_lu.key.id())

    # remove orphaned users (those that don't exist locally) from gitlab
    for _ru in remote_users:
        if not _ru['username'] in (x.key.id() for x in local_users):
            if _ru['is_admin']:
                continue
            gitlab_client.delete_user(_ru['id'])


def sync_users_async():
    """Enqueues a task that syncs users with gitlab in the background.
    """
    taskqueue.add(
        url=webapp2.uri_for('tasks-gitlab-sync-users'),
        queue_name='gitlab-sync',
    )
