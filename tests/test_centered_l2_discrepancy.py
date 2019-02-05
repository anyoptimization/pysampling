import os
import unittest

import numpy as np

from pysample.indicators import centered_l2_discrepancy_slow, centered_l2_discrepancy


class CenteredL2DiscrepancyTest(unittest.TestCase):

    def test_centered_l2_discrepancy(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")
        X = np.loadtxt(os.path.join(path, "centered_l2_discrepancy.x"), delimiter=",")
        correct = np.loadtxt(os.path.join(path, "centered_l2_discrepancy.val"), delimiter=",")

        _val = centered_l2_discrepancy_slow(X)
        self.assertTrue(np.abs(correct - _val) < 1e-4)

        _val = centered_l2_discrepancy(X)
        self.assertTrue(np.abs(correct - _val) < 1e-4)


if __name__ == '__main__':
    unittest.main()
