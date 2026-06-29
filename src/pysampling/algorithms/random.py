from pysampling.sampling import Sampling


class RandomSampling(Sampling):
    def _sample(self, n_points, n_dim, rng):
        return rng.random((n_points, n_dim))
