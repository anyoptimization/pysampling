import numpy as np

from pysampling.sampling import Sampling


def riesz_energy_and_grad(X, s, periodic=False):
    """Riesz s-energy ``sum_{i<j} 1/||x_i - x_j||^s`` and its gradient, in one pass.

    Works in squared distances (no ``sqrt``): with ``D2 = ||x_i - x_j||^2`` the
    energy term is ``D2^(-s/2)`` and the per-point gradient is
    ``-s * sum_j (x_i - x_j) * D2^(-s/2 - 1)``. Self-pairs drop out because the
    diagonal of ``D2`` is set to ``inf`` (``inf`` to a negative power is ``0``).

    If ``periodic`` is set, distances are measured on the unit torus (opposite
    faces of the cube are glued together) via the minimum-image convention, so
    there is no boundary for points to pile up against.
    """
    diff = X[:, None, :] - X[None, :, :]  # (n, n, d)
    if periodic:
        diff = diff - np.round(diff)  # minimum image on the unit torus
    d2 = np.einsum("ijk,ijk->ij", diff, diff)  # (n, n) squared distances
    np.fill_diagonal(d2, np.inf)

    w = d2 ** (-s / 2.0 - 1.0)  # D2^(-s/2-1); diagonal -> 0
    energy = 0.5 * np.sum(d2 ** (-s / 2.0))  # diagonal -> inf^neg -> 0
    grad = -s * np.einsum("ijk,ij->ik", diff, w)
    return energy, grad


def riesz_energy(X, s, periodic=False):
    """Riesz s-energy of the point set ``X`` (see :func:`riesz_energy_and_grad`)."""
    return riesz_energy_and_grad(X, s, periodic)[0]


class RieszEnergySampling(Sampling):
    """Space-filling design by minimizing the Riesz s-energy in ``[0, 1]^n_dim``.

    Points repel each other (the energy ``sum 1 / ||x_i - x_j||^s`` blows up as
    points get close), so minimizing it spreads them out. The result is a
    *maximin* design — it maximizes the minimum distance between points, far more
    than random, LHS, Halton, or Sobol. It is **not** a low-discrepancy method,
    and its 1-D projections collapse, so prefer ``sobol``/``lhs`` when uniformity
    or projection properties matter.

    Two domain conventions are supported:

    - ``periodic=True`` (default) measures distance on the unit torus (opposite
      faces glued). There is no boundary, so points settle into an even,
      interior-filling lattice. This avoids the boundary collapse the clamped
      variant suffers in higher dimensions (where almost all of a cube's volume
      is near its faces).
    - ``periodic=False`` uses ordinary Euclidean distance and clamps points back
      into the box. Use it when the edges of ``[0, 1]^n_dim`` are real hard walls
      (so ``0.99`` and ``0.01`` are genuinely far apart, not neighbours). Points
      then tend to sit on the boundary.

    Optimization is Adam gradient descent with normalized gradients, stopped once
    the energy plateaus (``patience``). It is iterative and stochastic, so pass a
    ``seed`` for reproducibility. ``s`` defaults to ``n_dim``; larger ``s`` makes
    the repulsion more local.
    """

    def __init__(self, s=None, periodic=True, n_max_iter=1000, alpha=0.005, patience=50, **kwargs):
        super().__init__(**kwargs)
        self.s = s
        self.periodic = periodic
        self.n_max_iter = n_max_iter
        self.alpha = alpha
        self.patience = patience

    def _sample(self, n_points, n_dim):
        s = self.s if self.s is not None else n_dim

        X = np.random.random((n_points, n_dim))
        best, best_energy, stalled = X.copy(), np.inf, 0

        # Adam state for a stable gradient descent without external deps.
        m = np.zeros_like(X)
        v = np.zeros_like(X)
        b1, b2, eps = 0.9, 0.999, 1e-8

        for t in range(1, self.n_max_iter + 1):
            energy, grad = riesz_energy_and_grad(X, s, self.periodic)

            # plateau-based convergence: stop once the energy stops improving.
            # (Normalized gradients keep the step size ~constant, so a step-size
            # threshold would never trigger -- track the objective instead.)
            if energy < best_energy - 1e-12:
                best, best_energy, stalled = X.copy(), energy, 0
            else:
                stalled += 1
                if stalled >= self.patience:
                    break

            # normalize by the largest per-point gradient norm to keep steps sane
            norm = np.linalg.norm(grad, axis=1).max()
            if norm > 0:
                grad /= norm

            m = b1 * m + (1 - b1) * grad
            v = b2 * v + (1 - b2) * grad * grad
            X = X - self.alpha * (m / (1 - b1**t)) / (np.sqrt(v / (1 - b2**t)) + eps)
            X = X % 1.0 if self.periodic else np.clip(X, 0.0, 1.0)

        return best
