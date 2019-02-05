import numpy as np


def random_search(fun_sample, fun_obj, iterations):
    X, f = None, np.inf

    for i in range(iterations):
        _X = fun_sample()
        _f = fun_obj(_X)

        if _f < f:
            f = _f
            X = _X

    return X


def ga(fun_sample, fun_obj, fun_crossover, fun_mutation, pop_size=20, n_gen=100):
    X = [fun_sample for _ in range(pop_size)]
    F = [fun_obj(ind) for ind in X]

    for i in range(n_gen):
        parents = np.random.random(size=(pop_size, 2)).argsort(axis=0)

        _X = []
        for mating in parents:
            a, b = X[mating[0]], X[mating[1]]
            offsprings = fun_crossover(a, b)
            offsprings = [fun_mutation(off) for off in offsprings]
            offsprings = [off for off in offsprings if np.any(off != a) and np.any(off != b)]
            _X.extend(offsprings)

        _F = [fun_obj(ind) for ind in _X]

        X, F = X + _X, F + _F

        I = np.argsort(F)[:pop_size]
        X, F = [X[i] for i in I], [F[i] for i in I]

    return X
