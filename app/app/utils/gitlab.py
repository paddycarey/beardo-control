# future imports
from __future__ import absolute_import

# stdlib imports
import json
import logging
import urllib
import uuid

# third-party imports
from nacelle.conf import settings

# local imports
from .network import make_request


class Gitlab(object):
    """Gitlab API wrapper.

    Wraps common operations performed in beardo, but does not have extensive
    coverage of the Gitlab API. Some functions may not act as you might expect
    from a simple API wrapper, these cases should be clearly noted in
    docstrings for the various methods.
    """

    def __init__(self):
        self.base_url = settings.GITLAB_URL
        self.email_suffix = settings.GITLAB_EMAIL_SUFFIX
        self.token = settings.GITLAB_API_TOKEN
        self.webhook_url = settings.GITLAB_WEBHOOK_URL

    def _request(self, url, **kwargs):
        """Authenticate requests to the Gitlab API using a private token.
        """
        headers = {'PRIVATE-TOKEN': self.token}
        response = make_request(self.base_url + url, headers=headers, **kwargs)
        logging.info('Requested: {0}'.format(url))
        logging.info('Method: {0}'.format(kwargs.get('method', 'GET')))
        logging.info(response.content)
        return json.loads(response.content)

    def _delete(self, url):
        """Make a DELETE request to the Gitlab API.
        """
        return self._request(url, method="DELETE")

    def _get(self, url):
        """Make a GET request to the Gitlab API.
        """
        return self._request(url)

    def _post(self, url, data=None):
        """Make a POST request to the Gitlab API.
        """
        if data is not None:
            data = urllib.urlencode(data)
        return self._request(url, method='POST', payload=data)

    def create_project(self, name):
        """Create a new project on Gitlab.
        """
        project = self._post('/projects', data={'name': name})
        self.create_project_hook(project['id'], self.webhook_url + name)
        return project

    def create_project_hook(self, project_id, url):
        """Create a new project hook on Gitlab.
        """
        return self._post('/projects/{0}/hooks'.format(project_id), data={'url': url})

    def delete_project(self, project_id):
        """Delete given project from Gitlab.
        """
        return self._delete('/projects/{0}'.format(project_id))

    def get_projects(self):
        """Fetch all projects from gitlab.
        """
        projects = []
        page = 1
        while not len(projects) % 100:
            projects += self._get('/projects?{0}'.format(urllib.urlencode({'per_page': 100, 'page': page})))
            page += 1
        return projects

    def _email_for_user_id(self, user_id):
        return '{0}@{1}'.format(user_id, self.email_suffix)

    def create_user(self, user_id):
        """Create gitlab user for this local user

        Note: The user_id passed in is not the same as Gitlab's user ID, it is
        the local datastore ID for the user.
        """
        data = {
            'email': self._email_for_user_id(user_id),
            'username': user_id,
            'password': str(uuid.uuid4()),
            'name': user_id,
        }

        # create user and return it to caller
        return self._post('/users', data=data)

    def delete_user(self, user_id):
        """Delete given user from Gitlab.
        """
        return self._delete('/users/{0}'.format(user_id))

    def get_users(self):
        """Fetch all registered users from gitlab.
        """
        users = []
        page = 1
        while not len(users) % 100:
            users += self._get('/users?{0}'.format(urllib.urlencode({'per_page': 100, 'page': page})))
            page += 1
        return users

    def get_user(self, user_id):
        """Fetch user from gitlab for this local user.

        Note: The user_id passed in is not the same as Gitlab's user ID, it is
        the local datastore ID for the user, which is used to derive a
        username which we look up using the gitlab API.
        """
        _email = self._email_for_user_id(user_id)
        response = self._get('/users?{0}'.format(urllib.urlencode({'search': _email})))
        for _user in response:
            if _user['email'] == _email:
                return _user
        return None

    def add_ssh_key(self, user_id, title, ssh_key):
        """Add SSH key to Gitlab.
        """
        _gu = self.get_user(user_id)
        if _gu is None:
            return None

        # build URL and make request
        return self._post(
            '/users/{0}/keys'.format(_gu['id']),
            data={'title': title, 'key': ssh_key},
        )

    def delete_ssh_key(self, user_id, key_id):
        """Remove remote SSH key from Gitlab.
        """

        _gu = self.get_user(user_id)
        if _gu is None:
            return None

        # build URL and make request
        return self._delete('/users/{0}/keys/{1}'.format(_gu['id'], key_id))

    def get_ssh_keys(self, user_id):
        """Fetch a user's SSH keys from Gitlab.
        """
        _gu = self.get_user(user_id)
        if _gu is None:
            return []

        # build URL and make request
        return self._get('/users/{0}/keys'.format(_gu['id']))
