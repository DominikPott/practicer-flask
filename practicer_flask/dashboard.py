from flask import Blueprint, render_template, g

from practicer_flask.auth import login_required
import practicer_flask.exercise_inventory
import practicer_flask.user_exercise_stats.api as statistics_api

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
@bp.route("/dashboard/<exercise_uuid>")
@login_required
def dashboard(exercise_uuid=None):
    user = g.user['id']
    if exercise_uuid:
        statistics_api.increase_experience(user=user, exercise=exercise_uuid)
        statistics_api.increase_streak(user=user)
        exercise_ = practicer_flask.exercise_inventory.exercise_from_uuid(exercise_uuid)
        statistics_api.add_exercise_to_history(user=user, exercise=exercise_)

    streak = statistics_api.streak(user=user)
    history = statistics_api.history(user=user)
    exercises = practicer_flask.exercise_inventory.exercises()
    exercises_history = _map_exercises_to_history(history, exercises)
    experiences = statistics_api.experience(user=user)
    exercises = enrich_exercises_with_experiences(exercises, experiences)
    return render_template("dashboard.html", exercises=exercises, exercises_history=exercises_history, streak=streak)


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


def enrich_exercises_with_experiences(exercises, experiences):
    for exercise in exercises:
        uuid = exercise.get('uuid', None)
        if not uuid:
            raise KeyError("No uuid in exercise " + exercise['label'])
        exercise_exp = experiences.get(uuid, 0)
        exercise['exp'] = {"angle": exercise_exp * 36}
    return exercises

