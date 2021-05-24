import practicer_flask.user_exercise_stats.experience_postgres

db = practicer_flask.user_exercise_stats.experience_postgres


def experience(user):
    return db.level(user=user)


def increment_experience(user, exercise):
    exp = experience(user)
    stats = _increment_exercise_stats(exp, exercise)
    _update(user, stats)


def _increment_exercise_stats(exp, exercise):
    old_experience = exp.get(exercise, 0)
    exp[exercise] = old_experience + 1
    return exp


def _update(user, exp):
    db.update_exp(user, exp)


if __name__ == "__main__":
    import practicer_flask.exercise_inventory as inv
    user = 0
    exp = experience(user=user)
    exercises = inv.exercises()
    print("Exp:", exp)
    increment_experience(user=user, exercise=exercises[1].get("uuid"))

    exp = experience(user=user)
    print("Exp:", exp)