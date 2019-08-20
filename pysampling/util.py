import os

import numpy as np


def path_to_resource(fname):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", fname)


def cdist(A, B, _type="repeat"):
    if _type == "repeat":
        u = np.repeat(A, B.shape[0], axis=0)
        v = np.tile(B, (A.shape[0], 1))

        D = np.sqrt(np.sum((u - v) ** 2, axis=1))
        return np.reshape(D, (A.shape[0], B.shape[0]))

    elif _type == "repeat":
        _A = np.sum(A ** 2, axis=1)[None, ...]
        _B = np.sum(B ** 2, axis=1)[..., None]
        val = _A + _B - 2.0 * A @ B.T
        return np.sqrt(val)

    elif _type == "repeat":
        _A = A[:, None, ...]
        _B = B[None, ...]
        return np.sqrt(np.sum((_A - _B) ** 2, axis=2))

    else:
        raise Exception("Unknown type for cdist!")

    return M


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
