import sys
import numpy as np

_mersenne_prime = np.uint64((1 << 61) - 1)
_max_hash = np.uint64((1 << 32) - 1)


class MinHash(object):
    def __init__(self, permutations):
        self._a, self._b = permutations
        self._default_signature = np.full(permutations.shape[1], _max_hash)

    def signature(self, values, old_signature=None):
        return np.vstack([
            (np.outer(np.array(values, dtype=np.uint64), self._a) + self._b) % _mersenne_prime & _max_hash,
            self._default_signature if old_signature is None else old_signature,
        ]).min(axis=0)

    @classmethod
    def create(cls, permutations_count, generator):
        return cls(generator.randint(1, _mersenne_prime, (2, permutations_count), dtype=np.uint64))

def my_hash(value):
    return hash(value) % ((sys.maxsize + 1) * 2)

def create(projections, seed=42):
    return MinHash.create(projections, np.random.RandomState(seed))

#hashes = list(map(lambda x: my_hash(x.encode("utf8")), ["foo", "bar", "baz", "asd", "dsa", "sdf", "fds"]))
#sig1 = mh.signature(hashes)
#print (sig1)
# hashes2 = list(map(lambda x: my_hash(x.encode("utf8")), ["foo", "bar", "ddd", "dsa", "fds", "aaa", "asd", "sss"]))
# sig2 = mh.signature(hashes2)
# print (sig2)

# print (len(np.where(sig1 == sig2)) / float(len(sig1))) #jaccard similarity
