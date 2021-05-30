import practicer_flask.user.postgres as db


def register(username, password):
    db.add_user(username, password)


def user(username):
    userdata = db.user(username=username)
    return userdata


if __name__ == "__main__":
    data = user('adina')
    print(data)
