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
    X = sample(algorithm, 50, 2, random_state=1)
    assert X.shape == (50, 2)
    assert np.all(X >= 0.0) and np.all(X <= 1.0)


def test_riesz_clamped_stays_in_box():
    X = sample("riesz", 50, 2, random_state=1, periodic=False)
    assert X.shape == (50, 2)
    assert np.all(X >= 0.0) and np.all(X <= 1.0)


def test_riesz_spreads_points_more_than_random():
    # Riesz is a maximin design — its defining property is a larger minimum
    # pairwise distance than plain random sampling.
    rnd = min_dist(sample("random", 60, 2, random_state=1))
    riesz = min_dist(sample("riesz", 60, 2, random_state=1))
    assert riesz > rnd


def test_unknown_algorithm_raises():
    with pytest.raises(ValueError):
        sample("does-not-exist", 50, 2)


def _min_cross_dist(A, B):
    return cdist(A, B).min()


def test_lhs_xp_keeps_distance_from_existing():
    # An Xp-aware maximin draw should sit further from the existing set than a
    # plain single draw of the same size.
    Xp = sample("lhs", 30, 2, random_state=0)
    plain = sample("lhs", 30, 2, criterion=None, random_state=1)
    aware = sample("lhs", 30, 2, Xp=Xp, random_state=1)
    assert _min_cross_dist(aware, Xp) > _min_cross_dist(plain, Xp)


def test_lhs_xp_dimension_mismatch_raises():
    Xp = sample("lhs", 10, 3, random_state=0)  # 3 columns
    with pytest.raises(ValueError):
        sample("lhs", 10, 2, Xp=Xp, random_state=1)  # but n_dim=2


def test_lhs_maxmin_beats_single_draw():
    # The default maxmin (swap) optimization reaches a strictly larger minimum
    # distance than an unoptimized single draw.
    single = min_dist(sample("lhs", 50, 2, criterion=None, random_state=1))
    maxmin = min_dist(sample("lhs", 50, 2, random_state=1))
    assert maxmin > single


def test_lhs_n_iter_improves_spacing():
    # More sweeps never worsen the maximin spacing (swap keeps improving).
    few = min_dist(sample("lhs", 50, 2, n_iter=2, random_state=1))
    many = min_dist(sample("lhs", 50, 2, n_iter=40, random_state=1))
    assert many >= few
