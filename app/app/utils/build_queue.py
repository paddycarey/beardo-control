"""Collection of functions used to interact with the beardo build queue.
"""
# stdlib imports
import datetime
import json
import time

# third-party imports
from google.appengine.api import taskqueue
from google.appengine.runtime import DeadlineExceededError

# local imports
from app.models import builds


def _get_queue():
    return taskqueue.Queue('build-queue')


def lease_task(max_seconds=50):
    """Leases the next available task from the task queue.

    Blocks for `max_seconds` before returning if no tasks are found. Normally
    we would just catch appengine's DeadlineExceededError and clean up
    quickly, but we don't always get enough time to do so when using this
    method. Blocking for a max number of seconds allows the function to exit
    cleanly before otherwise being killed by the appengine scheduler.
    """
    # get a queue object we can use to check for tasks
    _q = _get_queue()
    # timestamp so we can record (roughly) how long we've been running.
    _ts = datetime.datetime.utcnow()

    try:
        while True:
            try:
                _task = _q.lease_tasks(600, 1)[0]
            except IndexError:
                if (datetime.datetime.utcnow() - _ts).seconds > max_seconds:
                    raise DeadlineExceededError
                time.sleep(1)
            else:
                return {
                    'task_name': _task.name,
                    'payload': json.loads(_task.payload),
                }
    except DeadlineExceededError:
        return {'error': 'task queue empty'}, 204


def complete_task(task_data):
    """Removes task from queue and stores build data/logs in the datastore.
    """
    # get a queue object we can use to mark the task completed
    _q = _get_queue()
    # delete the task from the queue
    _q.delete_tasks_by_name([task_data['task_name']])
    # record build data/logs in the datastore and return the stored data
    return builds.record_build(task_data)
