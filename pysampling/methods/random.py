import numpy as np

from pysample.methods.sampling import Sampling


class RandomSampling(Sampling):

    def _sample(self, n_samples, n_dim):
        return np.random.random((n_samples, n_dim))
