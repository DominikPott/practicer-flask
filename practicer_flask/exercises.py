from flask import Blueprint, render_template

import practicer_flask.exercise_inventory

bp = Blueprint('exercises', __name__, )


@bp.route('/')
def exercise():
    return render_template("exercises.html", exercises=practicer_flask.exercise_inventory.exercises())


