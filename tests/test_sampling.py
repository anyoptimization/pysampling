import unittest

from pysampling.sample import sample


class SamplingTest(unittest.TestCase):

    def test_random(self):
        sample("random", 50, 2, seed=1)

    def test_lhs(self):
        sample("lhs", 50, 2, seed=1)

    def test_sobol(self):
        sample("sobol", 50, 2, seed=1)

    def test_halton(self):
        sample("halton", 50, 2, seed=1)

if __name__ == '__main__':
    unittest.main()
