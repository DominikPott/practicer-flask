from flask import Blueprint, render_template

import practicer.api

bp = Blueprint('exercises', __name__, )


@bp.route('/')
def exercise():
    return render_template("exercises.html", exercises=practicer.api.exercises())
