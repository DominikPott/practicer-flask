from flask import Blueprint, render_template

bp = Blueprint('model_viewer', __name__)


@bp.route('/models')
def model_viewer():
    return render_template("model_viewer.html")
