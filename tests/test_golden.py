"""Golden behavior baselines: pin the exact point set each method emits for a
fixed ``random_state``. Unlike the shape/bounds checks in ``test_sampling.py``,
these lock the actual numbers, so any future drift in the RNG wiring or an
algorithm's output is caught. Bless intended changes with ``pyclawd golden
update`` (humans review the diff); agents only run the compare.
"""

import pytest

from pysampling.sample import sample

ALGORITHMS = ["random", "lhs", "halton", "sobol", "riesz"]


@pytest.mark.golden
@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=ALGORITHMS)
def test_sample_is_reproducible(algorithm):
    # Fixed random_state -> deterministic output for the stochastic methods
    # (random, lhs, riesz); sobol/halton are deterministic regardless.
    return sample(algorithm, 25, 3, random_state=1)
