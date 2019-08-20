import numpy as np

from pysampling.measures import minimum_distance, correlation
from pysampling.sampling import Sampling


def sample(n_points, n_dim, smooth=True):

    X = np.random.random(size=(n_points, n_dim))
    val = X.argsort(axis=0) + 1

    if smooth:
        val = val - np.random.random(val.shape)
    else:
        val = val - 0.5
    val /= n_points

    return val


class LatinHypercubeSampling(Sampling):

    def __init__(self,
                 criterion="maxmin",
                 iterations=1000,
                 **kwargs):

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
        for i in range(self.iterations):

            # random
            _X = sample(n_points, n_dim)
            _f = self.fun_obj(_X)

            # if better replace it
            if _f < f:
                X, f = _X, _f

        return X



