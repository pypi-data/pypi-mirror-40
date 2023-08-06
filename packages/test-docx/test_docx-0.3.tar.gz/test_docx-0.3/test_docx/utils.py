import shutil
import os


def clean(value):
    return str(value).strip(" \n\t\r")


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def clean_dir(directory):
    shutil.rmtree(directory)


def delete_dir(path):
    try:
        clean_dir(path)
    except FileNotFoundError as _:
        pass
