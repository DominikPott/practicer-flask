import os
import random

from flask import Blueprint, render_template

import practicer_flask.exercise_inventory

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
def dashboard():
    exercises = practicer_flask.exercise_inventory.exercises()
    exercises = emulate_last_exercises(exercises)
    for exercise in exercises:
        path = exercise['path']
        directory = os.path.dirname(path)
        exercise['thumbnail'] = 'exercises/' + os.path.basename(os.path.dirname(directory)) + '/' + os.path.basename(
            directory) + '/' + exercise['thumbnail']
    return render_template("dashboard.html", exercises=exercises)


def emulate_last_exercises(exercises):
    last_exercise_count = random.randint(1, 10)
    random.shuffle(exercises)
    return exercises[:last_exercise_count]
