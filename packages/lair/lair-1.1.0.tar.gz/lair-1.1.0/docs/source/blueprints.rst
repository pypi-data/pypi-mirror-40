Blueprints
==========

Json Blueprint
--------------

::

    from lair.blueprints import Json as JsonBlueprint


    endpoint = JsonBlueprint('api', __name__)

    @endpoint.route('/')
    def index():
        return {'available': True}

