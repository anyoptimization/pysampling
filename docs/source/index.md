---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# pysampling

![python](https://img.shields.io/badge/python-3.10+-blue.svg)
![license](https://img.shields.io/badge/license-apache-orange.svg)

<https://github.com/anyoptimization/pysampling>

## Installation

The framework is available at the PyPi Repository:

```bash
pip install -U pysampling
```

## Usage

The method to be used for sampling using a different algorithm must be imported
from `pysampling.sample`. Here, we use Latin Hypercube Sampling to generate 50
points in 2 dimensions.

```{code-cell} ipython3
from pysampling.sample import sample

X = sample("lhs", 50, 2)
```

Then, we recommend using matplotlib or other visualization libraries to have a
look at the results:

```{code-cell} ipython3
import matplotlib.pyplot as plt

plt.scatter(X[:, 0], X[:, 1], s=30, facecolors="none", edgecolors="r")
plt.show()
```

## Features

So far our library provides the following implementations:

- Random (`'random'`)
- Latin Hypercube Sampling (`'lhs'`)
- Sobol (`'sobol'`)
- Halton (`'halton'`)
- Riesz s-energy (`'riesz'`)

The initialization of each of those will be shown in the following. Let us first
define a method that helps us to visualize them in a 2d space.

```{code-cell} ipython3
import matplotlib.pyplot as plt


def show(X):
    plt.figure(figsize=(5, 5))
    plt.scatter(X[:, 0], X[:, 1], s=30, facecolors="none", edgecolors="r")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect("equal")
    plt.show()
```

### Random (`'random'`)

```{code-cell} ipython3
X = sample("random", 50, 2, seed=1)
show(X)
```

### Latin Hypercube Sampling (`'lhs'`)

```{code-cell} ipython3
X = sample("lhs", 50, 2, seed=1)
show(X)
```

### Sobol (`'sobol'`)

```{code-cell} ipython3
X = sample("sobol", 84, 2)
show(X)
```

The Sobol sequence can be customized — for example, skipping the first points
and leaping over points in the sequence:

```{code-cell} ipython3
X = sample("sobol", 84, 2, n_skip=100, n_leap=10)
show(X)
```

### Halton (`'halton'`)

```{code-cell} ipython3
X = sample("halton", 100, 2)
show(X)
```

### Riesz s-energy (`'riesz'`)

Riesz sampling places points by minimizing the s-energy
`sum_{i<j} 1 / ||x_i - x_j||^s` — the points repel each other, so they
spread out as far apart as possible. It is a **maximin** design: it maximizes the
minimum distance between points, far more than the other methods. It is *not* a
low-discrepancy method (and its 1-D projections collapse), so reach for `sobol`
or `lhs` when uniformity or projection quality matter, and for `riesz` when you
want maximally well-separated points.

```{code-cell} ipython3
X = sample("riesz", 100, 2, seed=1)
show(X)
```

By default the energy is measured **periodically** — distances wrap around the
unit cube (opposite faces are glued together, as on a torus), so there is no
boundary for points to pile up against. Passing `periodic=False` instead uses
ordinary Euclidean distance and clamps points into the box, which pushes them
onto the boundary:

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt

from pysampling.util import cdist


def min_dist(Y):
    D = cdist(Y, Y)
    np.fill_diagonal(D, np.inf)
    return D.min()


fig, axes = plt.subplots(1, 2, figsize=(10, 5))
for ax, periodic in zip(axes, [False, True]):
    Y = sample("riesz", 100, 2, seed=1, periodic=periodic)
    ax.scatter(Y[:, 0], Y[:, 1], s=25, facecolors="none", edgecolors="r")
    ax.set_title(f"periodic={periodic}  (min-dist={min_dist(Y):.3f})")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
plt.show()
```

> **Note** — The clamped (`periodic=False`) variant is fine in 2-D, but it
> **degrades as the dimension grows**: almost all of a hypercube's volume lies
> near its boundary, so the points collapse onto faces and corners — in 10-D
> nearly every coordinate ends up pinned to 0 or 1. The periodic default
> (recommended) avoids this and stays an even, interior-filling design. Use
> `periodic=False` only when the edges of the box are genuine hard walls.

## Comparing uniformity

A more uniform spread has a lower discrepancy. We can quantify it with the
measures in `pysampling.measures` — here the centered L2 discrepancy of 100
points in 2D for each algorithm (lower is better):

```{code-cell} ipython3
from pysampling.measures import centered_l2_discrepancy

for name in ["random", "lhs", "halton", "sobol"]:
    Y = sample(name, 100, 2, seed=1)
    print(f"{name:8s} {centered_l2_discrepancy(Y):.5f}")
```

## Contact

Questions, bugs, or feature requests? Please open an issue on
[GitHub](https://github.com/anyoptimization/pysampling/issues).

Maintained by [Julian Blank](https://julianblank.com).
