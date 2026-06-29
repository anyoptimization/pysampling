import numpy as np

from pysampling.sampling import Sampling
from pysampling.util import calc_primes_until


def halton_sequence(n, b):
    """First ``n`` terms of the base-``b`` van der Corput (Halton 1-D) sequence.

    Vectorized over points: it expands the radical-inverse digit by digit, so it
    loops only ``O(log_b n)`` times instead of once per point.
    """
    i = np.arange(n, dtype=np.int64)
    x = np.zeros(n, dtype=float)
    f = 1.0
    while i.any():
        f /= b
        x += f * (i % b)
        i //= b
    return x


class HaltonSampling(Sampling):
    def _sample(self, n_points, n_dim, rng):
        bases = calc_primes_until(500)[:n_dim]
        X = np.column_stack([halton_sequence(n_points, b) for b in bases])
        return X
