import os


def path_to_resources(*args):
    l = [os.path.dirname(os.path.realpath(__file__))]
    l.append("resources")
    l.extend(args)
    return os.path.join(*l)
