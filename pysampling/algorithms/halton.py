import numpy as np

from pysampling.sampling import Sampling
from pysampling.util import calc_primes_until


def halton_sequence_by_index(i, b):
    f = 1.0
    x = 0.0
    while i > 0:
        f /= b
        x += f * (i % b)
        i = np.floor(i / b)
    return x


def halton_sequence(n, b):
    return np.array([halton_sequence_by_index(i, b) for i in range(n)])


class HaltonSampling(Sampling):

    def _sample(self, n_points, n_dim):
        bases = calc_primes_until(500)[:n_dim]
        X = np.column_stack([halton_sequence(n_points, b) for b in bases])
        return X
