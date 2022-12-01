import ctypes
import numpy as np

_mersenne_prime = np.uint64((1 << 61) - 1)
_max_hash = np.uint64((1 << 32) - 1)


class MinHash(object):
    def __init__(self, permutations):
        self._permutations = permutations
        self.hashvalues = self._init_hashvalues(len(self._permutations[0]))

    def _init_hashvalues(self, num_perm):
        return np.full(num_perm, _max_hash, dtype=np.uint64)

    def signature(self, values):
        a, b = self._permutations
        phv = np.bitwise_and(((np.array(values, dtype=np.uint64) * np.tile(a, (len(values), 1)).T).T + b) % _mersenne_prime, _max_hash)
        return np.vstack([phv, self.hashvalues]).min(axis=0)

    @classmethod
    def create(cls, permutations_count, generator):
        return cls(np.array([(generator.randint(1, _mersenne_prime, dtype=np.uint64), generator.randint(0, _mersenne_prime, dtype=np.uint64)) for _ in range(permutations_count) ], dtype=np.uint64).T)

def my_hash(value):
    return ctypes.c_size_t(hash(value)).value

def create(projections):
    return MinHash.create(projections, np.random.RandomState(42))
  
#mh = MinHash.create(128, np.random.RandomState(42))
#mh.update(my_hash("foo".encode("utf8")))
#mh.update(my_hash("bar".encode("utf8")))
#print (mh.hashvalues)

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
