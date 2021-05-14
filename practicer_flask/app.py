import os

from flask import Flask

import practicer_flask.exercises
import practicer_flask.dashboard

app = Flask(__name__)

app.register_blueprint(practicer_flask.exercises.bp)
app.register_blueprint(practicer_flask.dashboard.bp)

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEV", False))
