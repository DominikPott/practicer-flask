from flask import Blueprint, render_template

import practicer_flask.exercise_inventory
from practicer_flask import log

bp = Blueprint('exercises', __name__, )


@bp.route('/')
def exercise():
    import os
    exercises = practicer_flask.exercise_inventory.exercises()
    categories = {}
    for exercise in exercises:
        path = exercise['path']
        directory = os.path.dirname(path)
        exercise['thumbnail'] = 'exercises/' + os.path.basename(os.path.dirname(directory)) + '/' + os.path.basename(
            directory) + '/' + exercise['thumbnail']
        exercise['template'] = 'exercises/' + os.path.basename(os.path.dirname(directory)) + '/' + os.path.basename(
            directory) + '/' + exercise['template']
        categories.setdefault(exercise.get('categories', ['no categorie'])[0], []).append(exercise)

    return render_template("exercises.html", categories=categories)
