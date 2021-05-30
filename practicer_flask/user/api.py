import practicer_flask.user.postgres as db


def register(username, password):
    db.add_user(username, password)


def user(username):
    return db.user(username=username)


def user_from_id(id):
    return db.user_by_id(id=id)


if __name__ == "__main__":
    data = user('adina')
    print(data)
