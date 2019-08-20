import numpy as np

from pysample.methods.sampling import Sampling
from pysample.indicators import minimum_distance, correlation, centered_l2_discrepancy, wrapped_l2_discrepancy
from pysample.optimization import random_search


class LatinHypercubeSampling(Sampling):

    def __init__(self, criterion="maxmin", optimizer="random_search", iterations=1000) -> None:
        super().__init__()
        self.criterion = criterion
        self.iterations = iterations
        self.optimizer = optimizer

        if criterion == "maxmin":
            self.fun_obj = minimum_distance
        elif criterion == "correlation":
            self.fun_obj = correlation
        elif criterion == "centered_l2_discrepancy":
            self.fun_obj = centered_l2_discrepancy
        elif criterion == "wrapped_l2_discrepancy":
            self.fun_obj = wrapped_l2_discrepancy
        else:
            raise Exception("Criterion not known.")

    def _sample(self, n_samples, n_dim):

        if self.optimizer == "random_search":
            fun_sample = lambda: _sample(n_samples, n_dim)
            X = random_search(fun_sample, self.fun_obj, self.iterations)

        elif self.optimizer == "simulated_annealing":

            pass

        elif self.optimizer == "ga":
            n_generations = 100
            pop_size = 20


        else:
            X = _sample(n_samples, n_dim)

        return X


def _sample(n_samples, n_var, smooth=True):
    X = np.random.random(size=(n_samples, n_var))
    val = X.argsort(axis=0) + 1

    if smooth:
        val = val - np.random.random(val.shape)
    else:
        val = val - 0.5
    val /= n_samples
    return val


