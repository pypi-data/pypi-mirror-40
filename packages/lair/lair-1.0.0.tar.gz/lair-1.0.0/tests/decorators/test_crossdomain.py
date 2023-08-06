from pyfakefs.fake_filesystem_unittest import TestCase
from lair.decorators import crossdomain
from datetime import timedelta
import flask


class TestCrossdomain(TestCase):
    app = None

    def setUp(self):
        self.app = flask.Flask("test-app")

    def test_default(self):
        @self.app.route('/')
        @crossdomain('*')
        def my_handler():
            return '[]'

        client = self.app.test_client()

        response = client.get('/')
        h = response.headers
        self.assertEqual(h.get('Access-Control-Allow-Origin'), '*')
        methods = sorted(h.get('Access-Control-Allow-Methods').split(', '))
        self.assertListEqual(methods, ['GET', 'HEAD'])
        self.assertEqual(int(h.get('Access-Control-Max-Age')), 21600)
        self.assertIsNone(h.get('Access-Control-Allow-Headers'))

    def test_domain(self):
        @self.app.route('/')
        @crossdomain(['test.domain.tld', 'test2.domain.tld'])
        def my_handler():
            return '[]'

        client = self.app.test_client()

        response = client.get('/')
        h = response.headers
        self.assertEqual(h.get('Access-Control-Allow-Origin'), 'test.domain.tld, test2.domain.tld')
        methods = sorted(h.get('Access-Control-Allow-Methods').split(', '))
        self.assertListEqual(methods, ['GET', 'HEAD'])
        self.assertEqual(int(h.get('Access-Control-Max-Age')), 21600)
        self.assertIsNone(h.get('Access-Control-Allow-Headers'))

    def test_only_post(self):
        @self.app.route('/')
        @crossdomain('*', methods=['POST'], max_age=timedelta(seconds=60))
        def my_handler():
            return '[]'

        client = self.app.test_client()

        response = client.get('/')
        h = response.headers
        self.assertEqual(h.get('Access-Control-Allow-Origin'), '*')
        methods = sorted(h.get('Access-Control-Allow-Methods').split(', '))
        self.assertListEqual(methods, ['POST'])
        self.assertEqual(int(h.get('Access-Control-Max-Age')), 60)
        self.assertIsNone(h.get('Access-Control-Allow-Headers'))

    def test_only_headers(self):
        @self.app.route('/')
        @crossdomain('*', methods=['POST'], headers=['x-random-header'])
        def my_handler():
            return '[]'

        client = self.app.test_client()

        response = client.get('/')
        h = response.headers
        self.assertEqual(h.get('Access-Control-Allow-Origin'), '*')
        methods = sorted(h.get('Access-Control-Allow-Methods').split(', '))
        self.assertListEqual(methods, ['POST'])
        self.assertEqual(int(h.get('Access-Control-Max-Age')), 21600)
        self.assertIsNotNone(h.get('Access-Control-Allow-Headers'))
        self.assertEqual(h.get('Access-Control-Allow-Headers'), 'X-RANDOM-HEADER')

    def test_options(self):
        @self.app.route('/', methods=['OPTIONS', 'GET'])
        @crossdomain('*', methods=['OPTIONS'], attach_to_all=False, automatic_options=False)
        def my_handler():
            return '[]'

        @self.app.route('/test', methods=['OPTIONS', 'GET'])
        @crossdomain('*', methods=['OPTIONS'])
        def my_test_handler():
            return '[]'

        client = self.app.test_client()

        response = client.options('/')
        h = response.headers
        self.assertEqual(h.get('Access-Control-Allow-Origin'), '*')
        methods = sorted(h.get('Access-Control-Allow-Methods').split(', '))
        self.assertListEqual(methods, ['OPTIONS'])
        self.assertEqual(int(h.get('Access-Control-Max-Age')), 21600)
        self.assertIsNone(h.get('Access-Control-Allow-Headers'))

        response = client.get('/')
        h = response.headers
        self.assertIsNone(h.get('Access-Control-Allow-Origin'))
        self.assertListEqual(methods, ['OPTIONS'])
        self.assertIsNone(h.get('Access-Control-Max-Age'))
        self.assertIsNone(h.get('Access-Control-Allow-Headers'))

        response = client.options('/test')
        h = response.headers
        self.assertEqual(h.get('Access-Control-Allow-Origin'), '*')
        methods = sorted(h.get('Access-Control-Allow-Methods').split(', '))
        self.assertListEqual(methods, ['OPTIONS'])
        self.assertEqual(int(h.get('Access-Control-Max-Age')), 21600)
        self.assertIsNone(h.get('Access-Control-Allow-Headers'))
