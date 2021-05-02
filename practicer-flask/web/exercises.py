from flask import Blueprint, render_template

from practicer.api import exercises

bp = Blueprint('exercises', __name__, )


@bp.route('/')
def exercise():
    return render_template("exercises.html", exercises=exercises())
