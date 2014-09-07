"""Base datastore models and queries for beardo-control
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import logging

# third-party imports
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    """Common data/operations for all storage models
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

    def to_dict(self):
        """Serialise model instance to a dictionary (to make it play nice with
        json.dumps())
        """
        d = super(BaseModel, self).to_dict()
        d['id'] = self.key.id()
        return d


# Collection of reusable query functions that can easily be used with any model

def get(model, entity_id, _coerce=None):
    """Returns a single model instance, or None if not found.
    """
    if _coerce is None:
        _coerce = lambda x: x
    try:
        entity_id = _coerce(entity_id)
    except ValueError:
        logging.debug('Invalid ID (Unable to coerce): {0}'.format(entity_id))
        return None
    return model.get_by_id(entity_id)


def _get_sort_order(model, sort_order, valid_sort_orders):
    """Parse a string repr of sort order into something we can use in an ndb query.
    """
    _fname = sort_order.lstrip('-')
    _so = getattr(model, _fname, None)
    if _so is None or _fname not in valid_sort_orders:
        logging.warning('{0} is not a valid sort order, defaulting to `{1}`'.format(sort_order, valid_sort_orders[0]))
        return getattr(model, valid_sort_orders[0]), _fname, True
    if sort_order.startswith('-'):
        return -_so, _fname, False
    return _so, _fname, True


def get_page(model, cursor=None, sort_order=None, page_size=20, valid_sort_orders=None):
    """Retrieves a page of records from the datastore
    """
    # set default valid sort orders if none specified
    if not valid_sort_orders:
        valid_sort_orders = ['created', 'modified']
    # default sort order should be the first valid order if none specified
    if sort_order is None:
        sort_order = valid_sort_orders[0]

    sort_order, sort_field, sort_asc = _get_sort_order(model, sort_order, valid_sort_orders)
    cursor = Cursor(urlsafe=cursor) if cursor else None

    q = model.query()
    q = q.order(sort_order)
    results, next_cursor, more = q.fetch_page(page_size, start_cursor=cursor)
    if not more:
        next_cursor = None
    if next_cursor is not None:
        next_cursor = next_cursor.urlsafe()
    return results, next_cursor, sort_field, sort_asc
