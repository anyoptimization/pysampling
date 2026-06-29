import numpy as np


def check_random_state(random_state):
    """Normalize ``random_state`` to a :class:`numpy.random.Generator`.

    Accepts ``None`` (fresh, non-deterministic generator), an ``int`` seed, or
    an existing :class:`numpy.random.Generator` (returned as-is, so a caller can
    thread their own stream straight through without touching global RNG state).
    """
    if random_state is None or isinstance(random_state, (int, np.integer)):
        return np.random.default_rng(random_state)
    if isinstance(random_state, np.random.Generator):
        return random_state
    raise TypeError(
        f"random_state must be None, an int, or a numpy.random.Generator, "
        f"got {type(random_state).__name__!r}."
    )


class Sampling:
    """
    The abstract sampling class that builds the frame for each implementation of sampling methods.
    """

    def __init__(self, random_state=None) -> None:
        super().__init__()
        self.random_state = random_state

    def sample(self, n_points, n_dim):
        rng = check_random_state(self.random_state)
        return self._sample(n_points, n_dim, rng)

    def _sample(self, n_points, n_dim, rng):
        pass
