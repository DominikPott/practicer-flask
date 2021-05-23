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
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS topics (
                DATE TEXT PRIMARY KEY NOT NULL,
                TOPIC TEXT NOT NULL
                );
                '''
        cursor.execute(create_table_query)
        db.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while creating table.", error)
    finally:
        if db:
            cursor.close()
            db.close()


def _drop_table(name):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        create_table_query = f'DROP TABLE {name}'
        cursor.execute(create_table_query)
        db.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while dropping table", error)
    finally:
        if db:
            cursor.close()
            db.close()


def topics():
    query = 'SELECT * from topics'
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    topics_raw = cursor.fetchall()
    cursor.close()
    db.close()
    return list(map(map_to_dict, topics_raw))


def map_to_dict(topic):
    return {'date': topic[0], 'topic': topic[1]}


def add_topic(topic):
    date = topic['date']
    topic = topic['topic']
    query = f"INSERT INTO topics (DATE, TOPIC) VALUES ('{date}', '{topic}')"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    _drop_table(name='topics')
    _create_table()
    ts = [{'date': '2021.05.15', 'topic': 'Ananas'},
          {'date': '2021.05.16', 'topic': 'Bagger'},
          {'date': '2021.05.17', 'topic': 'Tomate'},
          {'date': '2021.05.18', 'topic': 'Zebra'},
          {'date': '2021.05.19', 'topic': 'Schwert'},
          {'date': '2021.05.20', 'topic': 'Maulwurf'},
          {'date': '2021.05.21', 'topic': 'Lampe'},
          {'date': '2021.05.22', 'topic': 'Geburtstagskuchen'},
          {'date': '2021.05.23', 'topic': 'Stift'},
          {'date': '2021.05.24', 'topic': 'Handy'},
          {'date': '2021.05.25', 'topic': 'Socke'},
          {'date': '2021.05.26', 'topic': 'Zecke'},
          {'date': '2021.05.27', 'topic': 'Bier'},
          {'date': '2021.05.28', 'topic': 'Feilchen'},
          {'date': '2021.05.29', 'topic': 'Breaking Bad'},
          {'date': '2021.05.30', 'topic': 'Walnuss'},
          {'date': '2021.05.31', 'topic': 'Waschmaschine'},
          {'date': '2021.06.01', 'topic': 'Pfeffer'},
          {'date': '2021.06.02', 'topic': 'Bett'},
          {'date': '2021.06.03', 'topic': 'Neonlicht'},
          {'date': '2021.06.04', 'topic': 'Brief'},
          ]
    for t in ts:
        add_topic(t)
    t = topics()
    print(t)
