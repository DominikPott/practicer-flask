_DEFAULT_STATS = {'count': 0, 'level': 0, 'progress': 0.0, 'level_max_progress': 1}

def load(exercise):
    try:
        return history_db.load_stats(exercise)
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
    history_db.update_exercise_stats(exercise, stats_)