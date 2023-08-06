from pyfakefs.fake_filesystem_unittest import TestCase
from lair.blueprints import Json as JsonBlueprint
import flask
import json


class TestJson(TestCase):
    app = None

    def setUp(self):
        self.app = flask.Flask("test-app")
        self.bp = JsonBlueprint('test', __name__)

    def test_default(self):
        @self.bp.route('/')
        def my_handler():
            return {'valid_endpoint': True}

        self.app.register_blueprint(self.bp)

        client = self.app.test_client()
        response: flask.Response = client.get('/')
        body = response.data
        content = json.loads(body)

        self.assertTrue('valid_endpoint' in content)
        self.assertTrue(content['valid_endpoint'])

    def test_error_404(self):
        @self.bp.route('/')
        def my_handler():
            flask.abort(404)

        self.app.register_blueprint(self.bp)

        client = self.app.test_client()
        response: flask.Response = client.get('/')
        body = response.data
        content = json.loads(body)

        self.assertTrue('code' in content)
        self.assertTrue('message' in content)
        self.assertTrue('description' in content)
        self.assertEqual(content['code'], 404)
        message = 'The requested URL was not found on the server. '\
                  ' If you entered the URL manually please check '\
                  'your spelling and try again.'
        self.assertEqual(content['description'], message)
        self.assertEqual(content['message'], "404 Not Found: %s" % message)

    def test_error_404_custom(self):
        @self.bp.route('/')
        def my_handler():
            flask.abort(404, "It's not there")

        self.app.register_blueprint(self.bp)

        client = self.app.test_client()
        response: flask.Response = client.get('/')
        body = response.data
        content = json.loads(body)

        self.assertTrue('code' in content)
        self.assertTrue('message' in content)
        self.assertTrue('description' in content)
        self.assertEqual(content['code'], 404)
        message = "It's not there"
        self.assertEqual(content['description'], message)
        self.assertEqual(content['message'], "404 Not Found: %s" % message)

    def test_error_500_custom(self):
        @self.bp.route('/')
        def my_handler():
            flask.abort(500, "Something went wrong")

        self.app.register_blueprint(self.bp)

        client = self.app.test_client()
        response: flask.Response = client.get('/')
        body = response.data
        content = json.loads(body)

        self.assertTrue('code' in content)
        self.assertTrue('message' in content)
        self.assertTrue('description' in content)
        self.assertEqual(content['code'], 500)
        message = "Something went wrong"
        self.assertEqual(content['description'], message)
        self.assertEqual(content['message'], "500 Internal Server Error: %s" % message)

    def test_error_exception(self):
        @self.bp.route('/')
        def my_handler():
            raise Exception('Something went wrong again')

        self.app.register_blueprint(self.bp)

        client = self.app.test_client()
        response: flask.Response = client.get('/')
        body = response.data
        content = json.loads(body)

        self.assertTrue('code' in content)
        self.assertTrue('message' in content)
        self.assertTrue('description' in content)
        self.assertEqual(content['code'], 500)
        message = "The server encountered an internal error and was "\
                  "unable to complete your request.  "\
                  "Either the server is overloaded "\
                  "or there is an error in the application."
        # message = "Something went wrong again"
        self.assertEqual(content['description'], message)
        self.assertEqual(content['message'], "Something went wrong again")
