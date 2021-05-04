from flask import Blueprint, render_template

import exercise_inventory

bp = Blueprint('exercises', __name__, )


@bp.route('/')
def exercise():
    return render_template("exercises.html", exercises=exercise_inventory.exercises())


