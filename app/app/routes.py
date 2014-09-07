"""All route definitions for the beardo control server
"""
# third-party imports
from nacelle.core.routes import MultiPrefixRoute
from webapp2 import Route
from webapp2_extras.routes import RedirectRoute


ROUTES = [

    # Dashboard routes
    MultiPrefixRoute(
        handler_pfx='app.handlers.template.dashboard.',
        routes=[

            Route(r'/', 'login', name='login'),
            RedirectRoute(r'/_/', 'dashboard', name='dashboard', strict_slash=True),

        ],
    ),

    # Project management routes
    MultiPrefixRoute(
        handler_pfx='app.handlers.template.projects.',
        path_pfx='/_/projects',
        routes=[

            RedirectRoute(r'/', 'projects_list', name='projects-list', strict_slash=True),
            RedirectRoute(r'/new/', 'projects_add', name='projects-add', strict_slash=True),
            RedirectRoute(r'/<project_id>/', 'projects_edit', name='projects-edit', strict_slash=True),
            RedirectRoute(r'/<project_id>/delete/', 'projects_delete', name='projects-delete', strict_slash=True),
            RedirectRoute(r'/<project_id>/<build_id>/', 'build_view', name='build-view', strict_slash=True),

        ],
    ),

    # User/key management routes
    MultiPrefixRoute(
        handler_pfx='app.handlers.template.users.',
        path_pfx='/_/users',
        routes=[

            RedirectRoute(r'/', 'users_list', name='users-list', strict_slash=True),
            RedirectRoute(r'/<user_id>/', 'users_profile', name='users-profile', strict_slash=True),
            RedirectRoute(r'/<user_id>/add-key/', 'ssh_keys_add', name='ssh-keys-add', strict_slash=True),
            RedirectRoute(r'/<user_id>/delete-key/<ssh_key_id>/', 'ssh_keys_delete', name='ssh-keys-delete', strict_slash=True),
            RedirectRoute(r'/<user_id>/delete/', 'users_delete', name='users-delete', strict_slash=True),

        ],
    ),

    # Task routes
    Route(r'/_tasks/gitlab/sync/projects/', 'app.handlers.tasks.gitlab.sync_projects', name='tasks-gitlab-sync-projects'),
    Route(r'/_tasks/gitlab/sync/ssh_keys/<user_id>/', 'app.handlers.tasks.gitlab.sync_ssh_keys', name='tasks-gitlab-sync-ssh-keys'),
    Route(r'/_tasks/gitlab/sync/users/', 'app.handlers.tasks.gitlab.sync_users', name='tasks-gitlab-sync-users'),

    # Webhook routes
    MultiPrefixRoute(
        handler_pfx='app.handlers.webhooks.',
        path_pfx='/_webhooks',
        routes=[
            Route(r'/push/<project_id>', 'push_hook', name='push-hook'),
        ],
    ),

    # Build queue routes
    Route(r'/_build/queue/', 'app.handlers.queue.build_queue', name='build-queue'),

]
