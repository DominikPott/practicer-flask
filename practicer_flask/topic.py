import datetime

from flask import Blueprint, render_template, request, redirect, url_for

import practicer_flask.topics.api as db

bp = Blueprint('topic', __name__)

TIMEFORMAT = "%Y.%m.%d"


@bp.route('/topic', methods=['GET', 'POST'])
def topic():
    if request.method == 'POST':
        topic = request.form['topic']
        t = new_topic(topic)
        store_topic(t)
        return redirect(url_for('.topic'))
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
    topics = db.topics()
    topics = sorted(topics, key=lambda t: t.get('date', None), reverse=True)
    return topics


def store_topic(topic):
    db.add_topic(topic)
