import datetime

from flask import Blueprint, render_template, request

import practicer_flask.redis_db

bp = Blueprint('topic', __name__)

DB = practicer_flask.redis_db.get_db()
TIMEFORMAT = "%Y.%m.%d"


@bp.route('/topic', methods=['GET', 'POST'])
def topic():
    if request.method == 'POST':
        topic = request.form['topic']
        t = new_topic(topic)
        store_topic(t)
    topics = read_topics()
    topics = enrich_topics_with_relative_date(topics)
    return render_template("topic.html", topics=topics)


def enrich_topics_with_relative_date(topics):
    today = datetime.date.today()
    for topic in topics:
        topic_date = _string_date_to_date(date=topic['date'])
        if topic_date == today:
            topic['relative_date'] = 'today'
        elif topic_date > today:
            topic['relative_date'] = 'future'
        elif topic_date < today:
            topic['relative_date'] = 'past'
    return topics


def new_topic(topic):
    date = first_free_date()
    return {"date": date, "topic": topic}


def first_free_date():
    topics = read_topics()
    if not topics:
        return datetime.date.today().strftime(TIMEFORMAT)
    dates = sorted([topic['date'] for topic in topics], reverse=True)
    highest_date = _string_date_to_date(dates[0])
    if highest_date >= datetime.date.today():
        date = highest_date + datetime.timedelta(days=1)
    else:
        date = datetime.date.today()
    return date.strftime(TIMEFORMAT)


def _string_date_to_date(date):
    date = [int(d) for d in date.split('.')]
    return datetime.date(*date)


def read_topics():
    topics = []
    for date in DB.keys():
        data = {'date': date, 'topic': DB.get(date)}
        topics.append(data)
    topics = sorted(topics, key=lambda t: t.get('date', None), reverse=True)
    return topics


def store_topic(topic):
    DB.set(topic["date"], topic['topic'])
