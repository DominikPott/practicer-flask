import practicer_flask.topics.postgres


def _db_factory():
    return practicer_flask.topics.postgres


def topics():
    db = _db_factory()
    return db.topics()


def add_topic(topic):
    db = _db_factory()
    db.add_topic(topic)
