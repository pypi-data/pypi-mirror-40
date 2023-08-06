import os
from pyfakefs.fake_filesystem_unittest import TestCase
from lair.run import main
import lair


DEFAULT_DEPS = 'lair\nflask\nclick\nkonfig\n'
DB_DEPS = f'flask_migrate\nflask_sqlalchemy\nsqlalchemy\n{DEFAULT_DEPS}'

class TestRun(TestCase):
    def setUp(self):
        # We need all the template files
        # and now, I don't know better solution for that
        real_template_dir = os.path.join(
            os.path.dirname(lair.__file__),
            'templates')

        self.setUpPyfakefs()
        self.fs.add_real_directory(real_template_dir)

    def test_no_args(self):
        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 2)

    def test_project_name(self):
        main(['--project-name=test-project'])

        self.assertTrue(os.path.isdir('test-project'))
        self.assertTrue(os.path.isfile('test-project/requirements.txt'))

        with open('test-project/requirements.txt', 'r') as f:
            self.assertEqual(f.read(), DEFAULT_DEPS)

    def test_project_name_rerun(self):
        main(['--project-name=test-project'])

        self.assertTrue(os.path.isdir('test-project'))
        self.assertTrue(os.path.isfile('test-project/requirements.txt'))

        with open('test-project/requirements.txt', 'r') as f:
            self.assertEqual(f.read(), DEFAULT_DEPS)

        self.assertFalse(os.path.isfile('test-project/test_project/models/example.py'))

        with self.assertRaises(SystemExit) as cm:
            main(['--project-name=test-project'])

        self.assertEqual(cm.exception.code, 1)

    def test_with_database(self):
        main(['--project-name=test-project', '--with-db'])

        self.assertTrue(os.path.isdir('test-project'))
        self.assertTrue(os.path.isfile('test-project/requirements.txt'))

        with open('test-project/requirements.txt') as f:
            self.assertEqual(f.read(), DB_DEPS)

        self.assertTrue(os.path.isfile('test-project/test_project/models/example.py'))
