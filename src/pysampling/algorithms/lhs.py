import numpy as np

from pysampling.measures import correlation
from pysampling.sampling import Sampling

# Exponent of the phi_p maximin surrogate. Larger p tracks the true maximin (min
# distance) more tightly; 10 strongly favours the smallest distances without
# overflowing in float64. Used as q = p/2 on squared distances.
_PHI_P = 10.0


def lhs_draw(n_points, n_dim, rng, smooth=True):
    """A single Latin Hypercube draw in ``[0, 1]^n_dim``.

    Each column is a random permutation of ``n_points`` stratified cells; with
    ``smooth`` the point is jittered uniformly within its cell, otherwise it sits
    at the cell centre.
    """
    X = rng.random((n_points, n_dim))
    ranks = X.argsort(axis=0) + 1
    val = ranks - rng.random(ranks.shape) if smooth else ranks - 0.5
    return val / n_points


def maximin_swap(X, rng, sweeps, Xp=None, p=_PHI_P):
    """Maximin-optimize a Latin hypercube in place by within-column swaps.

    Morris-Mitchell local search: each step proposes exchanging two entries of one
    column (which keeps ``X`` a valid Latin hypercube) and keeps it only if it
    lowers the ``phi_p`` energy — a smooth surrogate for maximizing the minimum
    distance. ``sweeps`` is the number of passes; each tries ``n_points`` swaps. If
    ``Xp`` is given, the distance from the new points to that existing set is
    folded into the energy, so the design also avoids ``Xp``.

    Fast by construction: the squared-distance matrix is maintained incrementally.
    Swapping column ``j`` only changes the ``j``-th coordinate of the two points,
    so every affected squared distance is updated from its cached value using that
    single coordinate — an ``O(n_points)`` step, independent of ``n_dim``, rather
    than an ``O(n_points * n_dim)`` recompute. The swap loop is sequential, as
    local search must be.
    """
    n, n_dim = X.shape
    q = p / 2.0  # work in squared distances: d**-p == (d**2)**-q

    # squared pairwise distances among the new points (diagonal -> inf drops self)
    diff = X[:, None, :] - X[None, :, :]
    D2 = np.einsum("ijk,ijk->ij", diff, diff)
    np.fill_diagonal(D2, np.inf)
    # squared distances to the existing set, if any
    DC2 = None
    if Xp is not None:
        d = X[:, None, :] - Xp[None, :, :]
        DC2 = np.einsum("ijk,ijk->ij", d, d)

    def energy(d2_row, dc2_row):
        e = np.sum(d2_row**-q)
        if dc2_row is not None:
            e += np.sum(dc2_row**-q)
        return e

    for _ in range(sweeps):
        for _ in range(n):
            j = int(rng.integers(n_dim))
            a, b = (int(v) for v in rng.choice(n, size=2, replace=False))

            va, vb = X[a, j], X[b, j]
            if va == vb:
                continue  # swap would change nothing
            col = X[:, j]

            # Only coordinate j of a and b changes, so each squared distance
            # updates from its cached value via that one coordinate (O(n)).
            new_a = D2[a] + (vb - col) ** 2 - (va - col) ** 2
            new_b = D2[b] + (va - col) ** 2 - (vb - col) ** 2
            new_a[b] = new_b[a] = D2[a, b]  # the a-b distance is invariant
            new_a[a] = new_b[b] = np.inf
            new_dca = new_dcb = None
            if DC2 is not None:
                pj = Xp[:, j]
                new_dca = DC2[a] + (vb - pj) ** 2 - (va - pj) ** 2
                new_dcb = DC2[b] + (va - pj) ** 2 - (vb - pj) ** 2

            before = energy(D2[a], None if DC2 is None else DC2[a]) + energy(
                D2[b], None if DC2 is None else DC2[b]
            )
            after = energy(new_a, new_dca) + energy(new_b, new_dcb)

            if after <= before:  # keep the swap; commit the cached distances
                X[a, j], X[b, j] = vb, va
                D2[a, :] = D2[:, a] = new_a
                D2[b, :] = D2[:, b] = new_b
                D2[a, a] = D2[b, b] = np.inf
                if DC2 is not None:
                    DC2[a], DC2[b] = new_dca, new_dcb

    return X


class LatinHypercubeSampling(Sampling):
    """Latin Hypercube sampling.

    With the default ``criterion="maxmin"`` the design is optimized for spacing —
    it runs ``n_iter`` sweeps of Morris-Mitchell within-column swap search,
    maximizing the minimum pairwise distance. This beats plain random sampling and
    typically Sobol on both spacing and discrepancy.

    - ``criterion="maxmin"`` (default) — maximin swap optimization.
    - ``criterion="correlation"`` — keep the best of ``n_iter`` draws by
      lowest inter-column correlation.
    - ``criterion=None`` — a single raw draw (fastest; already low-discrepancy,
      just not distance-optimized).

    ``Xp`` is an optional ``(m, n_dim)`` array of existing points to keep the new
    sample *away* from: under ``criterion="maxmin"`` the maximized minimum distance
    spans both the new points and their distance to ``Xp``, turning LHS into an
    augmented / sequential design that adds infill points avoiding an existing set.
    """

    def __init__(self, criterion="maxmin", n_iter=20, smooth=True, Xp=None, **kwargs):

        super().__init__(**kwargs)
        self.criterion = criterion
        self.n_iter = n_iter
        self.smooth = smooth
        self.Xp = None if Xp is None else np.asarray(Xp, dtype=float)

        if criterion not in (None, "maxmin", "correlation"):
            raise ValueError(
                f"Unknown criterion: {criterion!r}. Options: [None, 'maxmin', 'correlation']."
            )

    def _sample(self, n_points, n_dim, rng):

        if self.Xp is not None and self.Xp.shape[-1] != n_dim:
            raise ValueError(
                f"Xp must have {n_dim} columns to match n_dim, got shape {self.Xp.shape}."
            )

        X = lhs_draw(n_points, n_dim, rng, self.smooth)

        # criterion=None: a single draw is enough (already low-discrepancy)
        if self.criterion is None:
            return X

        # maximin: swap-based local search (the single, best-spaced variant)
        if self.criterion == "maxmin":
            return maximin_swap(X, rng, self.n_iter, self.Xp)

        # correlation: keep the best of `n_iter` independent draws
        f = correlation(X)
        for _ in range(self.n_iter):
            _X = lhs_draw(n_points, n_dim, rng, self.smooth)
            _f = correlation(_X)
            if _f < f:
                X, f = _X, _f
        return X
