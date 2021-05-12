from flask import Flask

import practicer_flask.exercises

app = Flask(__name__)

app.register_blueprint(practicer_flask.exercises.bp)

if __name__ == "__main__":
    app.run(debug=True)
