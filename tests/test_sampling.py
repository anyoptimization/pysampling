import numpy as np
import pytest

from pysampling.sample import sample
from pysampling.util import cdist

ALGORITHMS = ["random", "lhs", "halton", "sobol", "riesz"]


def min_dist(X):
    D = cdist(X, X)
    np.fill_diagonal(D, np.inf)
    return D.min()


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_sample_shape_and_bounds(algorithm):
    X = sample(algorithm, 50, 2, seed=1)
    assert X.shape == (50, 2)
    assert np.all(X >= 0.0) and np.all(X <= 1.0)


def test_riesz_clamped_stays_in_box():
    X = sample("riesz", 50, 2, seed=1, periodic=False)
    assert X.shape == (50, 2)
    assert np.all(X >= 0.0) and np.all(X <= 1.0)


def test_riesz_spreads_points_more_than_random():
    # Riesz is a maximin design — its defining property is a larger minimum
    # pairwise distance than plain random sampling.
    rnd = min_dist(sample("random", 60, 2, seed=1))
    riesz = min_dist(sample("riesz", 60, 2, seed=1))
    assert riesz > rnd


def test_unknown_algorithm_raises():
    with pytest.raises(ValueError):
        sample("does-not-exist", 50, 2)
