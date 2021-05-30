import os

from flask import Flask

import practicer_flask.auth
import practicer_flask.exercises
import practicer_flask.dashboard
import practicer_flask.topic
import practicer_flask.model_viewer


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(SECRET_KEY='dev')

    app.register_blueprint(practicer_flask.auth.bp)
    app.register_blueprint(practicer_flask.exercises.bp)
    app.register_blueprint(practicer_flask.dashboard.bp)
    app.register_blueprint(practicer_flask.topic.bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEV", False))
