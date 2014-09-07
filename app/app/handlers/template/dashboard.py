"""Request handlers for the beardo dashboard
"""
# third-party imports
import webapp2
from google.appengine.api import users as aeusers
from nacelle.core.decorators import render_jinja2

# local imports
from app.models import users
from app.utils.decorators import login_required


@render_jinja2('dashboard/login.html')
def login(request):
    request.user = aeusers.get_current_user()
    request.beardo_user = users.get(request.user)
    session = request.session()
    next_url = session.get('next_url', webapp2.uri_for('users-profile', user_id='me'))
    return {'login_url': aeusers.create_login_url(next_url)}


@login_required
@render_jinja2('dashboard/dashboard.html')
def dashboard(request):
    """Main beardo dashboard page
    """
    return {}
