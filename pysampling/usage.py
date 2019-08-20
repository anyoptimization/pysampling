import matplotlib.pyplot as plt

from pysample.sample import sample

X = sample("sobol", 8, 1, n_skip=0, setup="burkardt")

print(X)

# plt.scatter(X[:, 0], X[:, 1])
# plt.show()
