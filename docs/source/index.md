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
