import matplotlib.pyplot as plt

from pysample.sample import sample

X = sample("sobol", 1000, 2, setup="matlab")

print(X)

plt.scatter(X[:, 0], X[:, 1])
plt.show()
