import os

import numpy as np


def path_to_resources(fname):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", fname)


def cdist(A, B):
    u = np.repeat(A, B.shape[0], axis=0)
    v = np.tile(B, (A.shape[0], 1))

    D = np.sqrt(np.sum((u - v) ** 2, axis=1))
    M = np.reshape(D, (A.shape[0], B.shape[0]))
    return M


def cdist2(A, B):
    _A = np.sum(A ** 2, axis=1)[None, ...]
    _B = np.sum(B ** 2, axis=1)[..., None]
    val = _A + _B - 2.0 * A @ B.T
    return np.sqrt(val)


def cdist3(A, B):
    _A = A[:, None, ...]
    _B = B[None, ...]
    return np.sqrt(np.sum((_A - _B) ** 2, axis=2))




def calc_primes_until(n):
    size = n // 2
    sieve = [1] * size
    limit = int(n ** 0.5)
    for i in range(1, limit):
        if sieve[i]:
            val = 2 * i + 1
            tmp = ((size - 1) - i) // val
            sieve[i + val::val] = [0] * tmp

    return [2] + [i * 2 + 1 for i, v in enumerate(sieve) if v and i > 0]



"""

def expanded_pairwise_distances(A, B=None):
    '''
    Input: x is a Nxd matrix
           y is an optional Mxd matirx
    Output: dist is a NxM matrix where dist[i,j] is the square norm between x[i,:] and y[j,:]
            if y is not given then use 'y=x'.
    i.e. dist[i,j] = ||x[i,:]-y[j,:]||^2
    '''

    x = torch.from_numpy(A._value)

    if B is not None:
        y = torch.from_numpy(B._value)
    else:
        y = None

    if y is not None:
         differences = x.unsqueeze(1) - y.unsqueeze(0)
    else:
        differences = x.unsqueeze(1) - x.unsqueeze(0)
    distances = torch.sum(differences * differences, -1)
    return distances


def pairwise_distances(A, B=None):
    '''
    Input: x is a Nxd matrix
           y is an optional Mxd matirx
    Output: dist is a NxM matrix where dist[i,j] is the square norm between x[i,:] and y[j,:]
            if y is not given then use 'y=x'.
    i.e. dist[i,j] = ||x[i,:]-y[j,:]||^2
    '''

    x = torch.from_numpy(A._value)

    if B is not None:
        y = torch.from_numpy(B._value)
    else:
        y = None

    x_norm = (x ** 2).sum(1).view(-1, 1)
    if y is not None:
        y_t = torch.transpose(y, 0, 1)
        y_norm = (y ** 2).sum(1).view(1, -1)
    else:
        y_t = torch.transpose(x, 0, 1)
        y_norm = x_norm.view(1, -1)

    dist = x_norm + y_norm - 2.0 * torch.mm(x, y_t)
    # Ensure diagonal is zero if x=y
    # if y is None:
    #     dist = dist - torch.diag(dist.diag)
    return dist

"""
