import os
import psycopg2
import datetime


def get_db():
    url = os.environ.get('DATABASE_URL', None)
    if url:
        con = psycopg2.connect(url, sslmode='require')
    else:
        con = psycopg2.connect(host="localhost", database="statistics", user="postgres", password="test")
    return con


def _create_table():
    try:
        db = get_db()
        cursor = db.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS streak (
                user_id INT NOT NULL PRIMARY KEY,
                length INT NOT NULL,
                last_day DATE NOT NULL
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
        delete_table_query = 'DROP TABLE streak'
        cursor.execute(delete_table_query)
        db.commit()
    except psycopg2.Error as e:
        print("Error while deleting table", e)
    finally:
        if db:
            cursor.close()
            db.close()


def update_streak(user, streak):
    query = """
    INSERT INTO streak (user_id, length, last_day) VALUES (%s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE
        SET length=EXCLUDED.length, last_day=EXCLUDED.last_day;
    """
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, (user, streak[0], streak[1]))
        db.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        if db:
            cursor.close()
            db.close()


def streak(user):
    cmd = 'SELECT * FROM streak WHERE user_id = %s'
    result = query_(cmd, (user,))
    if not result:
        result = [0, datetime.date.today()]
    else:
        result = list(result[1:])
    return result


def query_(cmd, args):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(cmd, args)
        return cursor.fetchone()
    except psycopg2.Error as e:
        print(e)
    finally:
        if db:
            cursor.close()
            db.close()


if __name__ == "__main__":
    drop_table()
    _create_table()

    """
    for _ in range(4):
        user = 0
        old_streak = streak(user)
        print("Old: ", old_streak)
        old_streak[0] += 1
        old_streak[1] = old_streak[1] + datetime.timedelta(days=1)
        update_streak(user, old_streak)
        print("New", streak(user))
    """