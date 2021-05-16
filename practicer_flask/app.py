import os

from flask import Flask

import practicer_flask.exercises
import practicer_flask.dashboard
import practicer_flask.topic
import practicer_flask.model_viewer

app = Flask(__name__)

app.register_blueprint(practicer_flask.exercises.bp)
app.register_blueprint(practicer_flask.dashboard.bp)
app.register_blueprint(practicer_flask.topic.bp)
app.register_blueprint(practicer_flask.model_viewer.bp)


if __name__ == "__main__":
    app.run(debug=os.environ.get("DEV", False))
