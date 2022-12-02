import itertools
import collections

import scipy.integrate as integrate

import minhash

def flatten(list_of_lists):
    return itertools.chain.from_iterable(list_of_lists)

class Lsh(object):
    def __init__(self, minhash, hashtables):
        self._minhash = minhash
        self._hashtables = hashtables

    def index(self, features, key):
        self._hashtables.add(key, self._minhash.signature(features))

    def query(self, features):
        return self._hashtables.candidates(self._minhash.signature(features))

    def dump(self):
        pass

    @classmethod
    def create(cls, projections, threshold):
        return cls(minhash.create(projections), Hashtables.create(projections, threshold))

def _false_positive(start, end):
    return lambda x : 1 - (1 - x**float(end))**float(start)

def _false_negative(start, end):
    return lambda x : 1 - (1 - (1 - x**float(end))**float(start))

def _integrate(function, start, end):
    return integrate.quad(function, start, end)[0]


class RangeCalculator(object):
    def __init__(self, threshold):
        self._threshold = threshold

    def compute(self, projections):
        return min(self.ranges(projections), key=self._error)

    def ranges(self, projections):
        return ((start, end) for start in range(1, projections+1) for end in range(1, projections // start + 1))

    def _error(self, interval):
        return _integrate(_false_positive(*interval), 0.0, self._threshold) + _integrate(_false_negative(*interval), self._threshold, 1.0)

class Hashtables(object):
    def __init__(self, bands, storage):
        self._bands = bands
        self._storage = storage

    def add(self, key, signature):
        for band, table in zip(self._bands, self._storage):
            table.add(key, signature[band])

    def candidates(self, signature):
        return set(flatten([table.get(signature[band]) for band, table in zip(self._bands, self._storage)]))

    @classmethod
    def create(cls, projections, threshold):
        calculator = RangeCalculator(threshold)
        bands, size = calculator.compute(projections)
        return cls([slice(i*size, (i+1)*size) for i in range(bands)], [Table.create() for _ in range(bands)])

class Table(object):
    def __init__(self, data):
        self._data = data

    def add(self, key, signature):
        self._data[self._hash(signature)].add(key)

    def get(self, signature):
        return self._data[self._hash(signature)]

    def _hash(self, signature):
        return "-".join([str(x) for x in signature])

    @classmethod
    def create(cls):
        return cls(collections.defaultdict(set))

def create(projections, threshold):
    return Lsh.create(projections, threshold)
