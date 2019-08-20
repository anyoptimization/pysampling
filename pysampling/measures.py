import numpy as np

from pysampling.util import cdist


def minimum_distance(X):
    D = cdist(X, X)
    np.fill_diagonal(D, np.inf)
    return - np.min(D)


def correlation(X):
    M = np.corrcoef(X.T, rowvar=True)
    return np.sum(np.tril(M, -1) ** 2)


# ---------------------------------------------------------------------------------------------------------
# Discrepancy
# ---------------------------------------------------------------------------------------------------------
#
# Reimplemented from https://rdrr.io/cran/DiceDesign/man/discrepancyCriteria.html


def centered_l2_discrepancy(X):
    n_points, n_dim = X.shape
    cX = np.abs(X - 0.5)

    s1 = ((1 + 0.5 * cX - 0.5 * cX ** 2).prod(axis=1)).sum()
    s2 = ((1 + 0.5 * cX[:, None] + 0.5 * cX[None, :] - 0.5 * np.abs(X[:, None] - X[None, :])).prod(axis=2)).sum()

    return np.sqrt(((13 / 12) ** n_dim) - ((2 / n_points) * s1) + ((1 / n_points ** 2) * s2))


def l2_discrepancy(X):
    n_points, n_dim = X.shape
    s1 = np.sum(np.prod(X * (1 - X), axis=1))
    s2 = np.sum(np.prod((1 - np.maximum(X[:, None], X[None, :])) * np.minimum(X[:, None], X[None, :]), axis=2))
    return np.sqrt(12 ** (-n_dim) - (((2 ** (1 - n_dim)) / n_points) * s1) + ((1 / n_points ** 2) * s2))


def l2_star_discrepancy(X):
    n_points, n_dim = X.shape

    # all off diagonal elements
    t1 = (1 - np.maximum(X[:, None], X[None, :])).prod(axis=2) / (n_points ** 2)
    t1 = t1 * (1 - np.eye(n_points))

    # all elements on the diagonal
    t2 = (1 - X).prod(axis=1) / (n_points ** 2) - ((2 ** (1 - n_dim)) / n_points) * (1 - X ** 2).prod(axis=1)

    return np.sqrt(3 ** (-n_dim) + t1.sum() + t2.sum())


def modified_l2_discrepancy(X):
    n_points, n_dim = X.shape

    s1 = (3 - X ** 2).prod(axis=1).sum()
    s2 = (2 - np.maximum(X[:, None], X[None, :])).prod(axis=2).sum()
    return np.sqrt(((4 / 3) ** n_dim) - (((2 ** (1 - n_dim)) / n_points) * s1) + ((1 / n_points ** 2) * s2))


def symmetric_l2_discrepancy(X):
    n_points, n_dim = X.shape

    s1 = (1 + (2 * X) - 2 * X ** 2).prod(axis=1).sum()
    s2 = (1 - np.abs(X[:, None] - X[None, :])).prod(axis=2).sum()
    return np.sqrt(((4 / 3) ** n_dim) - ((2 / n_points) * s1) + ((2 ** n_dim / n_points ** 2) * s2))


def wrap_around_l2_discrepancy(X):
    n_points, n_dim = X.shape

    val = np.abs(X[:, None] - X[None, :])
    s = (1.5 - val * (1 - val)).prod(axis=2).sum()

    return np.sqrt((-((4 / 3) ** n_dim) + ((1 / n_points ** 2) * s)))
