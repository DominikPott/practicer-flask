from flask import Flask

from practicer import api

app = Flask(__name__)


@app.route('/')
def index():
    e = [e.get('label', "NoName") for e in api.exercises()]
    return "Exercises: " + "| ".join(e)


if __name__ == "__main__":
    app.run()
