from pyfakefs.fake_filesystem_unittest import TestCase
from lair.project_generator import ProjectGenerator
import lair
import os


class TestProjectGenerator(TestCase):
    pg: ProjectGenerator

    def setUp(self):
        self.pg = ProjectGenerator()
        # We need all the template files
        # and now, I don't know better solution for that
        real_template_dir = os.path.join(
            os.path.dirname(lair.__file__),
            'templates')

        self.setUpPyfakefs()
        self.fs.add_real_directory(real_template_dir)

    def test_properties(self):
        self.assertIsNone(self.pg.get('project-name'))

        self.pg.set('project-name', 'test-project')
        self.assertIsNotNone(self.pg.get('project-name'))
        self.assertEqual(self.pg.get('project-name'), 'test-project')

    def test_initializer(self):
        self.assertIsNone(self.pg.root())
        self.assertIsNone(self.pg.get('project-name'))
        self.assertIsNone(self.pg.get('module-name'))

        self.pg.set('project-name', 'test-project')
        self.pg.initialize()
        self.assertIsNotNone(self.pg.root())
        self.assertIsNotNone(self.pg.get('project-name'))
        self.assertIsNotNone(self.pg.get('module-name'))
        self.assertEqual(self.pg.get('project-name'), 'test-project')
        self.assertEqual(self.pg.get('module-name'), 'test_project')

    def test_create(self):
        self.pg.set('project-name', 'test-project')
        self.pg.set('dependencies', ['flask'])
        self.pg.set('with-db', True)
        self.pg.initialize()
        self.pg.create()

        self.assertTrue(os.path.isdir('test-project'))
        self.assertTrue(os.path.isfile('test-project/setup.py'))

        with open('test-project/requirements.txt', 'r') as f:
            self.assertEqual(f.read(), 'flask\n')

    def test_project_directory_exists(self):
        self.pg.set('project-name', 'test-project')
        os.mkdir('test-project')
        with self.assertRaises(FileExistsError):
            self.pg.initialize()

    def test_re_render_file(self):
        self.pg.set('project-name', 'test-project')
        self.pg.initialize()
        os.mkdir('test-project')
        self.pg.render('setup.py')
        with self.assertRaises(FileExistsError):
            self.pg.render('setup.py')
