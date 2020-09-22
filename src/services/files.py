import os
import shutil
import json
from pathlib import Path


def create_dir(path, delete_data=False):
    if delete_data:
        delete_dir(path)
    if not os.path.exists(path):
        os.makedirs(path)


def delete_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def join(folder, filename):
    return os.path.join(folder, filename)


def exists(path):
    return os.path.exists(path)


def list_dir(path):
    try:
        files = os.listdir(path)
        return list(map(lambda file: join(path, file), files))
    except FileNotFoundError:
        return []


def rebase_path(file_path, new_path):
    path = Path(file_path)
    return join(new_path, path.name)


def get_filename(file_path):
    path = Path(file_path)
    return path.name


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.loads(f.read())
