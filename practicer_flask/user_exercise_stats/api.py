""""Interface for exercise statistics."""
import datetime

import practicer_flask.user_exercise_stats.history_postgres as exercise_history
import practicer_flask.user_exercise_stats.streak
import practicer_flask.user_exercise_stats.experience

history_db = exercise_history
streak_db = practicer_flask.user_exercise_stats.streak
level_db = practicer_flask.user_exercise_stats.experience


def levels(user):
    level_db.level(user=user)


def increase_level(user, exercise):
    level_db.increment_exercise(user, exercise)


def history(user):
    return history_db.exercieses(user=user)


def add_exercise_to_history(user, exercise):
    date = datetime.date.today()
    history_db.add_exercise(user, date, exercise["uuid"])


def streak(user):
    return streak_db.user_streak(user=user)


def increase_streak(user):
    streak_db.update_streak(user=user)
