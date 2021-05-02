from flask import Flask, send_from_directory


def run(exercises):
    app = Flask(__name__)

    @app.route('/exercises/<path:filepath>')
    def exercise_file(filepath):
        import os
        d = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        url = send_from_directory(d, filename, as_attachment=True)
        return url

    from . import exercises as e
    app.register_blueprint(e.bp)

    app.run(debug=True)
