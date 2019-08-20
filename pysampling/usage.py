import matplotlib.pyplot as plt

from pysampling.sample import sample

X = sample("sobol", 84, 2, n_skip=100, n_leap=10)

plt.scatter(X[:, 0], X[:, 1])
plt.show()

