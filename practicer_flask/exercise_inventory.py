import json
import os


def exercises():
    root = os.path.dirname(__file__) + "/static/exercises"
    files = _find_exercise_files(root=root)
    exercise_data = _parse(files)
    return _sorted_by_categorie(exercise_data)


def _find_exercise_files(root):
    exercise_files = []
    for root_dir, dirs, files in os.walk(root):
        files = [f for f in files if f.endswith(".json")]
        exercise_files.extend([os.path.join(root_dir, exercise) for exercise in files])
    return exercise_files


def _parse(exercise_files):
    exercises_ = []
    for f in exercise_files:
        with open(f, "r") as exercise_file:
            data = json.load(exercise_file)
            data['path'] = f
        exercises_.append(data)
    return exercises_


def _sorted_by_categorie(exercises):
    return sorted(exercises, key=lambda exr: exr.get('categories', ['no categorie']))
