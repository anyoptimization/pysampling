from pysampling.algorithms.halton import HaltonSampling
from pysampling.algorithms.lhs import LatinHypercubeSampling
from pysampling.algorithms.random import RandomSampling
from pysampling.algorithms.riesz import RieszEnergySampling
from pysampling.algorithms.sobol import SobolSampling
from pysampling.sampling import Sampling


def sample(algorithm, n_points, n_dim, *args, **kwargs):

    _obj: Sampling

    if algorithm == "random":
        _obj = RandomSampling(*args, **kwargs)

    elif algorithm == "lhs":
        _obj = LatinHypercubeSampling(*args, **kwargs)

    elif algorithm == "halton":
        _obj = HaltonSampling(*args, **kwargs)

    elif algorithm == "sobol":
        _obj = SobolSampling(*args, **kwargs)

    elif algorithm == "riesz":
        _obj = RieszEnergySampling(*args, **kwargs)
    else:
        raise ValueError(
            f"Unknown sampling algorithm: {algorithm!r}. "
            "Options: ['random', 'lhs', 'halton', 'sobol', 'riesz']."
        )

    return _obj.sample(n_points, n_dim)
