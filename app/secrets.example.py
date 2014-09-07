"""Sensitive credentials required at runtime but that cannot be checked into git.
"""
# future imports
from __future__ import absolute_import


# List of emails allowed to register whilst the site is in "invite-only" mode.
INVITE_LIST = [
    'test@example.com',
]

# Gitlab credentials
GITLAB_URL = 'http://gitlab.somedomain.com/api/v3'
GITLAB_EMAIL_SUFFIX = 'gitlab.somedomain.com'
GITLAB_API_TOKEN = '1a2b3c4d5e6f7g8h9i0j'
GITLAB_WEBHOOK_URL = 'https://some-app.appspot.com/_webhooks/push/'

GITLAB_DEPLOY_KEY = 'ssh-rsa somemadeupkey auser@adomain.com'

# Sentry credentials
SENTRY_DSN = None
