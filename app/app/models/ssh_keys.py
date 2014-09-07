"""Datastore models for beardo
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import hashlib

# third-party imports
import webapp2
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

# local imports
from app.models import base
from app.utils import gitlab


class SSHKey(base.BaseModel):

    user = ndb.KeyProperty()
    title = ndb.StringProperty()
    ssh_key = ndb.StringProperty()

    def _post_put_hook(self, future):
        _uid = future.get_result().get().user.id()
        sync_ssh_keys_async(_uid)

    @classmethod
    def _pre_delete_hook(cls, key):
        _uid = key.get().user.id()
        sync_ssh_keys_async(_uid)


# Repeatable queries are defined below in module level functions, this is just
# a personal preference, I think it makes the models a bit cleaner. Only
# behaviour that modifies the model gets implemented on the model directly.


def delete(ssh_key_id):
    """Delete a single SSH key instance
    """
    ssh_key = get(ssh_key_id)
    if ssh_key is None:
        return None
    ssh_key.key.delete()


def get(ssh_key_id):
    """Returns a single SSH key instance, or None if not found.
    """
    return base.get(SSHKey, ssh_key_id, _coerce=str)


def check_exists(ssh_key):
    """Check if the given SSH key already exists.
    """
    _id = hashlib.sha1(ssh_key.split()[1]).hexdigest()
    return get(_id) is not None


def add_for_user(user, title, ssh_key):
    """Create and store a new model instance from a validated form.
    """
    # create new record from passed in data and store it
    entity = SSHKey(id=hashlib.sha1(ssh_key.split()[1]).hexdigest(), user=user.key, title=title, ssh_key=ssh_key)
    return entity.put().get()


def get_all_for_user(user_id):
    """Retrieves a page of users from the datastore
    """
    q = SSHKey.query().filter(SSHKey.user == ndb.Key('User', user_id))
    return q.order(SSHKey.created).fetch(1000)


# Utility functions

def sync_ssh_keys(user_id):
    """Sync SSH keys between the datastore and gitlab for the given user.

    Any keys present in the datastore which don't exist in gitlab will be
    created as required. Keys present in gitlab but not in the datastore
    will be deleted from gitlab.
    """

    # get an API client we can use to interact with our Gitlab instance
    gitlab_client = gitlab.Gitlab()

    # fetch lists of ssh keys from both the datastore and gitlab
    remote_keys = gitlab_client.get_ssh_keys(user_id)
    local_keys = get_all_for_user(user_id)

    # add missing keys (those that exist locally) to gitlab
    for _lk in local_keys:
        if _lk.ssh_key not in (x['key'] for x in remote_keys):
            gitlab_client.add_ssh_key(user_id, _lk.title, _lk.ssh_key)

    # remove orphaned keys (those that don't exist locally) from gitlab
    for _rk in remote_keys:
        if _rk['key'] not in (x.ssh_key for x in local_keys):
            gitlab_client.delete_ssh_key(user_id, _rk['id'])


def sync_ssh_keys_async(user_id):
    """Enqueues a task that syncs ssh keys with gitlab in the background.
    """
    taskqueue.add(
        url=webapp2.uri_for('tasks-gitlab-sync-ssh-keys', user_id=user_id),
        queue_name='gitlab-sync',
    )
