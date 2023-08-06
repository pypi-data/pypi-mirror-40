CLI
===

Generating new project
----------------------

Example usage:
::

   # This will generate a project directory
   # for your new microservice with Flask
   lair --project-name my-project

   # This will generate a  project directory
   # for your new microservice with Flask and SqlAlchemy,
   # and place an example modell in
   # project-dir/project_name/models/example.txt
   #  to use this as a model just rename from .txt to .py
   lair --project-name my-shiny-project --with-db

Database migration
------------------

Example initial workflow:
::

    # Initialize migration
    my-shiny-project db init

    # Create your models

    # Generate a new migration file
    my-shiny-project db migrate

    # Apply migration changes
    my-shiny-project db upgrade
