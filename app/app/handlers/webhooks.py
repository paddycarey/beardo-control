"""Request handlers for beardo webhooks
"""
# third-party imports
import webapp2
from google.appengine.api import taskqueue
from nacelle.core.decorators import render_json

# local imports
from app.models import projects


@render_json
def push_hook(request, project_id):
    """Triggered when a push is made to an attached repo
    """

    # get project from datastore
    project = projects.get(project_id)
    if project is None:
        return webapp2.abort(404, detail="Project not found")

    # add build task to the queue
    q = taskqueue.Queue('build-queue')
    q.add(taskqueue.Task(payload=request.body, method='PULL'))

    # return 200 response
    return {'project': project}
