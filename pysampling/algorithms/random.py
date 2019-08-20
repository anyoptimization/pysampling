import numpy as np

from pysampling.sampling import Sampling


class RandomSampling(Sampling):

    def _sample(self, n_points, n_dim):
        return np.random.random((n_points, n_dim))
