from flask import Flask, send_from_directory

import practicer_flask.exercises
from practicer_flask import log

app = Flask(__name__)


@app.route('/<path:filepath>')
def exercise_file(filepath):
    log.debug("Exercise_File: " + filepath)
    import os
    d = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    url = send_from_directory(d, filename, as_attachment=True)
    log.debug("Url:" + str(url))
    return url


app.register_blueprint(practicer_flask.exercises.bp)

if __name__ == "__main__":
    app.run()
