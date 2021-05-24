from flask import Blueprint, render_template

import practicer_flask.exercise_inventory
import practicer_flask.user_exercise_stats.api as statistics_api

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
def dashboard():
    exercises = practicer_flask.exercise_inventory.exercises()
    history = statistics_api.history(user=0)
    exercises_history = _map_exercises_to_history(history, exercises)
    streak = statistics_api.streak(user=0)
    return render_template("dashboard.html", exercises_history=exercises_history, streak=streak)


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



