# pysampling

[![python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-apache-orange.svg)](https://www.apache.org/licenses/LICENSE-2.0)

Sampling methods for design of experiments in Python. `pysampling` generates
well-spread point sets in the unit hypercube `[0, 1]^d` and provides a suite of
measures to assess their uniformity.

Detailed documentation: https://anyoptimization.com/projects/pysampling

## Algorithms

| Key        | Method                  |
|------------|-------------------------|
| `random`   | Uniform random sampling |
| `lhs`      | Latin Hypercube Sampling |
| `halton`   | Halton sequence         |
| `sobol`    | Sobol sequence          |
| `riesz`    | Riesz s-energy (maximin) |

## Installation

```bash
pip install -U pysampling
```

## Usage

Import the `sample` function and pick an algorithm. Here we draw 50 points in 2
dimensions with Latin Hypercube Sampling:

```python
from pysampling.sample import sample

X = sample("lhs", 50, 2)
```

To visualize the result (requires the optional `plot` extra, `pip install
pysampling[plot]`):

```python
import matplotlib.pyplot as plt

plt.scatter(X[:, 0], X[:, 1], s=30, facecolors="none", edgecolors="r")
plt.show()
```

See [`examples/plot_sampling.py`](examples/plot_sampling.py) for a runnable demo.

## Development

This project uses [pyclawd](https://github.com/anyoptimization) as its dev
toolkit.

```bash
pip install -e . --group dev
pyclawd check        # format-check -> lint -> typecheck -> test
pyclawd test fast    # quick test run
```

### Documentation

The docs are built by a cached pipeline (see [`docs/`](docs/)):

```bash
pip install -e . --group docs   # one-time: install the docs toolchain
pyclawd docs build              # compile -> execute (cached) -> render HTML
pyclawd docs serve              # serve docs/build/html locally
```

## Contact

Questions, bugs, or feature requests? Please open an issue on
[GitHub](https://github.com/anyoptimization/pysampling/issues).

Maintained by [Julian Blank](https://julianblank.com).

## License

Apache License 2.0 — see [LICENSE](LICENSE).
