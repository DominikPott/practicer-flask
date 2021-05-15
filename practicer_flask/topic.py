import csv
import datetime
import os

from flask import Blueprint, render_template, request

bp = Blueprint('topic', __name__)

DB_FILE = "static/topics.csv"


@bp.route('/topic', methods=['GET', 'POST'])
def topic():
    if request.method == 'POST':
        topic = request.form['topic']
        t = new_topic(topic)
        store_topic(t)
    return render_template("topic.html", topics=read_topics())


def new_topic(topic):
    date = first_free_date()
    return {"date": date, "topic": topic}


def first_free_date():
    timeformat = "%Y.%m.%d"
    topics = read_topics()
    if not topics:
        return datetime.date.today().strftime(timeformat)
    dates = sorted([topic['date'] for topic in topics], reverse=True)

    date = [int(d) for d in dates[0].split('.')]
    highest_date = datetime.date(*date)
    if highest_date >= datetime.date.today():
        date = highest_date + datetime.timedelta(days=1)
    else:
        date = datetime.date.today()
    return date.strftime(timeformat)


def read_topics():
    with open(DB_FILE, newline='') as topic_db:
        fieldnames = ['date', 'topic']
        reader = csv.DictReader(topic_db, fieldnames=fieldnames)
        topics = [topic for topic in reader]
    return sorted(topics, key=lambda topic: topic['date'], reverse=True)


def _create_db_file():
    basedir = os.path.dirname(DB_FILE)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    if not os.path.exists(DB_FILE):
        open(DB_FILE, 'a').close()


def store_topic(topic):
    with open(DB_FILE, 'a', newline='') as topic_db:
        writer = csv.writer(topic_db)
        writer.writerow([topic["date"], topic['topic']])
