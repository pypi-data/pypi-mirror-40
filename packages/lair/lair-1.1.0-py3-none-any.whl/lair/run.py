import sys
import argparse
from lair.project_generator import ProjectGenerator


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Service Example')
    parser.add_argument('--project-name', help='Name of the project',
                        type=str, default=None, required=True)
    parser.add_argument('--with-db',
                        help='With database', nargs='?',
                        const=True, default=False, required=False)
    args = parser.parse_args(args=args)

    dependencies = []

    if args.with_db:
        dependencies.extend(['flask_migrate',
                             'flask_sqlalchemy',
                             'sqlalchemy'])

    # Make sure flask is below flask_sqlalchemy in the list
    # otherwise it fails to install because 'flask is missing'
    dependencies.extend(['lair', 'flask', 'click', 'konfig'])

    app = ProjectGenerator()
    app.set('project-name', args.project_name)
    app.set('with-db', args.with_db)
    app.set('dependencies', dependencies)

    try:
        app.initialize()
    except FileExistsError as e:
        print("!!!", e)
        sys.exit(1)
    app.create()
