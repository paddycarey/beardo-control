"""Authorization decorators used to enforce login for the beardo dashboard.
"""
# stdlib imports
import logging

# third-party imports
import webapp2
from google.appengine.api import users as aeusers
from nacelle.conf import settings

# local imports
from app.models import users


# default routes used for redirection on auth failure
ADMIN_UNAUTHED_URL = 'dashboard'
LOGGEDIN_UNAUTHED_URL = 'login'


def admin_required(view_method):
    """Decorator that enforces admin login for wrapped handler functions.
    """
    def _arguments_wrapper(request, *args, **kwargs):

        # fail fast if the user's not an admin
        request.user = aeusers.get_current_user()
        if not aeusers.is_current_user_admin():
            return webapp2.redirect_to(ADMIN_UNAUTHED_URL)

        # get a user record from the datastore, creating one if necessary
        request.beardo_user = users.get_or_create(request.user)
        return view_method(request, *args, **kwargs)

    return _arguments_wrapper


def login_required(view_method):
    """Decorator that enforces login for wrapped handler functions.
    """
    def _arguments_wrapper(request, *args, **kwargs):

        # store current url in the session so we can redirect back to the
        # current url if required
        session = request.session()
        session['next_url'] = request.path_qs

        # ensure user is logged in via appengine user's service
        request.user = aeusers.get_current_user()
        if request.user is None:
            logging.info('User not logged in')
            return webapp2.redirect_to(LOGGEDIN_UNAUTHED_URL)

        # fetch datastore record for user if one already exists
        request.beardo_user = users.get(request.user.user_id())

        # create a datastore record if user is not stored but is on the invite list
        if settings.INVITE_ONLY and request.beardo_user is None and request.user.email() in settings.INVITE_LIST:
            request.beardo_user = users.get_or_create(request.user)

        # create a datastore record if registration is open to the public
        if aeusers.is_current_user_admin() or not settings.INVITE_ONLY:
            request.beardo_user = users.get_or_create(request.user)

        # if we still don't have a datastore record then user should not be allowed access
        if request.beardo_user is None:
            logging.info('User record not found')
            return webapp2.redirect_to(LOGGEDIN_UNAUTHED_URL)

        # call the view function
        return view_method(request, *args, **kwargs)

    return _arguments_wrapper
