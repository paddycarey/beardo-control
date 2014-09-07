"""
Taskqueue handlers for gitlab interaction

Handlers in this module will almost always return 200 responses, even in
situations where another status code may be appropriate. This is because
appengine will automatically retry any task that returns with a non-2xx status
code.
"""
# future imports
from __future__ import absolute_import

# third-party imports
from nacelle.core.decorators import login_task
from nacelle.core.decorators import render_json

# local imports
from app.models import projects
from app.models import ssh_keys
from app.models import users


@render_json
@login_task
def sync_projects(request):
    """Sync project data with gitlab.
    """
    projects.sync_projects()
    return {'status': 'success'}


@render_json
@login_task
def sync_ssh_keys(request, user_id):
    """Sync ssh key data with gitlab for a single user.
    """
    ssh_keys.sync_ssh_keys(user_id)
    return {'status': 'success'}


@render_json
@login_task
def sync_users(request):
    """Sync user data with gitlab.
    """
    users.sync_users()
    return {'status': 'success'}
