import unittest

import numpy as np

from pysample.indicators import centered_l2_discrepancy, wrapped_l2_discrepancy
from tests.util import load_resources


class IndicatorTest(unittest.TestCase):

    def test_centered_l2_discrepancy(self):
        X, correct = load_resources("random_set.x", "centered_l2_discrepancy.val")

        _val = centered_l2_discrepancy(X)
        self.assertTrue(np.abs(correct - _val) < 1e-4)

    def test_wrapped_l2_discrepancy(self):
        X, correct = load_resources("random_set.x", "wrapped_l2_discrepancy.val")
        _val = wrapped_l2_discrepancy(X)
        self.assertTrue(np.abs(correct - _val) < 1e-4)


if __name__ == '__main__':
    unittest.main()
