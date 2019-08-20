
Installation
============

The framework is available at the PyPi Repository:

.. code-block:: bash

    pip install pysampling


Usage
=====

The method to be used for sampling using different algorithm must be
import from pysampling.sample. Here, we use Latin Hypercube Sampling to
generate 50 points in 2 dimensions.

.. code:: ipython3

    import matplotlib.pyplot as plt
    from pysampling.sample import sample

    X = sample("lhs", 50, 2)

    plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='r')
    plt.show()



Contact
=======

.. |blankjul| raw:: html

   <a href="http://www.cse.msu.edu/~blankjul/" target="_blank">My personal homepage</a>


|blankjul|

Feel free to contact me if you have any question:

::

    Julian Blank (blankjul [at] egr.msu.edu)
    Michigan State University
    Computational Optimization and Innovation Laboratory (COIN)
    East Lansing, MI 48824, USA


