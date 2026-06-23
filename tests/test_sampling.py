import numpy as np
import pytest

from pysampling.sample import sample

ALGORITHMS = ["random", "lhs", "halton", "sobol"]


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_sample_shape_and_bounds(algorithm):
    X = sample(algorithm, 50, 2, seed=1)
    assert X.shape == (50, 2)
    assert np.all(X >= 0.0) and np.all(X <= 1.0)


def test_unknown_algorithm_raises():
    with pytest.raises(ValueError):
        sample("does-not-exist", 50, 2)
