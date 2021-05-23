from flask import Blueprint, render_template

import practicer_flask.exercise_inventory
import practicer_flask.user_exercise_stats.api as history_api

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
def dashboard():
    exercises = practicer_flask.exercise_inventory.exercises()
    history = history_api.exercise_histories(user=0)
    exercises_history = _map_exercises_to_history(history, exercises)
    return render_template("dashboard.html", exercises_history=exercises_history)


def _map_exercises_to_history(history, exercises):
    data = []
    for _, day, h_exercises in history:
        mapped_exercises = []
        for h_exercise in h_exercises:
            for exercise in exercises:
                if str(h_exercise) == exercise.get("uuid", None):
                    mapped_exercises.append(exercise)
                    break
        data.append([day, mapped_exercises])
    return data



