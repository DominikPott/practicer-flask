""""Interface for exercise statistics."""
import datetime

import practicer_flask.user_exercise_stats.exercise_history_postgres as exercise_history
import practicer_flask.user_exercise_stats.streak

history_db = exercise_history
streak_db = practicer_flask.user_exercise_stats.streak

def exercise_histories(user):
    return history_db.exercieses(user=user)


def add_exercise_to_history(user, exercise):
    date = datetime.date.today()
    history_db.add_exercise(user, date, exercise["uuid"])


def streak(user):
    return streak_db.user_streak(user=user)


def increase_streak(user):
    streak_db.update_streak(user=user)
