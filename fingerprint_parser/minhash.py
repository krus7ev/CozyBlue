import ctypes
import numpy as np

_mersenne_prime = np.uint64((1 << 61) - 1)
_max_hash = np.uint64((1 << 32) - 1)


class MinHash(object):
    def __init__(self, permutations):
        self._permutations = permutations

    def signature(self, values, old_signature=None):
        a, b = self._permutations
        hashes = np.bitwise_and(((np.array(values, dtype=np.uint64) * np.tile(a, (len(values), 1)).T).T + b) % _mersenne_prime, _max_hash)
        if old_signature: hashes = np.vstack([hashes, old_signature])
        return hashes.min(axis=0)

    @classmethod
    def create(cls, permutations_count, generator):
        return cls(generator.randint(1, _mersenne_prime, (2, permutations_count), dtype=np.uint64))

def my_hash(value):
    return ctypes.c_size_t(hash(value)).value

def create(projections):
    return MinHash.create(projections, np.random.RandomState(42))

# mh = MinHash.create(4, np.random.RandomState(1337))
# hashes = list(map(lambda x: my_hash(x.encode("utf8")), ["foo", "bar", "baz", "asd", "dsa", "sdf", "fds"]))
# sig1 = mh.signature(hashes)
# print (sig1)
# hashes2 = list(map(lambda x: my_hash(x.encode("utf8")), ["foo", "bar", "ddd", "dsa", "fds", "aaa", "asd", "sss"]))
# sig2 = mh.signature(hashes2)
# print (sig2)
# #
# #
# xor = sig1 ^ sig2
# print(xor)
# s = np.where(xor > 0, 0, 1)
# print (s.sum() / float(len(s)))
