# future imports
from __future__ import absolute_import

# stdlib imports
import hashlib
import urllib


def gravatar(email, size=40):
    """Convert an email address into a gravatar URL
    """
    gravatar_url = "http://www.gravatar.com/avatar/"
    gravatar_url += hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'s': str(size)})
    return gravatar_url
