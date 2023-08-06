import os
from datetime import datetime
from jinja2 import Environment, PackageLoader, TemplateNotFound
from typing import Dict, Any


class ProjectGenerator:
    __properties: Dict[str, Any]
    __jinja_env: Environment
    __root: str

    def __init__(self):
        self.__root = None
        self.__properties = {}
        self.__jinja_env = Environment(
            loader=PackageLoader('lair', 'templates'),
        )

    def set(self, name, value):
        self.__properties[name] = value

    def get(self, name) -> Any:
        return self.__properties.get(name, None)

    def root(self):
        return self.__root

    def render(self, file_path: str, **variables):
        target = os.path.join(self.root(), file_path)\
                        .replace('{module-name}', self.get('module-name'))

        if os.path.isfile(target):
            raise FileExistsError('File already exists: %s' % target)

        template_file = file_path.replace('/', '_')
        if template_file[0] == '.':
            template_file = '_' + template_file[1:]
        template_file = "%s.j2" % template_file

        try:
            template = self.__jinja_env.get_template(template_file)
        except TemplateNotFound:
            template = None

        with open(target, 'w') as f:
            if template is not None:
                f.write(template.render(**variables))
            else:
                f.write('\n')

    def initialize(self):
        self.__root = os.path.join(os.getcwd(), self.get('project-name'))
        if os.path.isdir(self.root()):
            raise FileExistsError('Project directory already'
                                  'exists: %s' % self.root())

        self.set('module-name', self.get('project-name').replace('-', '_'))

        globals = {
            'project_name': self.get('project-name'),
            'module_name': self.get('module-name'),
            'now': datetime.utcnow(),
            'with_db': self.get('with-db'),
        }
        self.__jinja_env.globals.update(globals)

    def create(self):
        os.mkdir(self.root(), 0o0755)

        # Files in project root
        self.render('Makefile')
        self.render('setup.py')
        self.render('requirements.txt', dependencies=self.get('dependencies'))
        self.render('MANIFEST.in')
        self.render('tox.ini')
        self.render('.travis.yml')
        self.render('README.rst')
        self.render('.gitignore')
        self.render('.coveragerc')

        # Test
        os.makedirs(os.path.join(self.root(), 'tests', 'endpoints'))
        self.render('tests/__init__.py')
        self.render('tests/endpoints/__init__.py')
        self.render('tests/endpoints/test_main.py')
        self.render('test-requirements.txt')

        # Docs
        os.makedirs(os.path.join(self.root(), 'docs', 'source', '_static'))
        self.render('docs/Makefile')
        self.render('docs/source/index.rst')
        self.render('docs/source/conf.py')
        self.render('docs/source/_static/.gitkeep')

        # Source
        os.makedirs(os.path.join(self.root(),
                                 self.get('module-name'),
                                 'endpoints'))
        self.render('{module-name}/settings.ini')
        self.render('{module-name}/run.py')
        self.render('{module-name}/app.py')
        self.render('{module-name}/__init__.py')
        self.render('{module-name}/endpoints/__init__.py')
        self.render('{module-name}/endpoints/main.py')

        if self.get('with-db'):
            self.render('{module-name}/database.py')
            os.makedirs(os.path.join(self.root(),
                                     self.get('module-name'),
                                     'models'))
            self.render('{module-name}/models/__init__.py')
            self.render('{module-name}/models/example.py')
