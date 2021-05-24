import datetime

import practicer_flask.user_exercise_stats.streak_postgres as db


def user_streak(user):
    return db.streak(user=user)


def update_streak(user):
    old_streak = user_streak(user)
    new_streak = _calculate_streak(old_streak)
    db.update_streak(user, new_streak)


def _calculate_streak(streak):
    length, last_day = streak
    if last_day >= datetime.date.today() - datetime.timedelta(days=2):
        length += 1
    else:
        length = 0
    last_day = datetime.date.today()
    return [length, last_day]


if __name__ == '__main__':
    user = 0
    streak = user_streak(user=user)
    print("Old: ", streak)
    new_streak = _calculate_streak(streak)
    print("New: ", new_streak)
    update_streak(user=user)
