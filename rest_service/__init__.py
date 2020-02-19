import os

from flask import Flask


def create_app(config: dict = None) -> Flask:
    """Create Flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(

        # Non-production SECRET_KEY
        SECRET_KEY='dev',

        # Default database
        DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'db.sqlite')
    )

    if config is None:
        # Load config from ././instance/application.cfg'
        app.config.from_pyfile('application.cfg', silent=True)
    else:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import database
    database.init_app(
        app, default_values=app.config.get('DB_DEFAULT_VALUES'))

    from . import api
    app.register_blueprint(api.bp)

    return app
