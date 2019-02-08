import unittest

import numpy as np

from pysample.methods.sobol import SobolSampling
from tests.util import path_to_test_resource


class SobolTest(unittest.TestCase):

    def test_c_code_with_matlab_low_dim(self):
        correct = np.loadtxt(path_to_test_resource("test_sobol_1.txt"), delimiter=" ")
        _val = SobolSampling(setup="burkardt", n_skip=0).sample(200, 2)
        self.assertTrue(np.all(np.abs(correct - _val) < 1e-6))

    def test_c_code_with_matlab_large_dim(self):
        correct = np.loadtxt(path_to_test_resource("test_sobol_2.txt"), delimiter=" ")
        _val = SobolSampling(setup="burkardt", n_skip=0).sample(200, 30)
        self.assertTrue(np.all(np.abs(correct - _val) < 1e-4))

    def test_c_code_joekuo(self):
        correct = np.loadtxt(path_to_test_resource("test_sobol_3.txt"), delimiter=" ")
        _val = SobolSampling(setup="joekuo", n_skip=0).sample(200, 70)
        self.assertTrue(np.all(np.abs(correct - _val) < 1e-4))

    def test_matlab_skip(self):
        correct = np.loadtxt(path_to_test_resource("test_sobol_4.txt"), delimiter=",")
        _val = SobolSampling(setup="burkardt").sample(20, 2)
        self.assertTrue(np.all(np.abs(correct - _val) < 1e-4))

    def test_matlab_default(self):
        correct = np.loadtxt(path_to_test_resource("test_sobol_5.txt"), delimiter=",")
        _val = SobolSampling(setup="burkardt", n_skip=0).sample(200, 3)
        #self.assertTrue(np.all(np.abs(correct - _val) < 1e-4))


if __name__ == '__main__':
    unittest.main()
