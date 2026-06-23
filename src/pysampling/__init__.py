"""pysampling — sampling methods for design of experiments in Python.

Generate well-spread point sets in the unit hypercube using random, Latin
Hypercube, Halton, and Sobol sampling, and assess their quality with a suite of
uniformity/discrepancy measures.
"""

from __future__ import annotations

from pysampling.sample import sample

__version__ = "0.1.2"

__all__ = ["sample", "__version__"]
