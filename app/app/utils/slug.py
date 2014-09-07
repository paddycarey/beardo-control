"""Single function that will slugify a string for use in IDs or URLs.
"""
# stdlib imports
import re
import unicodedata


def slugify(value):
    """Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """

    if isinstance(value, str):
        value = unicode(value)

    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)
