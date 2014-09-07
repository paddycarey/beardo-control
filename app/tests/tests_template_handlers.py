"""Tests for beardo-control frontend template handlers
"""
# third-party imports
import webapp2
from nacelle.app import wsgi
from nacelle.test.testcases import NacelleTestCase

# local imports
from .utils import _build_uri


class FrontendHandlerTests(NacelleTestCase):

    def test_index(self):
        """Test rendering the app's index page
        """
        # construct and make test request
        request = webapp2.Request.blank(_build_uri('login'))
        response = request.get_response(wsgi)
        # check response is as expected
        self.assertEqual(200, response.status_int)
