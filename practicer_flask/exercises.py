from flask import Blueprint, render_template

import practicer_flask.exercise_inventory
from practicer_flask import log

bp = Blueprint('exercises', __name__, )


@bp.route('/')
def exercise():
    import os
    exercises = practicer_flask.exercise_inventory.exercises()
    for exercise in exercises:
        path = exercise['path']
        directory = os.path.dirname(path)

        exercise['image'] = 'exercises/' + os.path.basename(os.path.dirname(directory)) + '/' + os.path.basename(
            directory) + '/' + exercise['thumbnail']
        log.debug(exercise['image'])
    return render_template("exercises.html", exercises=exercises)
