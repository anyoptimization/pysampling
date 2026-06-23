"""Visualize a sampled point set.

Run with the optional plotting dependency installed::

    pip install pysampling[plot]
    python examples/plot_sampling.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from pysampling.sample import sample


def main() -> None:
    X = sample("sobol", 84, 2, n_skip=100, n_leap=10)
    plt.scatter(X[:, 0], X[:, 1], s=30, facecolors="none", edgecolors="r")
    plt.title("pysampling — sobol, 84 points in 2D")
    plt.show()


if __name__ == "__main__":
    main()
