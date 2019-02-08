from pysample.methods.halton import HaltonSampling
from pysample.methods.lhs import LatinHypercubeSampling
from pysample.methods.random import RandomSampling
from pysample.methods.sobol import SobolSampling


def sample(method, n_samples, n_dim, *args, **kwargs):

    if method == "random":
        _method = RandomSampling(*args, **kwargs)
    elif method == "lhs":
        _method = LatinHypercubeSampling(*args, **kwargs)
    elif method == "halton":
        _method = HaltonSampling(*args, **kwargs)
    elif method == "sobol":
        _method = SobolSampling(*args, **kwargs)
    else:
        raise Exception("Unknown method for random sampling!")

    X = _method.sample(n_samples, n_dim)

    return X
