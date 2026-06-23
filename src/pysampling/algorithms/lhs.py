import numpy as np

from pysampling.measures import correlation, minimum_distance
from pysampling.sampling import Sampling


def sample(n_points, n_dim, smooth=True):

    X = np.random.random(size=(n_points, n_dim))
    ranks = X.argsort(axis=0) + 1

    val = ranks - np.random.random(ranks.shape) if smooth else ranks - 0.5
    val = val / n_points

    return val


class LatinHypercubeSampling(Sampling):
    def __init__(self, criterion="maxmin", iterations=1000, **kwargs):

        super().__init__(**kwargs)
        self.criterion = criterion
        self.iterations = iterations

        if criterion == "maxmin":
            self.fun_obj = minimum_distance
        elif criterion == "correlation":
            self.fun_obj = correlation
        else:
            raise Exception("Criterion not known. Options: ['maxmin', 'correlation']")

    def _sample(self, n_points, n_dim):

        # sample the initial solution and evaluate
        X = sample(n_points, n_dim)
        f = self.fun_obj(X)

        # for each iteration try to improve it
        for _ in range(self.iterations):
            # random
            _X = sample(n_points, n_dim)
            _f = self.fun_obj(_X)

            # if better replace it
            if _f < f:
                X, f = _X, _f

        return X
