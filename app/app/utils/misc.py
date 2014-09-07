# stdlib imports
import urllib
import urlparse


def replace_query_param(url, key, val):
    """
    Given a URL and a key/val pair, set or replace an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = urlparse.urlsplit(url)
    query_dict = dict(urlparse.parse_qs(query))
    if val is None:
        try:
            del query_dict[key]
        except KeyError:
            pass
    else:
        query_dict[key] = val
    for k, v in query_dict.items():
        if isinstance(v, list):
            query_dict[k] = v[0]
    query = urllib.urlencode(query_dict.items())
    return urlparse.urlunsplit((scheme, netloc, path, query, fragment))
