from pysample.util import cdist

import numpy as np


def minimum_distance(X):
    D = cdist(X, X)
    D = D + 1e12 * np.eye(X.shape[0])
    return - np.min(D)


def correlation(X):
    M = np.corrcoef(X.T, rowvar=True)
    return np.sum(np.tril(M, -1) ** 2)


def centered_l2_discrepancy(X):

    n_points, n_dim = X.shape
    acmh = np.abs(X - 0.5)

    _X = np.abs(X.T[..., None] - X.T[:, None, :])
    _acmh = np.abs(acmh.T[..., None] + acmh.T[:, None, :])

    val = np.sum(np.prod((1 + 0.5 * (_acmh - _X)), axis=0))
    val = ((13 / 12) ** n_dim - 2 / n_points * np.sum(
        np.prod(1 + 0.5 * (acmh - acmh ** 2), axis=1)) + val / n_points ** 2) ** 0.5

    return val



def wrapped_l2_discrepancy(X):

    """

    [Npts,Ndim]=size(coord);
    WDL2=0;
    for k=1:Npts
        yada=abs(coord(:,1)-coord(k,1));
        temp=(1.5-yada.*(1-yada));
        for i=2:Ndim
            yada=abs(coord(:,i)-coord(k,i));
            temp=temp.*(1.5-yada.*(1-yada));
        end
        WDL2=WDL2+sum(temp);
    end
    WDL2=(-(4/3)^Ndim+WDL2/Npts^2)^0.5; %^0.5;

    end
    """
    n_points, n_dim = X.shape
    _X = np.abs(X.T[..., None] - X.T[:, None, :])
    val = np.sum(np.prod((1.5 - _X * (1-_X)), axis=0))
    val = (-(4 / 3) ** n_dim + val / n_points ** 2) ** 0.5

    return val
