def experience_to_progress(experience):
    level = 0
    level_cap = calculate_level_cap(level=level)
    while experience >= level_cap:
        level += 1
        experience -= level_cap
        level_cap = calculate_level_cap(level=level)

    progress = 0
    if experience != 0:
        progress = float(experience) / level_cap

    return level, progress


def calculate_level_cap(level):
    return (level + 1) * 10


if __name__ == '__main__':
    print(experience_to_progress(35))