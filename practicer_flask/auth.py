from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import practicer_flask.user.api as user_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = user_db.user(username=username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard.dashboard'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif user_db.user(username=username) is not None:
            error = f"User {username} is already registered."
        if error is None:
            user_db.register(username=username, password=generate_password_hash(password))
            return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')
