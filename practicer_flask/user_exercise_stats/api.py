""""Filesystem / database interface to query exercise stats."""
import practicer_flask.user_exercise_stats.fs as filesystem
import practicer_flask.user_exercise_stats.postgres as postgres

db = postgres

_DEFAULT_STATS = {'count': 0, 'level': 0, 'progress': 0.0, 'level_max_progress': 1}


def load(exercise):
    try:
        return db.load_stats(exercise)
    except FileNotFoundError:
        return _DEFAULT_STATS


def increment(exercise):
    stats = load(exercise=exercise)
    stats = increment_exercise_stats(stats=stats)
    _update(exercise, stats)


def increment_exercise_stats(stats):
    stats["count"] += 1
    stats["progress"] += 1
    if stats["progress"] >= 10 * stats["level"]:
        stats["level"] += 1
        stats["progress"] = 0
    stats['level_max_progress'] = 10 * stats["level"]
    return stats


def _update(exercise, stats_):
    db.update_exercise_stats(exercise, stats_)
