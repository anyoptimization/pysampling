pysampling
====================================================================

You can find the detailed documentation here: https://anyoptimization.com/projects/pysampling


|python| |license|



.. |python| image:: https://img.shields.io/badge/python-3.6-blue.svg
   :alt: python 3.6

.. |license| image:: https://img.shields.io/badge/license-apache-orange.svg
   :alt: license apache
   :target: https://www.apache.org/licenses/LICENSE-2.0



Installation
============

The framework is available at the PyPi Repository:

.. code-block:: bash

    pip install -U pysampling


Usage
=====

The method to be used for sampling using different algorithm must be
import from pysampling.sample. Here, we use Latin Hypercube Sampling to
generate 50 points in 2 dimensions.

.. code:: python

    import matplotlib.pyplot as plt
    from pysampling.sample import sample

    X = sample("lhs", 50, 2)

    plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='r')
    plt.show()



Contact
=======


Feel free to contact me if you have any question:

::

    Julian Blank (blankjul [at] egr.msu.edu)
    Michigan State University
    Computational Optimization and Innovation Laboratory (COIN)
    East Lansing, MI 48824, USA


