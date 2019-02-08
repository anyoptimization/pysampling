import os
import numpy as np



def path_to_test_resource(fname):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", fname)

def load_resources(*args, **kwargs):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")
    val = [np.loadtxt(os.path.join(path, fname), delimiter=",") for fname in args]
    if len(val) == 1:
        return val[0]
    else:
        return val
