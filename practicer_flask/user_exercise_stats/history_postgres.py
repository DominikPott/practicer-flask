import os
import uuid

import psycopg2
import psycopg2.extras
import psycopg2.extensions

psycopg2.extras.register_uuid()


def get_db():
    url = os.environ.get('DATABASE_URL', None)
    if url:
        con = psycopg2.connect(url, sslmode='require')
    else:
        con = psycopg2.connect(host="localhost", database="statistics", user="postgres", password="test")
    return con


def _connection_info():
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        print("PostgreSQL server information")
        print(db.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if db:
            cursor.close()
            db.close()
            print("PostgreSQL connection is closed")


def _create_table():
    db=None
    try:
        db = get_db()
        cursor = db.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS history (
                user_id INT NOT NULL,
                date DATE NOT NULL,
                exercise_ids UUID [] NOT NULL,
                PRIMARY KEY (user_id, date)
                );
                '''
        cursor.execute(create_table_query)
        db.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if db:
            cursor.close()
            db.close()


def drop_table():
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        delete_table_query = '''DROP TABLE history'''
        cursor.execute(delete_table_query)
        db.commit()
    except psycopg2.Error as e:
        print("Error while deleting table", e)
    finally:
        if db:
            cursor.close()
            db.close()


def add_exercise(user, date, exercise_uuid):
    query = """
    INSERT INTO history (user_id, date, exercise_ids) VALUES (%s, %s, ARRAY [%s])
    ON CONFLICT (user_id, date) DO UPDATE
        SET exercise_ids = history.exercise_ids || EXCLUDED.exercise_ids
    """
    exercise_uuid = uuid.UUID(exercise_uuid)
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, (user, date, exercise_uuid))
        db.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        if db:
            cursor.close()
            db.close()


def exercieses(user):
    cmd = 'SELECT * FROM history WHERE user_id = %s'
    return query_(cmd, (user,))


def exercises_for_date(user, date):
    cmd = 'SELECT * FROM history WHERE user_id = %s AND date = %s'
    return query_(cmd, (user, date))


def query_(cmd, args):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(cmd, args)
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(e)
    finally:
        if db:
            cursor.close()
            db.close()


if __name__ == "__main__":
    drop_table()
    _create_table()
    

