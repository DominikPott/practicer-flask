from flask import Flask, url_for

import practicer_flask.exercises
from practicer_flask import log

app = Flask(__name__)

app.register_blueprint(practicer_flask.exercises.bp)

if __name__ == "__main__":
    app.run()
