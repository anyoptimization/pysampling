from pysampling.algorithms.halton import HaltonSampling
from pysampling.algorithms.lhs import LatinHypercubeSampling
from pysampling.algorithms.random import RandomSampling
from pysampling.algorithms.sobol import SobolSampling


def sample(algorithm, n_points, n_dim, *args, **kwargs):

    if algorithm == "random":
        _obj = RandomSampling(*args, **kwargs)

    elif algorithm == "lhs":
        _obj = LatinHypercubeSampling(*args, **kwargs)

    elif algorithm == "halton":
        _obj = HaltonSampling(*args, **kwargs)

    elif algorithm == "sobol":
        _obj = SobolSampling(*args, **kwargs)
    else:
        raise Exception("Unknown method for random sampling.")

    return _obj.sample(n_points, n_dim)
