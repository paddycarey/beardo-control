"""Request handlers for user management in the beardo dashboard.
"""
# third-party imports
import webapp2
from google.appengine.api import users as aeusers
from nacelle.core.decorators import render_jinja2

# local imports
from app.forms import forms
from app.models import ssh_keys
from app.models import users
from app.utils.decorators import admin_required
from app.utils.decorators import login_required


@admin_required
@render_jinja2('users/list.html')
def users_list(request):
    """Render lists/pages of users that can be viewed/edited as required
    """
    cursor = request.params.get('cursor')
    sort_order = request.params.get('sort', '-created')
    results, next_cursor, sort_field, sort_asc = users.get_page(cursor=cursor, sort_order=sort_order)
    return {
        'results': results,
        'next_cursor': next_cursor,
        'cursor': cursor,
        'sort_field': sort_field,
        'sort_asc': sort_asc,
    }


@login_required
@render_jinja2('users/profile.html')
def users_profile(request, user_id):
    """User profile page. Non-admin users can only view their own profile.
    """
    # normalize user ID
    ouid = user_id
    if not aeusers.is_current_user_admin() and not user_id == 'me':
        return webapp2.redirect_to('users-profile', user_id='me')
    if user_id == 'me':
        user_id = request.user.user_id()

    user = users.get(user_id)
    keys = ssh_keys.get_all_for_user(user.key.id())
    return {'user_id': ouid, 'user': user, 'ssh_keys': keys}


@admin_required
def users_delete(request, user_id):
    """Delete user from datastore
    """
    user = users.get(user_id)
    if user is not None:
        user_email = user.email
        user.key.delete()
        request.session().add_flash('User deleted: {0}.'.format(user_email), level='danger')
    return webapp2.redirect_to('users-list')


@login_required
@render_jinja2('users/add_ssh_key.html')
def ssh_keys_add(request, user_id):
    """Handles the form to allow adding SSH keys.
    """
    # normalize user ID
    ouid = user_id
    if not aeusers.is_current_user_admin() and not user_id == 'me':
        return webapp2.redirect_to('users-profile', user_id='me')
    if user_id == 'me':
        user_id = request.user.user_id()
    user = users.get(user_id)

    # if form validates then save the object to the datastore
    form = forms.SSHKeyForm(request.POST)
    if request.method == 'POST' and form.validate():
        _err = False

        # ensure this key doesn't already exist in the system
        if ssh_keys.check_exists(form.ssh_key.data):
            _err = True
            _msg = 'SSH key already exists in the system.'
            try:
                form.errors['ssh_key'].append(_msg)
            except KeyError:
                form.errors['ssh_key'] = [_msg]

        if not _err:
            ssh_keys.add_for_user(user, form.title.data, form.ssh_key.data)
            session = request.session()
            session.add_flash('SSH key added: {0}'.format(form.title.data), level='success')
            return webapp2.redirect_to('users-profile', user_id=ouid)

    # render template with the form in the context
    return {'form': form, 'cancel_url': webapp2.uri_for('users-profile', user_id=ouid), 'user': user}


@login_required
def ssh_keys_delete(request, user_id, ssh_key_id):
    """Allow users to delete SSH keys.
    """
    # normalize user ID
    ouid = user_id
    if not aeusers.is_current_user_admin() and not user_id == 'me':
        return webapp2.redirect_to('users-profile', user_id='me')
    if user_id == 'me':
        user_id = request.user.user_id()
    user = users.get(user_id)

    # fetch key from datastore
    ssh_key = ssh_keys.get(ssh_key_id)

    # check if the user has permission to delete this key
    if not aeusers.is_current_user_admin() and not ssh_key.user == user.key:
        return webapp2.redirect_to('users-profile', user_id=ouid)

    # delete the key from the datastore
    ssh_keys.delete(ssh_key_id)
    session = request.session()
    session.add_flash('SSH key deleted: {0}'.format(ssh_key.title), level='success')
    return webapp2.redirect_to('users-profile', user_id=ouid)
