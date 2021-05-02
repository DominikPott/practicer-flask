from flask import Flask, send_from_directory
import exercises

app = Flask(__name__)


@app.route('/exercises/<path:filepath>')
def exercise_file(filepath):
    import os
    d = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    url = send_from_directory(d, filename, as_attachment=True)
    return url


app.register_blueprint(exercises.bp)

if __name__ == "__main__":
    app.run()
