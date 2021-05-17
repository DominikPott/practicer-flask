import os
import random

from flask import Blueprint, render_template

import practicer_flask.exercise_inventory

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
def dashboard():
    exercises = practicer_flask.exercise_inventory.exercises()
    for exercise in exercises:
        path = exercise['path']
        directory = os.path.dirname(path)
        exercise['thumbnail'] = 'exercises/' + os.path.basename(os.path.dirname(directory)) + '/' + os.path.basename(
            directory) + '/' + exercise['thumbnail']

    exercises_history = emulate_days(exercises)
    return render_template("dashboard.html", exercises_history=exercises_history)


def emulate_days(exercises):
    exercises_days = []
    for day in range(365):
        day = emulate_previous_day(day)
        exercises_days.append((day, emulate_last_exercises(exercises)))
    return exercises_days


def emulate_last_exercises(exercises):
    last_exercise_count = random.randint(0, 5)
    random.shuffle(exercises)
    return exercises[:last_exercise_count]


def emulate_previous_day(day):
    import datetime
    date = datetime.date.today()
    date = date - datetime.timedelta(days=day)
    return date.strftime("%Y.%m.%d")
