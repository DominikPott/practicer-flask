import collections

from flask import Blueprint, render_template

import practicer_flask.exercise_inventory

bp = Blueprint('exercises', __name__, )


@bp.route('/')
def exercise():
    categories = collections.OrderedDict()
    for exercise in practicer_flask.exercise_inventory.exercises():
        categories.setdefault(exercise.get('categories', ['no categorie'])[0], []).append(exercise)
    return render_template("exercises.html", categories=categories)
