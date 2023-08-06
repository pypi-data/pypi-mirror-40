from flask import Flask, Blueprint

from .parsers import _iter_parsers


def create_app(config={}):
    app = Flask(__name__)
    app.config.update(config)
    blueprint = create_blueprint()
    app.register_blueprint(blueprint)
    return app


def create_blueprint():
    # The import name on this isn't right - I think flask will have trouble
    # using the url_for method with the blueprint's routes.
    bp = Blueprint(name='parse', import_name=__name__, url_prefix="/parse")
    for parser in _iter_parsers():
        bp.add_url_rule(
            rule=parser.endpoint(),
            view_func=parser.view_function
        )
    return bp

soupstars_blueprint = create_blueprint()
