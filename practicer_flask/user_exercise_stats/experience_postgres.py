import json
import os
import psycopg2


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
            CREATE TABLE IF NOT EXISTS level (
                user_id INT NOT NULL PRIMARY KEY,
                level JSON NOT NULL
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


def _drop_table():
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        delete_table_query = 'DROP TABLE level'
        cursor.execute(delete_table_query)
        db.commit()
    except psycopg2.Error as e:
        print("Error while deleting table", e)
    finally:
        if db:
            cursor.close()
            db.close()


def update_exp(user, exp):
    exp_json = json.dumps(exp)
    query = """
    INSERT INTO level (user_id, level) VALUES (%s, %s)
    ON CONFLICT (user_id) DO UPDATE
        SET level=EXCLUDED.level;
    """
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, (user, exp_json))
        db.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        if db:
            cursor.close()
            db.close()


def level(user):
    cmd = 'SELECT level FROM level WHERE user_id = %s'
    exp = query_(cmd, (user,))
    if not exp:
        return {}
    else:
        return exp[0]


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
    _drop_table()
    _create_table()

    '''
    import uuid
    for _ in range(4):
        user = 0
        print('Level: ', level(user=user))

        raw_data = {str(uuid.uuid4()): 0,
                    str(uuid.uuid4()): 3}

        update_exp(user=user, exp=raw_data)
        print('Level New: ', level(user=user))
    '''