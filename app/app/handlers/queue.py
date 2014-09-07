"""Request handlers for the beardo build queue
"""
# stdlib imports
import json

# third-party imports
from nacelle.core.decorators import render_json
from nacelle.core.decorators import require_method

# local imports
from app.utils import build_queue as bq


@render_json
@require_method(['GET', 'POST'])
def build_queue(request):
    if request.method == 'GET':
        return bq.lease_task()
    return bq.complete_task(json.loads(request.body))
