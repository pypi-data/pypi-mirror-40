from flask import jsonify, Blueprint, Flask
from werkzeug.exceptions import default_exceptions,\
    HTTPException, InternalServerError


def error_handling(error):
    if isinstance(error, HTTPException):
        result = {'code': error.code, 'description': error.description,
                  'message': str(error)}
    else:
        description = InternalServerError().description
        result = {'code': 500, 'description': description,
                  'message': str(error)}

    resp = jsonify(result)
    resp.status_code = result['code']
    return resp


class Json(Blueprint):
    app: Flask

    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None,
                 root_path=None):
        super(Json, self).__init__(name, import_name, static_folder,
                                   static_url_path, template_folder,
                                   url_prefix, subdomain,
                                   url_defaults, root_path)
        for code in default_exceptions.keys():
            self.register_error_handler(code, error_handling)

    def register(self, app, options, first_registration=False):
        super(Json, self).register(app, options, first_registration)
        self.app = app

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if view_func is not None:
            def _json(f):
                def __json(*args, **kw):
                    res = f(*args, **kw)
                    if isinstance(res, dict):
                        with self.app.app_context():
                            res = jsonify(res)
                    return res
                return __json

            view_func = _json(view_func)
        return super(Json, self).add_url_rule(rule, endpoint,
                                              view_func, **options)
