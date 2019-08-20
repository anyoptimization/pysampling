import numpy as np

class Sampling:
    """
    The abstract sampling class that builds the frame for each implementation of sampling methods.
    """

    def __init__(self, seed=None) -> None:
        super().__init__()
        self.seed = seed

    def sample(self, n_points, n_dim):

        if self.seed is not None:
            np.random.seed(self.seed)

        return self._sample(n_points, n_dim)

    def _sample(self, n_points, n_dim, *args):
        pass