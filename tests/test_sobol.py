import numpy as np

from pysampling.algorithms.sobol import SobolSampling
from tests.util import path_to_resources


def test_c_code_with_matlab_low_dim():
    correct = np.loadtxt(path_to_resources("test_sobol_1.txt"), delimiter=" ")
    val = SobolSampling(setup="burkardt", n_skip=0).sample(200, 2)
    assert np.all(np.abs(correct - val) < 1e-6)


def test_c_code_with_matlab_large_dim():
    correct = np.loadtxt(path_to_resources("test_sobol_2.txt"), delimiter=" ")
    val = SobolSampling(setup="burkardt", n_skip=0).sample(200, 30)
    assert np.all(np.abs(correct - val) < 1e-4)


def test_c_code_joekuo():
    correct = np.loadtxt(path_to_resources("test_sobol_3.txt"), delimiter=" ")
    val = SobolSampling(setup="joekuo", n_skip=0).sample(200, 70)
    assert np.all(np.abs(correct - val) < 1e-4)


def test_matlab_skip():
    correct = np.loadtxt(path_to_resources("test_sobol_4.txt"), delimiter=",")
    val = SobolSampling(setup="burkardt").sample(20, 2)
    assert np.all(np.abs(correct - val) < 1e-4)
