"""Request handlers for project management in the beardo dashboard.
"""
# third-party imports
import webapp2
from nacelle.core.decorators import render_jinja2

# local imports
from app.models import builds
from app.models import projects
from app.utils.decorators import login_required


@login_required
@render_jinja2('projects/list.html')
def projects_list(request):
    """Render lists/pages of projects that can be viewed/edited as required
    """
    cursor = request.params.get('cursor')
    sort_order = request.params.get('sort', 'name')
    results, next_cursor, sort_field, sort_asc = projects.get_page(cursor=cursor, sort_order=sort_order)
    return {
        'results': results,
        'next_cursor': next_cursor,
        'cursor': cursor,
        'sort_field': sort_field,
        'sort_asc': sort_asc,
    }


@login_required
def projects_add(request):
    """Creates a new project and saves details in the datastore.
    """
    project = projects.create()
    return webapp2.redirect_to('projects-edit', project_id=project.key.id())


@login_required
@render_jinja2('projects/overview.html')
def projects_edit(request, project_id=None):
    """Show project overview
    """
    project = projects.get(project_id)
    if project is None:
        return webapp2.abort(404, detail="Project not found")
    build_logs = builds.get_latest_for_project(project.key)
    return {'project': project, 'build_logs': build_logs, 'cancel_url': webapp2.uri_for('projects-list')}


@login_required
@render_jinja2('projects/build_log.html')
def build_view(request, project_id, build_id):
    """View a given build log
    """
    project = projects.get(project_id)
    if project is None:
        return webapp2.abort(404, detail="Project not found")
    build = builds.get(build_id)
    if build is None:
        return webapp2.abort(404, detail="Build not found")
    if not project.key == build.project:
        return webapp2.abort(404, detail="Build not found")
    return {'project': project, 'build_log': build, 'cancel_url': webapp2.uri_for('projects-list')}


@login_required
def projects_delete(request, project_id):
    """Delete project from datastore
    """
    project = projects.get(project_id)
    if project is not None:
        project_name = project.name
        project.key.delete()
        request.session().add_flash('Project deleted: {0}.'.format(project_name), level='danger')
    return webapp2.redirect_to('projects-list')
