CLI
===

Example usage:
::

   # This will generate a project directory
   # for your new microservice with Flask
   lair --project-name my-shiny-project

   # This will generate a  project directory
   # for your new microservice with Flask and SqlAlchemy,
   # and place an example modell in
   # project-dir/project_name/models/example.txt
   #  to use this as a model just rename from .txt to .py
   lair --project-name my-shiny-project --with-db
