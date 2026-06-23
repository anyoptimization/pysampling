import numpy as np
import pytest

from pysampling.measures import (
    centered_l2_discrepancy,
    l2_discrepancy,
    l2_star_discrepancy,
    modified_l2_discrepancy,
    symmetric_l2_discrepancy,
    wrap_around_l2_discrepancy,
)
from tests.util import path_to_resources

# --------------------------------------------------------------------------- #
# LOOPED REFERENCE IMPLEMENTATIONS
# --------------------------------------------------------------------------- #
# Straightforward (slow) implementations kept as ground truth for the vectorized
# measures in pysampling.measures.


def wrap_around_l2_discrepancy_loop(X):
    n, m = X.shape
    s1 = 0

    for i in range(n):
        for k in range(n):
            p = np.prod(1.5 - ((abs(X[i,] - X[k,])) * (1 - abs(X[i,] - X[k,]))))
            s1 += p

    return np.sqrt(-((4 / 3) ** m) + ((1 / n**2) * s1))


def symmetric_l2_discrepancy_loop(X):
    n, m = X.shape
    s1 = 0
    s2 = 0

    for i in range(n):
        p = np.prod(1 + (2 * X[i,]) - (2 * X[i,] * X[i,]))
        s1 += p

        for k in range(n):
            q = np.prod(1 - abs(X[i,] - X[k,]))
            s2 += q

    return np.sqrt(((4 / 3) ** m) - ((2 / n) * s1) + ((2**m / n**2) * s2))


def modified_l2_discrepancy_loop(X):
    n, m = X.shape
    s1 = 0
    s2 = 0

    for i in range(n):
        p = np.prod(3 - (X[i,] * X[i,]))
        s1 += p

        for k in range(n):
            q = 1
            for j in range(m):
                q = q * (2 - max(X[i, j], X[k, j]))

            s2 += q

    return np.sqrt(((4 / 3) ** m) - (((2 ** (1 - m)) / n) * s1) + ((1 / n**2) * s2))


def l2_star_discrepancy_loop(X):
    n, m = X.shape

    dL2 = 0
    for j in range(n):
        for i in range(n):
            if i != j:
                t = []
                for d in range(m):
                    t.append(1 - max(X[i, d], X[j, d]))
                t = np.prod(np.array(t)) / (n**2)

            else:
                t1 = 1 - X[i,]
                t1 = np.prod(t1)
                t2 = 1 - X[i,] ** 2
                t2 = np.prod(t2)
                t = t1 / (n**2) - ((2 ** (1 - m)) / n) * t2

            dL2 += t

    return np.sqrt(3 ** (-m) + dL2)


def l2_discrepancy_loop(X):
    n, m = X.shape
    s1 = 0
    s2 = 0

    for i in range(n):
        s1 += np.prod(X[i] * (1 - X[i]))

        for k in range(n):
            q = 1
            for j in range(m):
                q = q * (1 - max(X[i, j], X[k, j])) * min(X[i, j], X[k, j])

            s2 += q

    return np.sqrt(12 ** (-m) - (((2 ** (1 - m)) / n) * s1) + ((1 / n**2) * s2))


def centered_l2_discrepancy_loop(X):
    n, m = X.shape

    s1 = 0
    for i in range(n):
        p = np.prod(1 + 0.5 * abs(X[i,] - 0.5) - 0.5 * ((abs(X[i,] - 0.5)) ** 2))
        s1 = s1 + p

    s2 = 0
    for i in range(n):
        for k in range(n):
            q = np.prod(
                1 + 0.5 * abs(X[i,] - 0.5) + 0.5 * abs(X[k,] - 0.5) - 0.5 * abs(X[i,] - X[k,])
            )
            s2 = s2 + q

    return np.sqrt(((13 / 12) ** m) - ((2 / n) * s1) + ((1 / n**2) * s2))


# --------------------------------------------------------------------------- #
# TESTS
# --------------------------------------------------------------------------- #
# (vectorized measure, looped reference, expected value on resources/discrepancy.x)

CASES = [
    (centered_l2_discrepancy, centered_l2_discrepancy_loop, 0.3325753),
    (l2_discrepancy, l2_discrepancy_loop, 0.01605584),
    (l2_star_discrepancy, l2_star_discrepancy_loop, 0.1394512),
    (modified_l2_discrepancy, modified_l2_discrepancy_loop, 0.4616604),
    (symmetric_l2_discrepancy, symmetric_l2_discrepancy_loop, 0.945297),
    (wrap_around_l2_discrepancy, wrap_around_l2_discrepancy_loop, 0.2215735),
]


@pytest.fixture(scope="module")
def X():
    return np.loadtxt(path_to_resources("discrepancy.x"))


@pytest.mark.parametrize("measure, loop, expected", CASES, ids=[c[0].__name__ for c in CASES])
def test_discrepancy_matches_expected(X, measure, loop, expected):
    assert measure(X) == pytest.approx(expected, abs=1e-6)


@pytest.mark.parametrize("measure, loop, expected", CASES, ids=[c[0].__name__ for c in CASES])
def test_vectorized_matches_loop(X, measure, loop, expected):
    assert measure(X) == pytest.approx(loop(X), abs=1e-8)
