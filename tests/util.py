import os


def path_to_resources(*args):
    parts = [os.path.dirname(os.path.realpath(__file__)), "resources", *args]
    return os.path.join(*parts)
