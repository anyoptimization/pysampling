from pysample.sample import sample
import matplotlib.pyplot as plt

X = sample("lhs", 100, 2, criterion="maxmin", optimizer="ga")

plt.scatter(X[:, 0], X[:, 1])
plt.show()
