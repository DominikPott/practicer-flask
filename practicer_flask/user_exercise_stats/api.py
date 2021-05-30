""""Interface for exercise statistics."""
import datetime

import practicer_flask.user_exercise_stats.history_postgres as exercise_history
import practicer_flask.user_exercise_stats.streak
import practicer_flask.user_exercise_stats.experience
import practicer_flask.user_exercise_stats.progress as exercise_progress

history_db = exercise_history
streak_db = practicer_flask.user_exercise_stats.streak
experience_db = practicer_flask.user_exercise_stats.experience


def progress(user):
    progress_data = dict()
    experience_data = experience(user)
    for exercise in experience_data.keys():
        progress_data[exercise] = exercise_progress.experience_to_progress(experience_data[exercise])
    return progress_data


def experience(user):
    return experience_db.experience(user=user)


def increase_experience(user, exercise):
    experience_db.increment_experience(user, exercise)


def history(user):
    return history_db.exercieses(user=user)


def add_exercise_to_history(user, exercise):
    date = datetime.date.today()
    history_db.add_exercise(user, date, exercise["uuid"])


def streak(user):
    return streak_db.user_streak(user=user)


def increase_streak(user):
    streak_db.update_streak(user=user)


if __name__ == "__main__":
    print(progress(user=2))