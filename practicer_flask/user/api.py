import practicer_flask.user.postgres as db


def register(username, password):
    db.add_user(username, password)


def user(username):
    return db.user(username=username)
