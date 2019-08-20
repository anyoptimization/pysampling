import numpy as np

import re

from pysampling.sampling import Sampling
from pysampling.util import path_to_resource


class SobolSampling(Sampling):

    def __init__(self,
                 n_skip=None,
                 n_leap=0,
                 setup="joekuo",
                 **kwargs):

        super().__init__(**kwargs)

        if setup == "matlab":
            if n_skip is None:
                n_skip = 0
            max_bits = 53
            fname = "sobol_matlab.dat"

        elif setup == "burkardt":
            if n_skip is None:
                n_skip = -1
            max_bits = 32
            fname = "sobol_burkardt.dat"

        elif setup == "joekuo":
            if n_skip is None:
                n_skip = 0
            max_bits = 32
            fname = "sobol_joekuo.dat"

        else:
            raise Exception("Unknown setup.")

        self.setup = parse_file(path_to_resource(fname))
        self.n_skip = n_skip
        self.n_leap = n_leap
        self.max_bits = max_bits

    def _sample(self, n_points, n_dim):

        # find out how long the sequence needs to be - skip or leap included
        I = np.arange(0, n_points) * (self.n_leap + 1)
        if self.n_skip == -1:
            I += n_points
        else:
            I += self.n_skip
        n_sequence = np.max(I) + 1

        # contains all the values of the sequences as integer
        _X = np.zeros((n_sequence, n_dim), dtype=np.int)

        # number of bits which will be necessary for this sequence
        L = int(np.ceil(np.log2(n_sequence)))

        # number of bits necessary for the equation for each of them
        C = [highest_bit(i) for i in range(0, n_sequence)]

        for j in range(n_dim):

            if j == 0:
                V = np.concatenate((np.array([0]), 2 ** np.arange(self.max_bits-1, -1, -1)))

            else:

                s, a, m = self.setup[j]["s"], self.setup[j]["a"], self.setup[j]["m"]
                V = np.zeros(L + 1, dtype=np.int)

                if L <= s:
                    for k in range(1, L + 1):
                        V[k] = m[k - 1] << (self.max_bits - k)

                else:

                    for k in range(1, s + 1):
                        V[k] = m[k - 1] << (self.max_bits - k)

                    for i in range(s + 1, L + 1):
                        V[i] = V[i - s] ^ int(V[i - s] >> s)
                        for k in range(1, s):
                            V[i] ^= (((a >> (s - 1 - k)) & 1) * V[i - k])

            for i in range(1, n_sequence):
                _X[i, j] = _X[i - 1, j] ^ V[C[i - 1]]

        X = (_X / 2 ** self.max_bits)[I]
        return X


def highest_bit(i):
    bit = 1
    while i > 0 and i % 2 != 0:
        i = np.floor(i / 2)
        bit += 1
    return bit


def parse_file(path_to_file):
    setup = [{}]

    with open(path_to_file) as f:
        content = f.read().splitlines()[1:]

    for line in content:
        entries = [int(e) for e in re.split("\s+|\t", line.strip())]

        setup.append({
            'd': entries[0],
            's': entries[1],
            'a': entries[2],
            'm': np.array(entries[3:])

        })

    return setup
