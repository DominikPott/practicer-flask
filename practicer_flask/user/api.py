import practicer_flask.user_exercise_stats.postgres as postgres


def register():
    pass


def login(user, password):
    pass


def logout(user):
    pass


def create_table():
    query = """CREATE TABLE IF NOT EXISTS user (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        );
        """
    postgres.create_table(table=query)


if __name__ == "__main__":
    postgres.drop_table(table='user')
    create_table()
