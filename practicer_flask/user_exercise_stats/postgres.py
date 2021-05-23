import os
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


def add_exercise(user, date, exercise):
    query = """
    INSERT INTO history (user_id, date, exercise_ids) VALUES (%s, %s, ARRAY [%s])
    ON CONFLICT (user_id, date) DO UPDATE
        SET exercise_ids = history.exercise_ids || EXCLUDED.exercise_ids
    """
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, (user, date, exercise))
        db.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        if db:
            cursor.close()
            db.close()

def get_exercieses(user):
    query = 'SELECT * FROM history WHERE user_id = %s AND date = %s'

def get_exercises_for_date(user, date):
    query = 'SELECT * FROM history WHERE user_id = %s AND date = %s'
    return

def query(cmd, **kwargs):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(cmd, (user, date))
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(e)
    finally:
        if db:
            cursor.close()
            db.close()

def crud():
    try:
        connection = get_db()
        cursor = connection.cursor()
        # Executing a SQL query to insert data into  table
        insert_query = """INSERT INTO history (MODEL, PRICE) VALUES ('Iphone12', 1100)"""
        cursor.execute(insert_query)
        connection.commit()
        print("1 Record inserted successfully")
        # Fetch result
        cursor.execute("SELECT * from mobile")
        record = cursor.fetchall()
        print("Result ", record)

        # Executing a SQL query to update table
        update_query = """Update mobile set price = 1500 where id = 1"""
        cursor.execute(update_query)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record updated successfully ")
        # Fetch result
        cursor.execute("SELECT * from mobile")
        print("Result ", cursor.fetchall())

        # Executing a SQL query to delete table
        delete_query = """Delete from mobile where id = 1"""
        # cursor.execute(delete_query)
        # connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")
        # Fetch result
        cursor.execute("SELECT * from mobile")
        print("Result ", cursor.fetchall())

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    import datetime
    import uuid

    #drop_table()
    _create_table()

    user = 1
    date = datetime.date.today()
    date += datetime.timedelta(days=1)
    exercise = uuid.uuid4()

    add_exercise(user, date, exercise)
    data = get_exercises_for_date(user, date)
    print(data)