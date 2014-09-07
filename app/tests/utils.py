# future imports
from __future__ import absolute_import

# stdlib imports
import base64
import json

# third-party imports
import webapp2
from nacelle.app import wsgi


def _build_uri(name, *args, **kwargs):
    _request = webapp2.Request.blank('/')
    _uri = wsgi.router.build(_request, name, args, kwargs)
    return _uri


def _run_tasks(taskq_stub, q_name):
    """Since nose runs our tests single threaded, appengine can't run tests in
    the background, thus we need to run them manually at the appropriate point
    during our tests.
    """
    tasks = taskq_stub.GetTasks(q_name)
    taskq_stub.FlushQueue(q_name)
    while tasks:
        for task in tasks:
            params = base64.b64decode(task["body"])
            yield _make_test_request(
                task["url"],
                post_data=params,
                headers=[('X-AppEngine-TaskName', 'task1')],
                method='POST',
            )
        tasks = taskq_stub.GetTasks(q_name)
        taskq_stub.FlushQueue(q_name)


def _assert_json_response(testcase, response, status, checkdata):
    """Convenience function used to quickly check a JSON response.

    Params:
        - testcase: unittest.TestCase
        - response: webapp2.Response
        - status: int
        - checkdata: dict

    This function asserts the following:
        - 'Content-Type' header is 'application/json'
        - Response body contains valid JSON data
        - Response status matches the `status` parameter
        - checkdata is a valid subset of the response data
    """
    response_dict = json.loads(response.body)
    testcase.assertEqual(response.headers['Content-Type'], 'application/json')
    testcase.assertIsInstance(response_dict, dict)
    testcase.assertEqual(response.status_int, status)
    for key, value in checkdata.items():
        testcase.assertIn(key, response_dict)
        testcase.assertEqual(response_dict[key], value)


def _make_test_request(url, post_data=None, headers=None, method='GET'):
    """Make a test request against the app
    """
    request = webapp2.Request.blank(url, POST=post_data, headers=headers)
    request.method = method
    return request.get_response(wsgi)
