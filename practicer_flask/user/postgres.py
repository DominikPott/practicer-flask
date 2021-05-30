import os

import psycopg2
import psycopg2.extras


def get_db():
    url = os.environ.get('DATABASE_URL', None)
    if url:
        con = psycopg2.connect(url, sslmode='require')
    else:
        con = psycopg2.connect(host="localhost", database="statistics", user="postgres", password="test")
    return con


def create_table():
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS userdata (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
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
        delete_table_query = 'DROP TABLE userdata'
        cursor.execute(delete_table_query)
        db.commit()
    except psycopg2.Error as e:
        print("Error while deleting table", e)
    finally:
        if db:
            cursor.close()
            db.close()


def add_user(username, password):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        query = """
        INSERT INTO userdata (username, password) VALUES (%s, %s)
        ON CONFLICT (username)
        DO NOTHING;
        """
        userdata = cursor.execute(query, (username, password))
        db.commit()
        return userdata
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if db:
            cursor.close()
            db.close()


def user(username):
    db = None
    try:
        db = get_db()
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM userdata WHERE username = %s', (username,))
        return cursor.fetchone()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if db:
            cursor.close()
            db.close()


if __name__ == "__main__":
    drop_table()
    create_table()
    #add_user(username='dome', password='password')
    #data = user('dome')

