from flask import Flask

from .route import main

def create_app(config_file='setting.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(main)

    return app
